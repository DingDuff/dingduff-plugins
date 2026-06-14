<!--
INSTRUCTIONS FOR CLAUDE (read this first)

You are helping a lawyer install and run DingDuff, a legal-research connector for
Claude. The user is probably not technical. Be patient, do one step at a time,
and confirm each step worked before moving to the next.

Do this:
1. Ask which environment they use:
   - The Claude desktop app (Mac/Windows) — RECOMMENDED, especially Cowork mode.
   - A web browser at claude.ai / claude.com.
   - The mobile app — connecting works, but downloads/cite-check don't; see the
     "Using DingDuff on mobile" section and steer them to desktop/browser for full
     features.
2. Ask whether their Claude account is personal (Free / Pro / Max) or a work
   account on a Team or Enterprise plan. This changes who can add the connector.
3. Walk them through "Install DingDuff" on this page, step by step.
4. Branch as needed:
   - Browser user → also read the [Browser Setup](Browser-Setup) page.
   - On a Team/Enterprise plan and they can't add the connector, or the option is
     missing → read [Team & Enterprise](Team-and-Enterprise).
   - A tool fails or behaves oddly → read [Troubleshooting](Troubleshooting) and
     match the symptom.
   - They want the optional skills and best-practice settings → read [Skills & Settings](Skills).
5. The connector URL the user must paste is exactly: https://app.dingduff.com/mcp

Verify success at the end in two parts: (a) connector connected — ask the user to
have Claude confirm it can see the `opinion_search` tool (works without an API
key); (b) API key applied — confirm the `opinion_extract` tool is present (only
appears after Step 4's BYOK key). If `opinion_extract` is missing, that's the API
key, not a broken install.
-->

# DingDuff Installation & Help

DingDuff is a **legal-research connector for Claude**. It links your own Claude
account to a database of millions of court opinions, federal and state statutes
and rules, and federal court filings (PACER) — so you can do real legal research
right inside Claude, with citations.

This wiki is written so you can either **read it yourself** or **point Claude at
it** and ask Claude to walk you through everything. The easiest path:

> Open Claude, paste the link to this page, and say:
> *"Walk me through installing DingDuff, one step at a time."*

## Pages in this wiki

- **Install DingDuff** (this page) — the main setup, start to finish.
- [Browser Setup](Browser-Setup) — extra steps if you use Claude in a web browser instead of the desktop app.
- [Team & Enterprise](Team-and-Enterprise) — what to do if you're on a work plan and can't add the connector.
- [Troubleshooting](Troubleshooting) — fixes for common problems (a tool isn't working, you can't sign in, etc.).
- [Skills & Settings](Skills) — optional add-ons that make DingDuff noticeably better.
- [How Citation Checking Works](Citation-Checking) — what the cite-checker does, and the design behind its reliability and privacy.

---

## Before you start

DingDuff itself is **free while in beta**. To use it you need three things:

1. **Your own Claude account** — a paid plan (Pro, Max, Team, or Enterprise) is
   recommended. The Claude **desktop app** with **Cowork** mode is the best
   experience; a web browser also works (see [Browser Setup](Browser-Setup)).
   (The Free plan technically works but allows only **one** custom connector.)
2. **A DingDuff login** — sign up at **https://dingduff.com** to create your
   account. This gives you the email + password you'll use when connecting.
   DingDuff is for **licensed attorneys** (per the Terms of Service).
3. **Your own Anthropic API key (BYOK)** — needed to unlock two of the tools.
   You add this *after* connecting (Step 4 below). Typical cost is ~$5–10/month,
   paid to Anthropic, not to DingDuff.

> If you haven't created a DingDuff account yet, do that first at
> https://dingduff.com (click **Sign Up**). You'll need that email and password
> during Step 2.

---

## Install DingDuff

These steps are for the **Claude desktop app** (recommended). If you're in a
browser, do these same steps and then read [Browser Setup](Browser-Setup) for the
one extra setting browsers need.

### Step 1 — Open the connector settings

1. In Claude, open **Customize** from the left sidebar.
2. Go to **Connectors**.
3. Click the **+** button, then choose **Add custom connector**.

> On a **Team or Enterprise** plan, you may not see "Add custom connector" —
> only an organization owner can add it. If so, go to
> [Team & Enterprise](Team-and-Enterprise).

### Step 2 — Add DingDuff

1. In the dialog, give it a name (e.g., `DingDuff`).
2. In the URL field, paste exactly:

   ```
   https://app.dingduff.com/mcp
   ```

3. Click **Add**.
4. Claude will send you to the **DingDuff sign-in page**. Enter the **email and
   password** for the DingDuff account you created at dingduff.com, then approve
   the connection. You'll be returned to Claude automatically.

> A small browser/login window normally opens for sign-in. If nothing appears,
> see "Sign-in window doesn't open" in [Troubleshooting](Troubleshooting).

### Step 3 — Allow DingDuff's tools

After connecting, DingDuff appears in your connector list with its tools. We
recommend setting each tool to **always allow** (the **checkmark**, not the
hand icon) so you aren't asked for permission on every research request.

### Step 4 — Add your Anthropic API key (unlocks the last two tools)

Everything works at this point **except** two tools — `opinion_extract` and
`submit_batch_screen` — which stay locked until you add your own Anthropic API
key. To set it up:

1. Open a new chat and confirm DingDuff is connected.
2. Ask Claude: *"Help me get an Anthropic API key so I can add it to DingDuff."*
   Claude will point you to the **Claude Console** (console.anthropic.com).
3. In the Console, add a payment method, **create an API key**, and copy it.
4. Log in to your **profile on dingduff.com** and paste the key into the field
   provided.

**Two safety rules (required by our Terms):**
- Use a **dedicated key** for DingDuff only — so you can revoke it without
  affecting anything else.
- **Turn off auto-reload** on that key, so any exposure stays capped.

### Step 5 — Confirm it works

First confirm the connector is live. In a chat, ask Claude:

> *"Does the DingDuff connector have the `opinion_search` tool?"*

If yes, the connector is working. Then confirm your **API key** (Step 4) took
effect:

> *"Does the DingDuff connector have the `opinion_extract` tool?"*

`opinion_extract` and `submit_batch_screen` only appear **after** you add your API
key — if they're missing, go back to Step 4. Everything else works without a key.

Now try a real query, e.g.:

> *"Using only DingDuff, find recent Texas appellate cases on the economic loss
> rule and give me citations."*

---

## Recommended settings (optional but worth it)

These take a few minutes and noticeably improve results. Full details on
[Skills & Settings](Skills):

- **Install the research skills** (`dingduff-case-law-research-standard` is the
  best default) — they improve the quality of research answers.
- **Install the `dingduff-citation-check` skill** — verifies every citation in a
  drafted memo against the stored sources.
- **Add a custom instruction** (Profile → *Instructions for Claude*) telling
  Claude to always use DingDuff for legal research, so you don't have to ask each
  time.
- **Turn off chat training** in your Claude privacy settings.

---

## Using DingDuff on mobile

You can add the DingDuff connector on the **Claude mobile apps** the same way
(Connectors → add the custom connector → sign in), and **research tools**
(searching and viewing cases, statutes, and PACER) work fine.

However, the features that need a working file environment — **saving sources**
(`opinion_store` / `statute_store`) and the **citation-check** skill — rely on the
desktop app or browser. For full functionality, use the **desktop app (Cowork)**
or a **browser**; treat mobile as read-and-research on the go.

## Quick fixes

- **A DingDuff "store" tool says it worked but no files appear** → you likely
  need to turn on network access for Claude's tools. See
  [Troubleshooting → Opinion/statute store tools don't work](Troubleshooting).
- **You can't find "Add custom connector"** → you may be on a Team/Enterprise
  plan; see [Team & Enterprise](Team-and-Enterprise).
- **`opinion_extract` is missing or fails** → you haven't added your API key yet;
  redo Step 4 above.

For everything else, see [Troubleshooting](Troubleshooting).
