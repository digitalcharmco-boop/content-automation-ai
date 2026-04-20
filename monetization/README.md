# Monetization Toolkit

This folder contains quick assets to launch a low-friction tripwire and simple email automation.

Files:
- `tripwire_page.md` — minimal sales page copy
- `emails/nurture_emails.md` — 5-message nurture sequence
- `emails/cold_outreach.md` — 6-step cold outreach
- `agents/send_sequence.py` — simple sender supporting SMTP or SendGrid
- `agents/dry_run_send.py` — preview rendered emails locally

Quick setup (Powershell):
```powershell
cd content_automation_ai
#set SENDGRID_API_KEY=SG.xxxxx (optional)
#set SMTP_HOST=smtp.example.com
#set SMTP_PORT=587
#set SMTP_USER=you@example.com
#set SMTP_PASS=your_smtp_password
set TEST_RECIPIENT=you@yourdomain.com
set SENDER_EMAIL=you@yourdomain.com
```

Dry-run (prints emails without sending):
```powershell
python monetization\agents\send_sequence.py --template monetization/emails/nurture_emails.md --dry-run
```

To actually send using SMTP:
```powershell
python monetization\agents\send_sequence.py --template monetization/emails/nurture_emails.md --provider smtp
```

To send via SendGrid (set `SENDGRID_API_KEY`):
```powershell
python monetization\agents\send_sequence.py --template monetization/emails/nurture_emails.md --provider sendgrid
```

Notes:
- Use `--to` to override the recipient for testing.
- The scripts are intentionally minimal — they are a starting point. Do not run against large lists without warming up infrastructure and compliance checks.