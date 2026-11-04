---
name: answer-memory
description: Set up a private resume-backed profile, manage confirmed reusable application answers, and export the local application log.
---

Use one shared local directory across both hosts, `~/.tech-job-apply` by default. A user may set `TECH_JOB_APPLY_HOME` to an absolute path on the same local machine. Use private permissions (0700 directory, 0600 files). Never store this data in the plugin or project repo. Do not save passwords, tokens, one-time codes, or session data.

1. Ask for a resume file and read only that file. Draft profile.json with the resume's local path, identity/contact details, education and experience supported by the resume, and user-provided links. Show the draft and ask the user to confirm or correct it before reuse. If the resume changes, review changed fields and invalidate affected reusable answers.
2. Maintain answers.json as a list of records with `question`, `answer`, `scope` (country, employer, role or other relevant context), `status` (draft or confirmed), `source`, and `confirmed_at`. Keep phrasing and polarity, particularly for authorization and sponsorship. Confirm each answer in scope before automatic reuse. Store inferred values as drafts only with user consent. Do not generalize company-specific answers. Let the user review, update, or delete records. Sensitive self-identification is opt-in and user-directed.
3. Keep discovery observations in leads.json keyed by stable identity with provider aliases. Keep preferences in preferences.json. Write JSON with a private temporary file and atomic replacement, and avoid concurrent edits by coordinating with the other session.
4. Application state and event history live in the helper's SQLite database. Use [the bundled helper](scripts/store.py) for transitions and export. Run `python3 /path/to/store.py export jsonl` for the append-ordered event log or `export csv` for a current-state table. Redirect exports only to a private location using a restrictive umask. Include no application answers in the log.
