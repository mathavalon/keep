import { FormEvent, useEffect, useState } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "@/integrations/supabase/client";

type Gate = "setup" | "login" | "confirm" | "ready";

export default function App() {
  const [gate, setGate] = useState<Gate>(supabase ? "login" : "setup");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => {
      void openSession(data.session);
    });
    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      void openSession(session);
    });
    return () => data.subscription.unsubscribe();
  }, []);

  async function openSession(session: Session | null) {
    if (!supabase || !session) {
      setGate("login");
      return;
    }
    if (!session.user.email_confirmed_at) {
      setGate("confirm");
      return;
    }
    const { error } = await supabase.rpc("keep_mark_email_ok");
    if (error) {
      setMessage(error.message);
      setGate("confirm");
      return;
    }
    setGate("ready");
  }

  async function submit(event: FormEvent | { preventDefault(): void }, mode: "sign-in" | "sign-up") {
    event.preventDefault();
    if (!supabase) return;
    setBusy(true);
    setMessage("");
    const credentials = { email, password };
    const result =
      mode === "sign-up"
        ? await supabase.auth.signUp(credentials)
        : await supabase.auth.signInWithPassword(credentials);
    setBusy(false);
    if (result.error) {
      setMessage(result.error.message);
      return;
    }
    if (mode === "sign-up") {
      setGate("confirm");
      setMessage("Enviamos o link de confirmação para o seu e-mail.");
    }
  }

  if (gate === "ready") {
    return <iframe title="Painel Keep" src="/painel.html" className="panel" />;
  }

  return (
    <main className="gate">
      <p className="brand">keep</p>
      {gate === "setup" && (
        <p>Este projeto ainda não tem o banco dele. Crie um projeto novo no Lovable a partir deste repositório. Não use o projeto da Avalon.</p>
      )}
      {gate === "confirm" && (
        <p>Confirme o e-mail para entrar. A membership só fica OK depois dessa confirmação.</p>
      )}
      {gate === "login" && (
        <form onSubmit={(event) => submit(event, "sign-in")}>
          <label>
            E-mail
            <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label>
            Senha
            <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required minLength={6} />
          </label>
          <div className="actions">
            <button type="submit" disabled={busy}>Entrar</button>
            <button type="button" disabled={busy} onClick={(event) => submit(event, "sign-up")}>Criar conta</button>
          </div>
        </form>
      )}
      {message && <p className="message">{message}</p>}
    </main>
  );
}
