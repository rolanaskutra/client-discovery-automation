# B2B Gamintojo LinkedIn Automatizavimas

Automatizuota sistema, kuri naudoja **Claude AI agentų komandą** B2B gamybos įmonės LinkedIn puslapio valdymui, potencialių klientų paieškai ir tinklo auginimui.

## Agentų komanda

| Agentas | Funkcija |
|---------|----------|
| **Turinio kūrėjas** | Generuoja natūralius LinkedIn postus (ne AI stiliumi) |
| **Klientų tyrėjas** | Identifikuoja potencialius B2B klientus pagal industriją ir regioną |
| **Tinklo augimo strategas** | Kuria savaitinį veiksmų planą sekėjų ir ryšių plėtrai |
| **Analitikos specialistas** | Analizuoja metrikas ir teikia rekomendacijas |

## Kaip veikia

1. Claude AI agentai sugeneruoja turinį ir strategijas
2. Rezultatai įrašomi į Google Sheets
3. **Žmogus peržiūri ir patvirtina** prieš publikuojant
4. GitHub Actions paleidžia automatiškai kiekvieną dieną

## Paleisti

```bash
# Visus agentus
python client_discovery.py

# Tik tam tikrus agentus
python client_discovery.py content     # Tik turinio generavimas
python client_discovery.py leads       # Tik klientų paieška
python client_discovery.py growth      # Tik augimo planas
python client_discovery.py analyze     # Tik analizė
```

## Konfigūracija

Redaguokite `config.py` ir pakeiskite `COMPANY_PROFILE` savo įmonės duomenimis.

### Reikalingi GitHub Secrets

| Secret | Aprašymas |
|--------|-----------|
| `ANTHROPIC_API_KEY` | Claude AI API raktas iš [console.anthropic.com](https://console.anthropic.com) |
| `GOOGLE_SHEETS_CREDENTIALS` | Google Cloud service account credentials JSON |
| `SPREADSHEET_ID` | Google Sheets dokumento ID |

### Natūralumo nustatymai

`config.py` > `CONTENT_CONFIG` > `naturalness`:
- `max_emoji_per_post` – riboja emoji skaičių (rekomenduojama: 0-2)
- `max_hashtags` – riboja hashtagus (rekomenduojama: 3-4)
- `personal_voice` – rašo pirmu asmeniu (natūraliau)
- `vary_post_length` – kaitalioja trumpus ir ilgus postus

## Google Sheets struktūra

Automatiškai sukuriami šie lapai:
- **Postai** – sugeneruoti LinkedIn postai peržiūrai
- **Klientai** – potencialių klientų sąrašas
- **Savaitės planas** – tinklo augimo veiksmų planas
- **Analizė** – metrikų analizė ir rekomendacijos
