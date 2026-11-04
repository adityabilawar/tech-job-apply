# Tech Job Apply

Discover US tech internships and new-grad roles, prepare one application at a time, with review-first or opt-in automatic submission. Supported hosts use the same four [Agent Skills](https://agentskills.io/specification) and local application history.

## Install

Install from GitHub using the commands below. For local development, use the absolute path to this checkout in place of the GitHub repository name.

**Codex**

```sh
codex plugin marketplace add adityabilawar/tech-job-apply
codex plugin add tech-job-apply@tech-job-apply-local
```

You can also install **Tech Job Apply** from the marketplace in the Codex desktop Plugins directory. Start a new chat after installing. [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins)

**Claude Code**

In Claude Code, run:

```text
/plugin marketplace add adityabilawar/tech-job-apply
/plugin install tech-job-apply@tech-job-apply-local
```

Reload plugins with `/reload-plugins`. [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

**Grok Build**

Grok Build reads Claude Code marketplaces and plugins. From a clone of this repository, you can also load the shared package directly:

```sh
grok --plugin-dir ./plugins/tech-job-apply
```

Open `/plugins` to check that the plugin is loaded. [Grok Build plugin docs](https://docs.x.ai/build/features/skills-plugins-marketplaces)

**Grok Bot**

[Import the public Tech Job Apply Bot template](https://x.ai/bot/M43kZu1K1a7AYgLpDSH2E) to start with the four workflows and an onboarding skill. To add the workflows to an existing Bot, give your Bot the public repository link and ask it to read the four skill files under `plugins/tech-job-apply/skills`. Start by asking it to test free, read-only discovery and save the workflow as a private skill. Application filling requires an authorized browser plus access to Python and the same private storage as your other appliers. If the Bot cannot access that shared storage, use it for discovery only. [Grok Bot private skills](https://docs.x.ai/grok-bot/skills-routines-and-automations)

## Set up and use

1. Ask to use **answer-memory** with the path to your resume. Confirm the extracted profile and add reusable answers you want the plugin to use. Defaults are yours to configure.
2. Ask to use **job-preferences**. For example, “Find SWE and ML internships in the US, prioritize NYC, and exclude Example Corp.”
3. Ask **job-discover** to find openings. Public GitHub lists work without an Apify account. For Apify, provide `APIFY_TOKEN` through your environment and authorize a spending limit in USD. The skill checks live pricing and caps before each paid run.
4. Give **job-apply** a lead or official job URL. For example, “Prepare the Example Corp ML internship application and show me the review.” Use a session with an authorized browser surface and Python 3. Discovery and preference editing can run without browser automation. Both hosts must use the same local storage path to share claims.
5. Ask **answer-memory** to export the application event history as JSONL or current state as CSV. CSV opens in spreadsheet apps.

Your profile, preferences, and log stay in `~/.tech-job-apply` by default. Keep this folder private and outside the checkout. The application helper stores stages and events transactionally and exports JSONL on demand. A claim remains active across pauses and restarts. After an interruption, verify the previous applier has stopped before recovering its claim. An interrupted final click must be reconciled in the portal before closing the claim.

## What this does not do

- Unsupervised mass submission or automatic retries of ambiguous submissions.
- Captcha solving or coding tests without explicit approval.
- Inventing experience, qualifications, or application answers.

## Submission modes

**Review-first remains the default.** To opt in to automatic submission, authorize an exact job or fixed shortlist for the current run and confirm the resume and attachments. For example:

> Automatically submit the applications at these two official URLs in this run using my confirmed resume and saved answers. Pause if anything needs my input.

The plugin pauses for inferred answers, new consent, and required handoffs. An ambiguous result stops the run without retrying. No applications were submitted as part of this update.

### Updating

Refresh the marketplace and reload the plugin in your host. For Grok Build's direct-load method, pull the latest checkout and restart Grok Build. For Grok Bot, refresh existing private skills from this repository and keep automatic submission disabled until a user explicitly authorizes a run.
