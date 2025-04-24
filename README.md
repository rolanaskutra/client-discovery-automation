# Client Discovery Automation

Šis projektas automatiškai generuoja potencialių klientų sąrašus su OpenAI ir įrašo duomenis į Google Sheets.

## 🔧 Instrukcijos

1. Įkelk šį projektą į naują **privatų GitHub repozitoriją** savo paskyroje.
2. Eik į **Settings > Secrets and variables > Actions** ir įrašyk šiuos slaptus raktus:

### 🔐 Required Secrets:
- `OPENAI_API_KEY` – tavo OpenAI API raktas
- `GOOGLE_SHEETS_CREDENTIALS` – `credentials.json` failo turinys iš Google Cloud Console
- `EMAIL_PASSWORD` – jei naudoji SMTP siuntimui

3. GitHub Actions automatiškai paleis šį skriptą **kiekvieną dieną 8:00 UTC**.

## 📥 Kur gauti Google Sheets credentials
Sek šią nuorodą: https://developers.google.com/sheets/api/quickstart/python

1. Sukurk naują projektą Google Cloud Console
2. Įjunk Google Sheets API
3. Sukurk OAuth2 klientą
4. Parsisiųsk `credentials.json` ir nukopijuok jo turinį kaip slaptą kintamąjį

Jei reikia pagalbos – kreipkis!
