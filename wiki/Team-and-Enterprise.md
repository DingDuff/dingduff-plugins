<!--
INSTRUCTIONS FOR CLAUDE
This page is for users on a work Claude account (Team or Enterprise). The common
blocker: on these plans only an organization Owner can add a custom connector,
and a user's role must allow it. If the user can't add DingDuff or doesn't see
"Add custom connector," help them identify whether it's an admin/org issue and
give them exact wording to send their admin. Also covers org-level network/code
settings that an admin may need to enable.
-->

# Team & Enterprise Plans

On **Team** and **Enterprise** Claude plans, individuals usually **cannot add a
custom connector themselves**. An organization **Owner** has to add DingDuff for
the whole organization first; after that, each member connects to it individually.

## How to tell this is your situation

Any of these usually means it's an admin/organization setting, not something you
did wrong:

- You open **Customize → Connectors → +** and there's **no "Add custom
  connector"** option.
- DingDuff doesn't appear in your connector list even though a colleague added it.
- You see a message that the connector isn't available for your organization or
  your role.

## What an Owner needs to do (send them this)

> Please add the DingDuff custom connector for our organization:
> 1. Go to **Organization settings → Connectors**.
> 2. Click **Add**, choose **Custom**, then **Web**.
> 3. Enter this server URL: `https://app.dingduff.com/mcp`
> 4. Click **Add**.
> 5. Make sure my role is allowed to use custom connectors (not "Blocked").

Once the Owner has done this, each member connects on their own:

1. **Customize → Connectors**.
2. Find **DingDuff** in the list and click **Connect**.
3. Sign in with your **DingDuff** email and password (from dingduff.com).

Then continue with [Install DingDuff → Step 3](Home) (allow the tools).

## If the connector connects but tools are blocked

On Enterprise plans, roles can allow a connector but restrict individual tools.
If some DingDuff tools are missing or always blocked, ask your admin to set
DingDuff's tools to **Always allow** (or at least "Ask") for your role, rather
than **Blocked**.

## Code execution & network access (for downloads and citation-check)

DingDuff's `opinion_store` / `statute_store` tools and the citation-check skill
need Claude's **code-execution environment with internet access** (see
[Browser Setup](Browser-Setup) for what this is). On Team/Enterprise plans this
is often controlled centrally. If downloads fail, ask your admin:

> Please enable code execution / file creation and **allow network egress** for
> our organization under **Organization settings → Capabilities**, so DingDuff
> can download legal sources and run citation checks.

Note: capability changes usually apply only to **new** chat sessions.

## Still stuck?

See [Troubleshooting](Troubleshooting), or email **hello@dingduff.com** with your
plan type (Team or Enterprise) and what you see on the Connectors screen.
