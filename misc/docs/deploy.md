# Deploy Guide — Tripwire Launch (Quick)

Follow these steps to rebrand, configure checkout, and run the launch flow.

**0) Rebrand all assets (required first step)**

Choose one:

**Option A: Interactive prompt**
```powershell
python monetization\rebrand.py --interactive
```
You'll be prompted for company name, product details, checkout URL, and sender email.

**Option B: Use config file**
1. Copy the example: `copy monetization\branding_config.example.json monetization\branding_config.json`
2. Edit `branding_config.json` with your details
3. Apply: `python monetization\rebrand.py --config monetization\branding_config.json`

This updates all placeholders in:
- `monetization/sales_page.html` (your checkout link, price, product name)
- `monetization/emails/nurture_emails.md` (sender, company name)
- `monetization/emails/cold_outreach.md` (sender, support email)
- And all other email/copy files

1) Build payload ZIP (creates `monetization_payload.zip`):

```powershell
cd content_automation_ai
python monetization\build_payload.py
```

2) Host the sales page
- Option A: Gumroad
  - Create a new product on Gumroad with price $17.
  - Paste the contents of `monetization/sales_page.html` into the product description (or summarize and link to a hosted page).
  - Set the product to deliver `monetization_payload.zip` as the digital file (upload the ZIP to Gumroad) or set the success URL to your delivery service.

- Option B: Static host (Netlify, GitHub Pages)
  - Upload `monetization/sales_page.html` to your static host.
  - Use Stripe Checkout or Gumroad for payment; set the success URL to a script or page that triggers delivery (or use our simulator locally).

3) Configure sending (only for real sends)

**Option A: Manual env vars (quick local testing)**
Set env vars in PowerShell (example for SendGrid):
```powershell
set SENDGRID_API_KEY=SG.xxxxx
set SENDER_EMAIL=you@yourdomain.com
set TEST_RECIPIENT=you@yourdomain.com
```

Or for SMTP:
```powershell
set SMTP_HOST=smtp.example.com
set SMTP_PORT=587
set SMTP_USER=you@example.com
set SMTP_PASS=your_smtp_password
set SENDER_EMAIL=you@example.com
set TEST_RECIPIENT=you@yourdomain.com
```

**Option B: GCP Secret Manager (recommended for production)**
1. Configure `monetization/secret_map.json` with your GCP project and secret IDs:
   ```json
   {
     "project": "my-gcp-project",
     "SENDGRID_API_KEY": "sendgrid-api-key",
     "SENDER_EMAIL": "sender-email",
     "SMTP_HOST": "smtp-host",
     "SMTP_USER": "smtp-user",
     "SMTP_PASS": "smtp-pass"
   }
   ```

2. Set `GOOGLE_APPLICATION_CREDENTIALS` to point to your GCP service account JSON:
   ```powershell
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\gcp-service-account.json
   ```

3. Load secrets before sending:
   ```powershell
   python monetization\agents\send_sequence.py --template monetization\emails\nurture_emails.md --dry-run --load-secrets
   ```

**Option C: Write secrets to local .env.local (for testing)**
Once loaded, write to local `.env.local` for easy reuse in tests:
```powershell
python monetization\agents\send_sequence.py --template monetization\emails\nurture_emails.md --dry-run --load-secrets --write-env
```
This creates `.env.local` which can be sourced in subsequent runs.

4) Dry-run previews (generate 50 previews):
```powershell
python monetization\generate_50_list.py
python monetization\agents\personalize_and_preview.py --csv monetization\outreach_list_50.csv --template monetization\emails\cold_outreach_personalized.md --out monetization\previews_50.json
```

5) Preview nurture emails (no sends):
```powershell
python monetization\agents\send_sequence.py --template monetization\emails\nurture_emails.md --dry-run
```

6) Simulate a purchase (local test):
```powershell
python monetization\checkout_simulator.py --email testbuyer@example.com --price 17.0
python monetization\deliver_payload.py
```

7) Check dashboard (local):
```powershell
python monetization\dashboard.py
```

Notes:
- Do not run live sends to large lists without warmed-up sender and compliance checks.
- When ready to go live, replace placeholders in `monetization/sales_page.html`, `monetization/checkout_copy.md`, and the email templates with your real branding and links.
