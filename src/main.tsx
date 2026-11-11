import type { Session } from "@supabase/supabase-js";
import { supabase } from "@/integrations/supabase/client";

type Credentials = { email: string; password: string };
type Lead = { name: string; email: string; site: string };
type AuthResult = { error?: string; confirm?: string };

declare global {
  interface Window {
    KeepAuth: {
      session: Session | null;
      preview: boolean;
      sign: (mode: string, credentials: Credentials) => Promise<AuthResult>;
      saveLead: (lead: Lead) => Promise<AuthResult>;
      signOut: () => Promise<void>;
    };
    KeepUI: { route: () => void; go: (path: string) => void };
  }
}

const missing = "O banco deste projeto ainda não está conectado.";

window.KeepAuth = {
  session: null,
  preview: !supabase,
  async sign(mode, credentials) {
    if (!supabase) return { error: missing };
    if (mode === "sign-up") {
      const { error } = await supabase.auth.signUp({
        email: credentials.email,
        password: credentials.password,
        options: { emailRedirectTo: `${location.origin}/login` },
      });
      if (error) return { error: error.message };
      return { confirm: "Enviamos o link de confirmação para o seu e-mail." };
    }
    const { data, error } = await supabase.auth.signInWithPassword(credentials);
    if (error) return { error: error.message };
    window.KeepAuth.session = data.session;
    if (!data.user?.email_confirmed_at) {
      return { confirm: "Confirme o e-mail para abrir o painel." };
    }
    const marked = await supabase.rpc("keep_mark_email_ok");
    if (marked.error) return { error: marked.error.message };
    return {};
  },
  async saveLead(lead) {
    if (!supabase) return { error: missing };
    const { error } = await supabase.from("keep_leads").insert({
      name: lead.name,
      email: lead.email,
      site: lead.site || null,
    });
    return error ? { error: error.message } : {};
  },
  async signOut() {
    if (supabase) await supabase.auth.signOut();
    window.KeepAuth.session = null;
    location.assign("/");
  },
};

async function start() {
  if (supabase) {
    const { data } = await supabase.auth.getSession();
    window.KeepAuth.session = data.session;
    supabase.auth.onAuthStateChange((_event, session) => {
      window.KeepAuth.session = session;
    });
  }
  window.KeepUI.route();
}

void start();
