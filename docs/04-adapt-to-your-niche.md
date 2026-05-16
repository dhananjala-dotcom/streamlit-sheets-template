# 04 · Adapt this template to your own use case

The demo collects workshop feedback. To repurpose it for anything else — RSVPs, reading log, habit tracker, inventory — you change the schema in **three places**.

## The three places to edit

1. **The Google Sheet header row.** Pick your columns. For a reading log it might be:
   ```
   timestamp | book | pages_read | mood | notes
   ```
2. **The form in `app.py`** for the step you're working on (`step1-mock/app.py`, `collect/app.py`, etc.). Replace the form widgets to match your columns. Update the `append_row([...])` list so the order lines up with your header row.
3. **The display in the dashboard or admin app.** Update the column references in `st.metric`, `st.bar_chart`, `st.line_chart`. If your data isn't time-based, drop the "submissions per day" line chart.

That's the whole edit loop. The login gate, gspread connection, caching, and deploy flow all keep working unchanged.

## Niches that fit this template well

- **Workshop / event feedback** (the demo)
- **Reading log** — books, pages, ratings, dates
- **Habit tracker** — daily check-ins for one or several habits
- **Lightweight RSVP** — names, dietary preferences, +1 count
- **Tiny issue tracker** — title, priority, status, owner
- **Inventory** — items in a small shop or library
- **Class attendance** — but see "privacy" below before using real names

## Before you ship it

- **Privacy.** Step 2 publishes the sheet to anyone with the URL. Do not put PII, grades, addresses, or anything sensitive in a public sheet. For private data, use step 3.
- **The single-password admin gate is not real authentication.** Anyone with the password sees everything. It's fine for a private dashboard you share with one or two co-organizers; it is **not** fine for protecting student records or anything regulated.
- **Sheets are not a real database.** Two people editing the admin app at the same time can race. The cell-level save in this template (only the `status` column is editable, and edits go cell-by-cell) reduces but does not eliminate the risk. For small private use, fine.
- **Rate limits.** The Google Sheets API allows ~60 reads per minute per service account. With `@st.cache_resource` and `@st.cache_data`, you'll rarely hit it. If you do, increase the cache TTL.

## Upgrades when you outgrow the defaults

- **Multi-user login** — replace the single password with [`streamlit-authenticator`](https://github.com/mkhorasani/Streamlit-Authenticator) (YAML + hashed passwords) or "Sign in with Google" via [`streamlit-oauth`](https://github.com/dnplus/streamlit-oauth).
- **Richer charts** — swap `st.bar_chart` / `st.line_chart` for [Plotly](https://plotly.com/python/) or [Altair](https://altair-viz.github.io/) when you need axis control, annotations, or interactivity. Add the library to `requirements.txt` and commit.
- **A real database** — when concurrency or scale becomes painful, move from a Sheet to SQLite (via [`sqlite-utils`](https://sqlite-utils.datasette.io/)) or a hosted Postgres (Neon, Supabase). The form layer stays Streamlit; only the read/write helpers change.
- **A custom domain** — Streamlit Community Cloud gives you `*.streamlit.app` subdomains. For a real domain, host on Fly.io, Render, or a small VM and point your DNS at it.

## A worked example: turning step 2 into a reading log

1. Make a new Google Sheet, header row: `timestamp | book | pages_read | mood`.
2. Add a few rows; publish to web as CSV ([`02-publish-sheet-to-web.md`](02-publish-sheet-to-web.md)).
3. In [`step2-read-public-sheet/app.py`](../step2-read-public-sheet/app.py):
   - Replace `SHEET_CSV_URL` with your new URL.
   - Change the filter widgets: instead of `rating_min/max` and `workshop_search`, add a date-range picker on `timestamp` and a multiselect on `mood`.
   - Replace the rating bar chart with a bar chart of `pages_read` grouped by `book`.
   - Keep the "submissions per day" line chart — it now shows your reading volume over time.
4. Commit. Done.

The structure of the file (cached loader → filters → KPIs → charts → raw table) is the part you keep; the specifics adapt.
