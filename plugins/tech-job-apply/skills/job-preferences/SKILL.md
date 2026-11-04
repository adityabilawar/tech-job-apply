---
name: job-preferences
description: Set or revise search titles, locations, NYC priority, remote preferences, salary floor, and job or company exclusions.
---

Use the shared local directory defined in answer-memory. Read preferences.json before proposing updates. Ask in one pass for any missing choices needed for the current search. Save confirmed changes atomically and preserve other settings.

Use these keys: `role_families`, `include_titles`, `exclude_titles`, `levels`, `country`, `locations`, `nyc_priority`, `remote_policy` (allow, require, exclude), `salary_floor` (amount, currency, period, and whether unknown pay is eligible), `excluded_companies`, and `skipped_jobs` (stable IDs or canonical URLs, with optional reasons). Missing keys use US, internships and new grad, SWE/AI/ML/FDE/quant, any US location, NYC priority off, remote allowed, and no salary floor or exclusions.

Distinguish strict filters from rank preferences. Compare base compensation in like currency and period only. Flag unknown or incomparable pay, and honor the user's policy for it. Record specific skips against stable identities and aliases. Ask before generalizing a skip to an employer or job family. A skip request for an active application must go through job-apply so it releases the claim safely.
