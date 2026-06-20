<!--
INSTRUCTIONS FOR CLAUDE
Match the user's symptom to one of the sections below and walk them through the
fix. Each entry is Symptom → Cause → Fix. The two most common real-world issues
are: (1) the opinion/statute store tools "not working" because network egress /
the code-execution environment is off, and (2) Team/Enterprise users who can't
add the connector because an admin must enable it. Confirm the fix worked before
moving on.
-->

# Troubleshooting

Find the symptom that matches, then follow the fix. If a connector or capability
change doesn't seem to take effect, **start a new chat** — many settings only
apply to new sessions.

---

## Opinion/statute store tools don't work (no files appear)

**Symptom:** You ask Claude to save cases or statutes with `opinion_store` or
`statute_store`. The tool seems to run, but no files show up and Claude can't
read them back.

**Cause:** These tools return **time-limited download links**. Claude has to fetch
those links using its **code-execution environment**, and that environment needs
**internet access**. If code execution or network access is turned off, the
download silently fails.

**Fix:**
1. Open **Settings → Capabilities**.
2. Turn on **Code execution and file creation** (the setting that lets Claude run
   code / create files).
3. Turn on **Allow network egress** (internet access for that environment).
4. **Start a new chat** — these usually take effect only on new sessions.
5. Retry the save.

> Labels may vary. If you don't see those exact names, look under **Settings →
> Capabilities** for code execution / sandbox / network access and enable them.
> On Team/Enterprise this may be an admin setting — see
> [Team & Enterprise](Team-and-Enterprise). More detail in
> [Browser Setup](Browser-Setup).

---

## You can't find "Add custom connector"

**Symptom:** Under **Customize → Connectors → +**, there's no "Add custom
connector" option, or DingDuff never shows up.

**Cause:** Either you're on a **Team/Enterprise** plan where only an Owner can add
connectors, or (on **Free**) you've hit the one-custom-connector limit.

**Fix:**
- **Team/Enterprise:** an Owner must add DingDuff first. See
  [Team & Enterprise](Team-and-Enterprise) for the exact steps to send them.
- **Free plan:** Free accounts allow only **one** custom connector. Remove an
  existing one, or upgrade to Pro/Max for more.

---

## The sign-in window doesn't open (OAuth/login)

**Symptom:** After clicking **Add**, no DingDuff sign-in page appears, or sign-in
never completes.

**Cause:** A popup blocker or privacy extension is blocking the login window, or
you don't yet have a DingDuff account.

**Fix:**
- Make sure you created a DingDuff account at **https://dingduff.com** first.
- Allow popups for Claude, and disable ad/privacy blockers for the sign-in.
- Try a different browser, then re-add the connector.
- Double-check the URL is exactly `https://app.dingduff.com/mcp`.

---

## DingDuff is connected, but Claude doesn't use it

**Symptom:** DingDuff is in your connector list, but Claude answers legal
questions without it, or says it has no DingDuff tools in this chat.

**Cause:** The connector isn't toggled on for that chat, or its tools aren't
permitted.

**Fix:**
- In the chat, click the **+** (tools) control and make sure **DingDuff** is
  toggled **on**.
- In **Customize → Connectors → DingDuff**, set the tools to **always allow**
  (checkmark, not the hand).
- Tell Claude explicitly: *"Use only the DingDuff database for this."* Adding a
  custom instruction (see [Skills & Settings](Skills)) makes this automatic.

---

## It worked yesterday, now it asks me to sign in again

**Symptom:** DingDuff stops responding and you're prompted to reconnect.

**Cause:** Sign-in sessions expire periodically (about an hour of token validity),
which is normal.

**Fix:** Reconnect via **Customize → Connectors → DingDuff → Connect** and sign in
again. If it keeps happening immediately, remove and re-add the connector.

---

## The citation-check skill won't run

**Symptom:** `dingduff-citation-check` errors, can't find sources, or can't run.

**Cause:** It needs (a) `python3` available in the session and (b) your source
files saved locally first via `opinion_store` / `statute_store`.

**Fix:**
- Use **Cowork (desktop)** or **Claude Code**, which provide `python3`. In a plain
  browser chat, enable the code-execution environment ([Browser Setup](Browser-Setup)).
- First save the cited opinions/statutes with the store tools (which need network
  access — see the first entry above), then run the cite-check.
- See [Skills & Settings](Skills) for install steps.

---

## Still stuck

Email **hello@dingduff.com**. It helps to include: your plan (Free/Pro/Max/Team/
Enterprise), whether you're on the desktop app or a browser, the tool or step that
failed, and any error text Claude showed.
