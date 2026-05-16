# 03 · Service-account setup (for step 3)

Step 3 reads **and writes** a Google Sheet. To do that securely without each user logging into Google, you create a **service account** — a robot Google account that owns its own credentials. You share the sheet with the robot. The app authenticates as the robot.

This is the longest doc here. The good news: you do it once, and step 3's two apps reuse the same setup.

## 1. Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com).
2. At the top, click the project dropdown → **New project**.
3. Name it whatever you like, e.g. `sheets-template`. Click **Create**.
4. Wait for the project to be ready; make sure it's selected in the top-bar dropdown.

## 2. Enable the APIs

1. In the search bar at the top, type **Google Sheets API** → click it → **Enable**.
2. Repeat for **Google Drive API**.

(Both are required by `gspread`.)

## 3. Create the service account

1. Search **Service Accounts** → open it.
2. Click **Create service account**.
3. **Service account name:** something descriptive like `sheets-bot`. The **ID** auto-fills.
4. Click **Create and continue**. Skip the optional "grant access" steps (no roles needed). Click **Done**.

## 4. Download the JSON key

1. In the Service Accounts list, click the one you just made.
2. Go to the **Keys** tab → **Add key** → **Create new key** → **JSON** → **Create**.
3. A `.json` file downloads. **Keep it private** — anyone with this file can act as the service account.
4. Open the file in a plain text editor (TextEdit, Notepad, VS Code on the web — anything that won't autoformat). You'll copy from it in step 6.

## 5. Share the sheet with the service account

1. In the JSON file, find the `client_email` field. It looks like `sheets-bot@<project>.iam.gserviceaccount.com`.
2. Copy that email address.
3. Open your target Google Sheet (the one step 3 will write to).
4. Click **Share** at the top right.
5. Paste the `client_email`, set permission to **Editor**, untick **Notify people**, click **Share**.

The robot can now read and write the sheet.

## 6. Paste secrets into Streamlit Cloud

On your step-3 apps in Streamlit Cloud (**both** the collect app and the admin app — each has its own Secrets):

1. Open the app's **Manage app** → ⋮ → **Settings** → **Secrets**.
2. Paste, using the shape from [`.streamlit/secrets.toml.example`](../.streamlit/secrets.toml.example):

   ```toml
   sheet_id = "YOUR_SHEET_ID"
   admin_password = "pick a strong password"

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "..."
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."
   universe_domain = "googleapis.com"
   ```

3. Click **Save**. The app restarts with the new secrets.

**About the `private_key` field:** the JSON value looks like one long string with `\n` markers in it. Paste it **as-is** between the double quotes in the TOML — TOML interprets `\n` as a newline automatically.

## 7. Find your sheet ID

The sheet ID is in the sheet's URL:

```
https://docs.google.com/spreadsheets/d/THIS_LONG_RANDOM_STRING/edit#gid=0
                                       ^^^^^^^^^^^^^^^^^^^^^^^
```

Copy that string into `sheet_id` in the secrets.

## Why this much ceremony?

You're handing a robot account read-and-write power on a specific sheet. That requires:

- Identifying the robot (the service account exists → has a `client_email`)
- Proving you're the robot (the JSON key)
- Giving the robot permission on that specific sheet (sharing it as Editor)

Once it's done, you never think about it again — until the key expires (the JSON key has no expiry by default, but you should rotate it every few months if the data matters).
