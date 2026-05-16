# 02 · Publish a Google Sheet to the web (for step 2)

Step 2 reads a Google Sheet over plain HTTP — no authentication. To make that work, you "publish" the sheet so its contents are available as CSV at a stable URL.

## Heads-up: what "publish to web" means

- **Anyone** who has or guesses the URL can read the sheet's contents.
- Changes to the sheet appear at the URL within ~5 minutes.
- This is fine for **public, non-sensitive** data (workshop feedback, demo numbers, public registrations).
- Do **not** publish anything you wouldn't post on Twitter.

If your data is private, skip this and use step 3 instead.

## Steps

1. Create or open the Google Sheet you want to use. Make sure the **first row is a header**. For the demo schema use:

   ```
   timestamp | workshop | rating | comments | status
   ```

2. Add at least 3 rows of fake data so step 2 has something to chart. Example:

   ```
   2026-05-10 14:30 | Intro to Python | 5 | Loved the pace.       | new
   2026-05-10 14:32 | Intro to Python | 4 | More examples please. | new
   2026-05-11 10:15 | Pandas basics   | 5 |                       | reviewed
   ```

3. In the sheet menu: **File → Share → Publish to web**.
4. In the dialog:
   - Stay on the **Link** tab.
   - First dropdown: pick the specific sheet/tab (or *Entire Document*).
   - Second dropdown: choose **Comma-separated values (.csv)**.
   - Click **Publish**, then **OK** when it warns you.
5. Copy the URL it gives you. It looks like:

   ```
   https://docs.google.com/spreadsheets/d/e/2PACX-1vXXXXXXXXXX.../pub?output=csv
   ```

6. In your fork, open [`step2-read-public-sheet/app.py`](../step2-read-public-sheet/app.py) (use the pencil ✏️ or press `.` for github.dev).
7. Replace the placeholder `SHEET_CSV_URL = "..."` near the top with your URL.
8. Commit. Streamlit Cloud redeploys; your dashboard now reads from your sheet.

## Updating the data

Just edit cells in the Google Sheet. The app picks up changes within 60 seconds — controlled by the `@st.cache_data(ttl=60)` line in `app.py`. Change `ttl=60` to a smaller number for faster refresh, larger for slower.

## Stopping the publish

Same menu: **File → Share → Publish to web → Stop publishing**. The CSV URL stops working immediately.
