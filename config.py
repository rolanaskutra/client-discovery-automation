"""
Konfigūracija: B2B gamintojo LinkedIn automatizavimas su Claude AI.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Užkrauna .env failą lokaliam darbui

# --- Claude AI (Anthropic) ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

# --- Google Sheets ---
GOOGLE_SHEETS_CREDENTIALS = os.environ.get("GOOGLE_SHEETS_CREDENTIALS", "")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")

# --- Įmonės profilis (pritaikykite savo įmonei) ---
COMPANY_PROFILE = {
    "pavadinimas": "UAB Pavyzdys",
    "sektorius": "Pramoninė gamyba",
    "produktai": [
        "CNC apdirbtos detalės",
        "Metalo konstrukcijos",
        "Pramoniniai komponentai",
    ],
    "tiksliniai_klientai": [
        "Automobilių pramonė",
        "Maisto pramonės įranga",
        "Energetikos sektorius",
        "Statybų sektorius",
    ],
    "regionai": ["Lietuva", "Latvija", "Estija", "Skandinavija", "Vokietija"],
    "kalba": "lt",  # lt = lietuvių, en = anglų, mixed = mišrus
    "tonas": "profesionalus, bet žmogiškas, be korporatyvinio žargono",
    "linkedin_url": "",
}

# --- LinkedIn turinio nustatymai ---
CONTENT_CONFIG = {
    # Kiek postų generuoti per savaitę
    "posts_per_week": 3,
    # Turinio tipų proporcijos (turi sudaryti 100%)
    "content_mix": {
        "gamybos_procesas": 25,       # Behind-the-scenes
        "klientu_istorijos": 20,      # Case studies / atsiliepimai
        "industrijos_insights": 20,   # Sektoriaus naujienos ir komentarai
        "komandos_prisistatymas": 15, # Darbuotojai, kultūra
        "produktu_naujienos": 10,     # Nauji produktai / pajėgumai
        "patarimų_postai": 10,       # Edukaciniai postai
    },
    # Natūralumo nustatymai
    "naturalness": {
        "max_emoji_per_post": 2,
        "avoid_hashtag_spam": True,
        "max_hashtags": 4,
        "vary_post_length": True,  # Trumpi ir ilgi postai kaitaliojasi
        "include_typo_chance": 0,  # 0 = jokių klaidų, 0.05 = retkarčiais
        "personal_voice": True,    # Rašyti pirmu asmeniu
    },
}

# --- Agentų konfigūracija ---
AGENTS_CONFIG = {
    "content_creator": {
        "role": "LinkedIn turinio kūrėjas",
        "focus": "Natūralus, įtraukiantis B2B turinys",
    },
    "lead_researcher": {
        "role": "Potencialių klientų tyrėjas",
        "focus": "Tikslinių įmonių ir kontaktų identifikavimas",
    },
    "network_grower": {
        "role": "Tinklo augimo strategas",
        "focus": "Ryšių plėtimas ir engagement strategija",
    },
    "analyst": {
        "role": "LinkedIn analitikos specialistas",
        "focus": "Rezultatų stebėjimas ir rekomendacijos",
    },
}
