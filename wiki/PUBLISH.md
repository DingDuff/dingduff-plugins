# How to publish this wiki

These files are the **source** for the GitHub wiki on `DingDuff/dingduff-public`
(repo renamed 2026-06-24 from `dingduff-plugins`; the local source folder is
still `~/Desktop/DingDuff/dingduff-plugins/` — only the GitHub repo name changed).
A GitHub wiki is a **separate git repo** (`<repo>.wiki.git`), so you push these
pages there — not into the code repo.

> Note: this `PUBLISH.md` and the `<!-- INSTRUCTIONS FOR CLAUDE -->` comments are
> fine to keep. `PUBLISH.md` is just a notes file; if you don't want it to appear
> as a wiki page, don't copy it over in the steps below. The HTML comments are
> invisible when rendered but readable by Claude.

## One-time setup

1. On GitHub, open **github.com/DingDuff/dingduff-public → Settings → Features**
   and make sure **Wikis** is enabled.
2. Open the **Wiki** tab and click **Create the first page** (any content). Save
   it once. This creates the underlying `dingduff-public.wiki.git` repo so you
   can clone it.

## Publish (copy these commands)

```bash
# From a working directory of your choice:
git clone https://github.com/DingDuff/dingduff-public.wiki.git
cd dingduff-public.wiki

# Copy the wiki pages in (adjust the source path if needed):
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/Home.md .
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/Browser-Setup.md .
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/Team-and-Enterprise.md .
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/Troubleshooting.md .
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/Skills.md .
cp /Users/kyle/Desktop/DingDuff/dingduff-plugins/wiki/_Sidebar.md .

git add .
git commit -m "Add DingDuff install & troubleshooting wiki"
git push origin master   # GitHub wikis use the 'master' branch
```

After pushing, your pages live at:

- `https://github.com/DingDuff/dingduff-public/wiki` (Home)
- `https://github.com/DingDuff/dingduff-public/wiki/Browser-Setup`
- `https://github.com/DingDuff/dingduff-public/wiki/Troubleshooting`
- etc.

The **link to put on your website** is the Home URL:
`https://github.com/DingDuff/dingduff-public/wiki`

## Updating later

Edit the files in `dingduff-plugins/wiki/`, copy them into your cloned
`dingduff-public.wiki` checkout again, then `git add . && git commit && git push`.

---

## Optional: the one-sentence website change

This lives in a **different repo** (`dingduff-mcp`), so it's separate from
publishing the wiki — apply it whenever you're ready.

In `dingduff-mcp/dingduff/templates/landing.html`, the setup accordion is the
block `<div class="setup-acc"> ... </div>` (around lines 207–375). You can replace
that block with a single sentence pointing at the wiki, e.g.:

```html
<p class="get-dingduff-intro">
  To install, point Claude at our wiki and ask it to walk you through
  installation:
  <a href="https://github.com/DingDuff/dingduff-public/wiki"
     target="_blank" rel="noopener noreferrer">DingDuff install &amp; help wiki</a>.
</p>
```

Keep the surrounding `#get-dingduff` section heading and the "How DingDuff
works" / pricing cards (the `<div class="byok-explainer">` block — legacy class
name, content is generic — and the `#cost` section) — those aren't part of the
step-by-step instructions and are still useful on the page.
