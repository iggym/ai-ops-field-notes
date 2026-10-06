# AI Ops Field Notes: Improvement Tasks

Repo audit date: 2026-10-06. Last updated: 2026-10-06 (all P0 items done; see the **Progress log** at the bottom). Priorities: **P0** = broken or incorrect today, **P1** = high-value improvement, **P2** = nice to have.

---

## P0: Bugs and correctness

- [x] **Duplicate article: `the-model-was-fine.html` is a byte-for-byte copy of `green-alerts-silent-rag.html`.**
  Its `<title>` and body are "Green alerts, silent RAG". The metadata entry for "The model was fine" (id `1203`, hook "…by someone who wasn't in the incident channel", tags `false-positive`, `feature-flag`) points to the wrong content. Write or restore the real feature-flag false-positive dispatch with `docs/master-prompt-v1.md`, or set its status to `draft` until then.
  - ✅ Rewrote it as a real feature-flag false-positive dispatch in the house template, using the master prompt.
- [x] **Leftover citation tokens in `the-4200-weekend.html`** (line ~440): `[citation:7][citation:12]` shows on the live page. Replace them with a plain-words source disclosure.
  - ✅ Replaced with a composite disclosure. Also fixed the page `<title>`, which was "$4,200 Weekend" instead of "The $4,200 Weekend".
- [x] **README references a missing asset:** `./assets/narrative-diagram.svg` does not exist, so the image is broken on GitHub. Create the SVG or remove the `<img>`.
  - ✅ Removed the `<img>`. The Mermaid diagram already covers it.
- [x] **README is truncated:** the ```` ```mermaid ```` block is never closed and the file ends after the flowchart. Close the fence and finish the README (see P1 README task).
  - ✅ Closed the fence and added sections on what the repo is, the layout, how to add a dispatch, and the metadata schema.
- [x] **`metadata.json` inconsistencies:**
  - [x] The "When Green Means Dead" entry is missing `id`, `slug`, `format`, and `research_window`. ✅ Added `id` `0105`, the slug, the format, and the research window from its own footer.
  - [x] `the-4200-weekend` uses `"through"` in `research_window`. Every other entry uses `"to"`.
  - [x] Tag variants are inconsistent: `circuit-breaker` and `circuit-breakers`; `agentic-ai`, `agentic-loops`, and `agentic-failure`; `observability`, `llm-observability`, and `observability-gap`. Pick canonical tags. ✅ Canonical tags are now `circuit-breakers`, `agentic-failure` and `llm-observability`.
  - [x] `reading_time_minutes` doesn't match the pages. `the-message-that-never-sent` says 3 in metadata and "6 min" on the page, and `when-green-means-dead` is about 1,100 words but listed as 5. Recompute as `ceil(words/200)`. ✅ Set to 4 and 6, and the page label now says 4 min.
  - [x] Formatting is irregular (mixed indentation, `}, {` vs `},{`). Reformat with 2-space JSON. ✅ Done. Also sorted newest first, used one key order everywhere, and added `source_type` to every entry.
- [x] **Homepage XSS-style injection risk:** `index.html` interpolates `title`, `hook`, and `path` from metadata into `innerHTML` without escaping. The risk is low because metadata is first-party, but a stray `<` or `&` in a hook will break rendering. Add an `escapeHTML()` helper. ✅ Added `esc()` and applied it to every interpolated field.
- [x] **Homepage date sorting** uses `new Date(b.date)`. That's fine for ISO dates, but `fmtTs` builds `new Date(iso+'T00:00:00')` in local time and then calls `toISOString()` (UTC), which can shift the displayed date by one day for users east of UTC. Format the date string directly instead. ✅ Done. Sorting now compares the ISO strings.
- [x] **Remove the stray Node.js `.gitignore` boilerplate.** It's harmless but misleading for a static site. Trim it to OS/editor files. ✅ Done.

- [x] **Leftover `{{DATE}} =` template placeholder** in `when-green-means-dead.html` (kicker and footer). Found during the P0 work. ✅ Removed.

## P1: Site consistency and design system

- [ ] **Unify article templates.** The 11 articles use at least 5 different designs:
  - IBM Plex Serif/Mono on `#09090b` (green-alerts, two-incidents, model-was-fine)
  - Fira Code + Inter on `#0d1117` (commit-that-never-happened, green-dashboard, loop-that-ate-the-key)
  - Inter on `#0f1115` (eleven-day-retry-loop, ghost-in-the-vector-space)
  - Newsreader on a **light** `#fafaf8` background (message-that-never-sent)
  - Inter only (4200-weekend); custom (when-green-means-dead)

  Adopt the house template defined in `docs/master-prompt-v1.md` and migrate the older articles to it, keeping each interactive moment.
  - Progress: 9 of 17 articles now use the house template (the 7 generated on 2026-10-06, plus `two-incidents-one-revert` and `green-alerts-silent-rag`). Still to migrate: `the-4200-weekend`, `the-commit-that-never-happened`, `the-green-dashboard-that-lied`, `the-loop-that-ate-the-key`, `the-eleven-day-retry-loop`, `the-ghost-in-the-vector-space`, `the-message-that-never-sent`, `when-green-means-dead`.
- [ ] **Extract shared CSS/JS** into `assets/css/dispatch.css` and `assets/js/dispatch.js` (progress bar, share buttons, hamburger). Each article currently inlines about 8–15 KB of duplicated styles.
- [ ] **Match the homepage and article branding.** The homepage uses amber `#FFB020` and red `#FF4433` with a terminal aesthetic, while the articles use red `#ef4444`. Choose one accent palette.
- [ ] **Consistent footer disclosure** on every article, matching the master prompt templates and recorded in metadata as `source_type`.
- [ ] **Article navigation:** add "← previous / next →" links and a "more dispatches" block at the bottom of each article.
- [ ] **Rewrite the README** to describe what the repo actually is: the site, how to add a dispatch (link to `docs/master-prompt-v1.md`), the metadata schema, local preview (`python3 -m http.server`), and a dispatch index table.

## P1: SEO, sharing, and discoverability

- [ ] **Add Open Graph/Twitter meta tags to every article.** (Progress: the 7 articles generated on 2026-10-06 have OG/Twitter, description, canonical and JSON-LD tags. The 10 older ones still need them.) None have them today, so shared links on X and LinkedIn render without a title card. That works against a top-of-funnel site.
- [ ] Add `<meta name="description">` and `<link rel="canonical">` to every article (only `when-green-means-dead` has a description).
- [ ] **Social preview images:** generate one 1200×630 OG image per article (title + hook on the house background) in `assets/og/<slug>.png`.
- [ ] **RSS/Atom feed** (`feed.xml`) generated from `metadata.json`, linked from the homepage `<head>`.
- [ ] **`sitemap.xml` and `robots.txt`.**
- [ ] **Add OG/meta tags and a favicon to the homepage.** The homepage has none.
- [ ] **Render the homepage without JavaScript.** The feed is built client-side from `metadata.json`, so crawlers and no-JS readers see "loading…". Pre-render the list into `index.html` at build time, or add a `<noscript>` list.
- [ ] Add JSON-LD `Article` structured data to each article.

## P1: Automation and quality gates

- [ ] **Add a build script** (Progress: `scripts/validate.py` covers the validation half: required keys, unique id/slug, slug/path/file match, `<title>` vs. metadata, duplicate files, leftover `[citation:N]`/`{{PLACEHOLDER}}`/TODO, and orphan article files. Still to do: generate the feed, sitemap and pre-rendered homepage.) (`scripts/build.py` or Node) that, from `metadata.json`:
  - validates the schema (required keys, unique `id` and `slug`, slug == filename, path exists),
  - checks that each article's `<title>`/`<h1>` matches its metadata title (this catches the duplicate-file bug),
  - fails on `[citation:` tokens and on `TODO` or `{{` placeholders,
  - generates `feed.xml`, `sitemap.xml`, and the pre-rendered homepage list.
- [ ] **Add a GitHub Actions workflow** that runs the validator on every PR, plus an HTML validator (`html-validate`) and a link checker (`lychee`).
- [ ] **Add a `metadata.schema.json`** (JSON Schema) for editor autocompletion and CI validation.
- [ ] **Add a PR template** (`.github/pull_request_template.md`) with the new-dispatch checklist from the master prompt.
- [ ] **Accessibility audit:** run Lighthouse/axe on each article. Check contrast of `--text-dim #71717a` on `#09090b` (about 4.1:1, which is below AA for small text), focus states, `aria-live` on widgets, and reduced motion. `the-4200-weekend` autostarts its counter after 4s.

## P2: Content and editorial

- [ ] **Topic tagging and filtering on the homepage:** show tags on each entry and add a filter bar (cost, retries, RAG, drift, rollback).
- [ ] **Pinned/SEV-1 entry:** nothing is pinned. Pin the strongest piece (for example "When Green Means Dead") as the entry point.
- [x] ~~**Fill coverage gaps** listed in the master prompt:~~ ✅ Six new dispatches (see the progress log). The master prompt's under-covered list has been refreshed with the next set of gaps. prompt injection reaching tools, PII in traces, guardrail false negatives, eval contamination, LLM-judge drift, context truncation, fallback-chain quality decay, and stale prompt caches.
- [ ] **Cross-link to the rest of the portfolio.** The footer mentions "an eight-repo portfolio", but there are no links to the sibling repos. Add a "Go deeper" link per tag that points to the relevant playbook repo.
- [ ] **Publishing cadence:** dates range from 2024-12 to 2026-06 with gaps. Keep `research_window`-driven publishing, aiming for one or two a month, and track it in a `docs/editorial-calendar.md`.
- [ ] **Version the master prompt:** record what changed in each `master-prompt-vN.md` revision, and store the generation inputs per article (topic, sources) in `docs/sources/<slug>.md` for traceability.
- [ ] **Light theme or `prefers-color-scheme` support** for the homepage and articles. Only one article currently uses a light theme.
- [ ] **Privacy-friendly analytics** (for example Plausible or GoatCounter) to see which dispatches convert. That matters for a top-of-funnel site.
- [ ] Add a **custom 404 page** in the house style.

---

## Progress log

### 2026-10-06: P0 sweep and six new dispatches
- Fixed every P0 item above. The new `scripts/validate.py` now passes: 17 articles, 0 errors.
- Rewrote `the-model-was-fine` (id `1203`) so it matches its metadata.
- Generated six new dispatches with `docs/master-prompt-v1.md`, all composites in the house template with OG/canonical/JSON-LD tags and one interactive moment each:
  | id | slug | topic |
  |---|---|---|
  | 0714 | `the-invoice-that-gave-orders` | Indirect prompt injection through hidden PDF text reaching a payee-update tool |
  | 0804 | `the-trace-that-kept-everything` | PII sent verbatim to a tracing vendor, bypassing log redaction |
  | 0819 | `the-contract-ended-at-page-41` | Silent context-window truncation in contract review |
  | 0902 | `the-fallback-nobody-noticed` | Rate-limit fallback to a smaller model counted as success |
  | 0916 | `the-cache-that-answered-last-quarter` | Semantic cache serving answers from a superseded policy |
  | 0929 | `the-parser-said-low-risk` | Fail-open structured-output parser default in fraud scoring |
- **Next up (highest remaining priority):** the P1 template migration for the 8 older articles, OG tags for those pages, and a CI workflow that runs `scripts/validate.py` on every PR.
