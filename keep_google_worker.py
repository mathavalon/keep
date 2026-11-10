#!/usr/bin/env python3
"""Worker do Keep para Search Console e Analytics.

As chaves são só deste worker. Ele não lê o cliente OAuth do Skill.
O refresh token fica em data/google_keep_token.json e não entra no painel.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"
TOKEN_PATH = BASE_DIR / "data" / "google_keep_token.json"
TRAFFIC_PATH = BASE_DIR / "data" / "traffic.json"
REDIRECT_URI = os.environ.get("KEEP_GOOGLE_REDIRECT_URI", "http://127.0.0.1:8787/oauth/callback")
SCOPES = " ".join([
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
])
SAO_PAULO = ZoneInfo("America/Sao_Paulo")


def client_config() -> tuple[str, str]:
    client_id = os.environ.get("KEEP_GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("KEEP_GOOGLE_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise SystemExit(
            "Faltam KEEP_GOOGLE_CLIENT_ID e KEEP_GOOGLE_CLIENT_SECRET.\n"
            "Use um cliente OAuth novo, no projeto Keep da mesma conta Google. "
            "Não use a chave do worker da Avalon."
        )
    return client_id, client_secret


def request_json(url: str, method: str = "GET", headers: dict | None = None, body: dict | bytes | None = None) -> dict:
    data = None
    req_headers = dict(headers or {})
    if isinstance(body, dict):
        data = json.dumps(body).encode()
        req_headers.setdefault("Content-Type", "application/json")
    elif isinstance(body, bytes):
        data = body
    request = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        try:
            message = json.loads(detail).get("error", {}).get("message", detail)
        except json.JSONDecodeError:
            message = detail
        raise SystemExit(f"Google recusou a chamada ({error.code}): {message}") from error
    return json.loads(raw.decode()) if raw else {}


def google_token(form: dict[str, str]) -> dict:
    body = urllib.parse.urlencode(form).encode()
    token = request_json(
        "https://oauth2.googleapis.com/token",
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        body=body,
    )
    if not token.get("access_token"):
        raise SystemExit("O Google não devolveu um access token.")
    return token


def save_refresh_token(token: dict) -> None:
    refresh = token.get("refresh_token")
    if not refresh:
        raise SystemExit("O Google não devolveu refresh token. Rode connect de novo e aceite o consentimento.")
    TOKEN_PATH.write_text(json.dumps({
        "refresh_token": refresh,
        "scopes": token.get("scope", SCOPES),
        "connected_at": datetime.now(SAO_PAULO).isoformat(timespec="seconds"),
    }, indent=2), encoding="utf-8")
    TOKEN_PATH.chmod(0o600)


def access_token() -> str:
    if not TOKEN_PATH.exists():
        raise SystemExit("O Keep ainda não tem token. Rode: python3 keep_google_worker.py connect")
    saved = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    client_id, client_secret = client_config()
    token = google_token({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": saved["refresh_token"],
        "grant_type": "refresh_token",
    })
    return token["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


class Callback(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/oauth/callback":
            self.send_error(404)
            return
        query = urllib.parse.parse_qs(parsed.query)
        self.server.oauth_code = query.get("code", [None])[0]  # type: ignore[attr-defined]
        self.server.oauth_state = query.get("state", [None])[0]  # type: ignore[attr-defined]
        self.server.oauth_error = query.get("error", [None])[0]  # type: ignore[attr-defined]
        body = "Keep recebeu o acesso. Pode fechar esta aba.".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def connect() -> None:
    client_id, client_secret = client_config()
    state = secrets.token_urlsafe(24)
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "false",
        "state": state,
    })
    host, port = "127.0.0.1", 8787
    server = HTTPServer((host, port), Callback)
    print("Abra o login se o navegador não abrir sozinho.")
    webbrowser.open(f"https://accounts.google.com/o/oauth2/v2/auth?{params}")
    server.timeout = 1
    deadline = time.time() + 180
    while time.time() < deadline and not getattr(server, "oauth_code", None) and not getattr(server, "oauth_error", None):
        try:
            server.handle_request()
        except socket.timeout:
            continue
    if time.time() >= deadline and not getattr(server, "oauth_code", None):
        raise SystemExit("O login não voltou em 3 minutos.")
    if getattr(server, "oauth_error", None):
        raise SystemExit(f"Login cancelado: {server.oauth_error}")
    if getattr(server, "oauth_state", None) != state or not getattr(server, "oauth_code", None):
        raise SystemExit("A resposta do Google não confere com este login.")
    token = google_token({
        "code": server.oauth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    save_refresh_token(token)
    print(f"Token salvo em {TOKEN_PATH.name}. Ele não entra no dashboard.")
    show_accounts(token["access_token"])


def show_accounts(token: str) -> None:
    sites = request_json("https://www.googleapis.com/webmasters/v3/sites", headers=auth_header(token))
    print("\nSearch Console:")
    for entry in sites.get("siteEntry", []):
        print(f"  {entry.get('permissionLevel', ''):<16} {entry.get('siteUrl', '')}")
    summaries = request_json(
        "https://analyticsadmin.googleapis.com/v1beta/accountSummaries?pageSize=50",
        headers=auth_header(token),
    )
    print("\nAnalytics:")
    for account in summaries.get("accountSummaries", []):
        for prop in account.get("propertySummaries", []):
            property_id = str(prop.get("property", "")).split("/")[-1]
            print(f"  {property_id:<14} {prop.get('displayName', '')}")


def month_bounds(start: date, end: date) -> list[tuple[str, date, date]]:
    bounds = []
    year, month = start.year, start.month
    while date(year, month, 1) <= end:
        first = date(year, month, 1)
        if month == 12:
            nxt = date(year + 1, 1, 1)
        else:
            nxt = date(year, month + 1, 1)
        last = min(end, nxt.fromordinal(nxt.toordinal() - 1))
        bounds.append((f"{year:04d}-{month:02d}", max(first, start), last))
        year, month = nxt.year, nxt.month
    return bounds


def page_path(value: str) -> str:
    path = urllib.parse.urlsplit(value.strip()).path or value.strip()
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/").lower() or "/"


def article_paths(brand: str) -> dict[str, str]:
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    paths = {}
    for article in kb["brands"][brand]["articles"]:
        url = article.get("url") or ""
        if url:
            paths[page_path(url)] = url
    return paths


def pull_search_console(token: str, site: str, start: date, end: date, paths: dict[str, str]) -> tuple[dict[str, int], dict[str, dict[str, float]]]:
    monthly: dict[str, int] = {}
    pages: dict[str, dict[str, float]] = {}
    encoded_site = urllib.parse.quote(site, safe="")
    for label, first, last in month_bounds(start, end):
        body = request_json(
            f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query",
            method="POST",
            headers=auth_header(token),
            body={
                "startDate": first.isoformat(),
                "endDate": last.isoformat(),
                "dimensions": ["page"],
                "type": "web",
                "rowLimit": 25000,
            },
        )
        clicks = 0
        for row in body.get("rows", []):
            path = page_path(row["keys"][0])
            if path not in paths:
                continue
            row_clicks = int(row.get("clicks") or 0)
            impressions = float(row.get("impressions") or 0)
            position = float(row.get("position") or 0)
            clicks += row_clicks
            page = pages.setdefault(path, {"clicks": 0, "impressions": 0, "position_weight": 0})
            page["clicks"] += row_clicks
            page["impressions"] += impressions
            page["position_weight"] += position * impressions
        monthly[label] = clicks
    return monthly, pages


def pull_analytics(token: str, property_id: str, start: date, end: date, paths: dict[str, str]) -> tuple[dict[str, int], dict[str, int]]:
    body = request_json(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport",
        method="POST",
        headers=auth_header(token),
        body={
            "dateRanges": [{"startDate": start.isoformat(), "endDate": end.isoformat()}],
            "dimensions": [{"name": "yearMonth"}, {"name": "landingPage"}],
            "metrics": [{"name": "sessions"}],
            "limit": 100000,
        },
    )
    monthly: dict[str, int] = {}
    pages: dict[str, int] = {}
    for row in body.get("rows", []):
        year_month = row["dimensionValues"][0]["value"]
        label = f"{year_month[:4]}-{year_month[4:]}"
        path = page_path(row["dimensionValues"][1]["value"])
        if path not in paths:
            continue
        sessions = int(float(row["metricValues"][0]["value"]))
        monthly[label] = monthly.get(label, 0) + sessions
        pages[path] = pages.get(path, 0) + sessions
    return monthly, pages


def write_traffic(brand: str, site: str, property_id: str, start: date, end: date, gsc_months: dict[str, int], ga_months: dict[str, int], gsc_pages: dict[str, dict[str, float]], ga_pages: dict[str, int], paths: dict[str, str]) -> None:
    current = json.loads(TRAFFIC_PATH.read_text(encoding="utf-8")) if TRAFFIC_PATH.exists() else {"brands": {}}
    pages = []
    for path, url in sorted(paths.items(), key=lambda item: item[1]):
        gsc = gsc_pages.get(path, {"clicks": 0, "impressions": 0, "position_weight": 0})
        impressions = gsc["impressions"]
        pages.append({
            "url": url,
            "gsc_clicks": int(gsc["clicks"]),
            "gsc_position": round(gsc["position_weight"] / impressions, 2) if impressions else None,
            "ga_landing_sessions": int(ga_pages.get(path, 0)),
        })
    current["generated_at"] = datetime.now(SAO_PAULO).isoformat(timespec="seconds")
    current["brands"][brand] = {
        "site_url": site,
        "property_id": property_id,
        "months": [
            {
                "month": label,
                "gsc_clicks": int(gsc_months.get(label, 0)),
                "ga_landing_sessions": int(ga_months.get(label, 0)),
            }
            for label, _first, _last in month_bounds(start, end)
        ],
        "pages": pages,
    }
    TRAFFIC_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")


def pull(brand: str, site: str | None, property_id: str | None, start: date) -> None:
    token = access_token()
    if not site or not property_id:
        show_accounts(token)
        raise SystemExit("Rode de novo com --site e --property copiados da lista acima.")
    end = datetime.now(SAO_PAULO).date()
    paths = article_paths(brand)
    gsc_months, gsc_pages = pull_search_console(token, site, start, end, paths)
    ga_months, ga_pages = pull_analytics(token, property_id, start, end, paths)
    write_traffic(brand, site, property_id, start, end, gsc_months, ga_months, gsc_pages, ga_pages, paths)
    print(f"Tráfego de {brand} salvo em {TRAFFIC_PATH.name}. O painel ainda usa a projeção até o próximo passo.")


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Worker Google do Keep")
    parser.add_argument("command", choices=["connect", "pull"])
    parser.add_argument("--brand", choices=["adfert", "intrivia"])
    parser.add_argument("--site", help="URL da propriedade no Search Console, como sc-domain:adfert.com.br")
    parser.add_argument("--property", help="ID numérico da propriedade GA4")
    parser.add_argument("--from", dest="start", type=parse_date, default=date(2025, 4, 1))
    args = parser.parse_args()
    if args.command == "connect":
        connect()
        return
    if not args.brand:
        raise SystemExit("pull precisa de --brand adfert ou --brand intrivia")
    pull(args.brand, args.site, args.property, args.start)


if __name__ == "__main__":
    main()
