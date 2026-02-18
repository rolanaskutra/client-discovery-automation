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

# --- Eurodita įmonės profilis ---
COMPANY_PROFILE = {
    "pavadinimas": "Eurodita",
    "pilnas_pavadinimas": "UAB Eurodita",
    "sektorius": "Medinių konstrukcijų gamyba (B2B private-label)",
    "aprasymas": (
        "Eurodita – nuo 1994 m. veikiantis rąstinių namų, glulam namų ir medinių "
        "konstrukcijų gamintojas iš Kauno, Lietuvos. Dirbame išskirtinai B2B modeliu: "
        "gaminame private-label principu – mūsų partneriai (dileriai, statybų įmonės, "
        "distributeriai) parduoda mūsų produkciją savo prekės ženklu. Kliento klientas "
        "niekada nemato Eurodita vardo. Apdorojame 150 000 m² FSC sertifikuotos "
        "skandinaviškos eglės medienos per metus, pagaminame ~2000 individualių "
        "konstrukcijų ir ~12 000 standartinių nameliŲ. 98% užsakymų pristatome laiku."
    ),
    "produktai": [
        "Rąstiniai namai (log cabins)",
        "Glulam namai ir konstrukcijos",
        "Sodo nameliai ir pavėsinės",
        "Garažai ir sandėliukai",
        "Pirčių barelinės (sauna barrels)",
        "Glamping podai",
        "Komercinės medinės konstrukcijos",
        "Individualūs projektai pagal užsakymą (bespoke)",
    ],
    "unikalus_pasiulymas": [
        "Private-label / white-label gamyba (partnerio prekės ženklu)",
        "Nėra minimalaus užsakymo kiekio (no MOQ)",
        "Pilna individualizacija: dydis, sienos storis, išplanavimas",
        "FSC sertifikuota skandinaviška mediena",
        "Vokiška Hundegger glulam sistema, itališkos Nardi džiovyklos",
        "AutoCAD + HSB CAD projektavimas",
        "3D vizualizacijos partnerio prekės ženklu",
        "30+ metų patirtis, eksportas į 14+ šalių",
    ],
    "tiksliniai_klientai": [
        "Rąstinių namų dileriai ir pardavėjai (log cabin dealers)",
        "Sodo pastatų mažmenininkai (garden building retailers)",
        "Statybų įmonės ir rangovai (construction companies)",
        "Nekilnojamojo turto vystytojai (property developers)",
        "Glamping ir turizmo verslas (glamping operators)",
        "Distributeriai ir didmenininkai (distributors)",
        "Architektų studijos (architectural firms)",
    ],
    "regionai": [
        "Jungtinė Karalystė (UK)",
        "Vokietija",
        "Prancūzija",
        "Skandinavija (Švedija, Norvegija, Danija, Suomija)",
        "Beniliuksas (Belgija, Nyderlandai, Liuksemburgas)",
        "JAV ir Kanada",
        "Australija ir Naujoji Zelandija",
        "Airija",
        "Italija, Ispanija",
    ],
    "kalba": "en",  # Tarptautinė auditorija – anglų kalba
    "tonas": (
        "Profesionalus, bet šiltas ir žmogiškas. Kalbame kaip patyrę gamintojai, "
        "kurie supranta dilerių verslą. Ne korporatyvinis žargonas, o praktinė "
        "patirtis ir konkretūs pavyzdžiai. Pabrėžiame partnerystę, ne pardavimą."
    ),
    "linkedin_url": "https://www.linkedin.com/company/eurodita",
    "svetaine": "https://eurodita.com",
    "lokacija": "Kaunas, Lietuva",
    "imone_nuo": 1994,
}

# --- LinkedIn turinio nustatymai ---
CONTENT_CONFIG = {
    # Kiek postų generuoti per savaitę
    "posts_per_week": 3,
    # Turinio tipų proporcijos (turi sudaryti 100%)
    "content_mix": {
        "gamybos_procesas": 20,       # Behind-the-scenes: medienos apdorojimas, glulam linija, džiovyklos
        "partneriu_sekmes": 20,       # Dilerių sėkmės istorijos, private-label nauda
        "industrijos_insights": 20,   # Log cabin rinkos tendencijos, medienos industrija, tvarumas
        "produktu_showcase": 15,      # Nauji projektai, bespoke namai, glamping podai
        "b2b_patarimų_postai": 15,   # Patarimai dileriams: kaip parduoti, rinkodaros tips
        "komanda_ir_kultura": 10,     # Eurodita gamykla, žmonės, FSC, Kaunas
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
        "role": "LinkedIn turinio kūrėjas medinių namų B2B gamintojui",
        "focus": (
            "Natūralus, įtraukiantis turinys apie rąstinius namus, glulam konstrukcijas, "
            "private-label gamybą ir medienos industriją. Auditorija – dileriai, "
            "distributeriai, statybų įmonės visoje Europoje ir pasaulyje. "
            "Turinys anglų kalba."
        ),
    },
    "lead_researcher": {
        "role": "Potencialių B2B partnerių (dilerių/distributorių) tyrėjas",
        "focus": (
            "Ieško log cabin dilerių, sodo pastatų pardavėjų, statybų įmonių, "
            "glamping operatorių ir distributorių, kurie galėtų tapti Eurodita "
            "private-label partneriais. Fokusas: UK, Vokietija, Skandinavija, "
            "Prancūzija, Beniliuksas, JAV."
        ),
    },
    "network_grower": {
        "role": "Tinklo augimo strategas B2B medienos pramonei",
        "focus": (
            "Ryšių plėtimas su log cabin dileriais, statybų verslo savininkais, "
            "architektais ir nekilnojamojo turto vystytojais. Engagement strategija "
            "pritaikyta B2B private-label gamintojo specifikai."
        ),
    },
    "analyst": {
        "role": "LinkedIn analitikos specialistas medienos/statybų sektoriui",
        "focus": (
            "Rezultatų stebėjimas ir rekomendacijos Eurodita LinkedIn puslapiui. "
            "Analizuoja kas veikia log cabin / timber frame B2B nišoje."
        ),
    },
}
