"""
Claude AI agentų sistema B2B gamintojo LinkedIn valdymui.
Kiekvienas agentas turi savo specializaciją ir užduotis.
"""
import json
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, COMPANY_PROFILE, AGENTS_CONFIG


def get_client():
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def call_agent(agent_name: str, task: str, context: str = "") -> str:
    """Iškviečia Claude AI agentą su specifine užduotimi."""
    client = get_client()
    agent_cfg = AGENTS_CONFIG[agent_name]

    system_prompt = f"""Tu esi {agent_cfg['role']} B2B gamybos įmonei.
Įmonė: {COMPANY_PROFILE['pavadinimas']}
Sektorius: {COMPANY_PROFILE['sektorius']}
Produktai: {', '.join(COMPANY_PROFILE['produktai'])}
Tiksliniai klientai: {', '.join(COMPANY_PROFILE['tiksliniai_klientai'])}
Regionai: {', '.join(COMPANY_PROFILE['regionai'])}

Tavo fokusas: {agent_cfg['focus']}

SVARBIOS TAISYKLĖS:
- Rašyk natūraliai, kaip tikras žmogus, ne kaip AI
- Venk korporatyvinio žargono ir tuščių frazių
- Tonas: {COMPANY_PROFILE['tonas']}
- Niekada nerašyk "kaip AI modelis" ar panašių frazių
- Naudok konkrečius pavyzdžius, ne abstrakčius teiginius
- Kiekvienas tekstas turi skambėti taip, lyg jį rašytų įmonės darbuotojas
"""

    messages = []
    if context:
        messages.append({"role": "user", "content": f"Kontekstas:\n{context}"})
        messages.append({"role": "assistant", "content": "Supratau kontekstą. Laukiu užduoties."})

    messages.append({"role": "user", "content": task})

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Content Creator agentas
# ---------------------------------------------------------------------------

def generate_linkedin_post(content_type: str, topic_hint: str = "") -> dict:
    """Sugeneruoja natūralų LinkedIn postą."""
    task = f"""Sukurk vieną LinkedIn postą, tipas: {content_type}.
{"Tema/kontekstas: " + topic_hint if topic_hint else "Pasirink aktualią temą pats."}

FORMATO REIKALAVIMAI:
- Grąžink JSON formatu: {{"post_text": "...", "suggested_image": "...", "hashtags": ["..."]}}
- Post ilgis: 600-1500 simbolių
- Maksimaliai 4 hashtagus
- Maksimaliai 2 emoji (arba 0 – natūraliau)
- Pradėk nuo kablio (hook) – pirmas sakinys turi sudominti
- Rašyk pirmu asmeniu ("mes", "mūsų komanda", "šiandien")
- Pabaigoje – klausimas arba kvietimas diskutuoti
- NERAŠYK: "🚀", "game-changer", "excited to announce", "proud to share"
- Suggested_image: trumpas aprašymas kokia nuotrauka tiktų (komanda fotografuos)

NATŪRALUMO PATARIMAI:
- Kartais pradėk nuo trumpo sakinio ar klausimo
- Naudok pastraipas, ne vieną bloką
- Pridėk konkretų detalę (skaičių, pavadinimą, situaciją)
- Kartais pasidalink nesėkme ar iššūkiu – ne tik pergalėmis
"""
    raw = call_agent("content_creator", task)

    # Bandome ištraukti JSON iš atsakymo
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"post_text": raw, "suggested_image": "", "hashtags": []}


# ---------------------------------------------------------------------------
# Lead Researcher agentas
# ---------------------------------------------------------------------------

def research_potential_clients(industry: str, region: str, count: int = 10) -> list:
    """Tyrinėja ir identifikuoja potencialius klientus."""
    task = f"""Sudaryk sąrašą {count} potencialių klientų (B2B) šiame segmente:
Industrija: {industry}
Regionas: {region}

Kiekvienam klientui nurodyk:
- company_name: įmonės pavadinimas
- why_fit: kodėl jie galėtų būti mūsų klientas (1-2 sakiniai)
- decision_makers: kokie pareigūnai priima sprendimus (pareigybės)
- approach_strategy: kaip geriausia kreiptis per LinkedIn
- priority: high / medium / low

Grąžink JSON masyvą: [{{"company_name": "...", "why_fit": "...", "decision_makers": ["..."], "approach_strategy": "...", "priority": "..."}}]

SVARBU: Siūlyk realias, egzistuojančias įmones, ne išgalvotas.
"""
    raw = call_agent("lead_researcher", task)

    try:
        start = raw.index("[")
        end = raw.rindex("]") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return [{"raw_response": raw}]


# ---------------------------------------------------------------------------
# Network Grower agentas
# ---------------------------------------------------------------------------

def create_engagement_plan(current_followers: int = 0, target: int = 500) -> dict:
    """Sukuria tinklo augimo planą."""
    task = f"""Dabartinis sekėjų skaičius: {current_followers}
Tikslas: {target} sekėjų

Sukurk konkretų savaitinį veiksmų planą LinkedIn tinklo auginimui.

Grąžink JSON:
{{
  "weekly_actions": [
    {{"action": "...", "frequency": "...", "expected_impact": "...", "time_minutes": 15}}
  ],
  "connection_strategy": {{
    "daily_connection_requests": 5,
    "message_template": "...",
    "target_roles": ["..."]
  }},
  "engagement_tactics": [
    {{"tactic": "...", "description": "..."}}
  ],
  "content_calendar_week": [
    {{"day": "Pirmadienis", "content_type": "...", "topic": "..."}}
  ]
}}

SVARBU:
- Connection request žinutė turi būti trumpa (max 200 simbolių), natūrali, be pardavimo
- Veiksmai turi būti realistiški – max 30 min/dieną
- Fokusas į kokybę, ne kiekybę
"""
    raw = call_agent("network_grower", task)

    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"raw_response": raw}


# ---------------------------------------------------------------------------
# Analyst agentas
# ---------------------------------------------------------------------------

def analyze_and_recommend(metrics: dict) -> dict:
    """Analizuoja LinkedIn metrikas ir pateikia rekomendacijas."""
    task = f"""Štai mūsų LinkedIn puslapio metrikos:
{json.dumps(metrics, ensure_ascii=False, indent=2)}

Pateik analizę ir rekomendacijas:

Grąžink JSON:
{{
  "analysis_summary": "...",
  "whats_working": ["..."],
  "whats_not_working": ["..."],
  "recommendations": [
    {{"action": "...", "reason": "...", "priority": "high/medium/low"}}
  ],
  "next_week_focus": "..."
}}
"""
    raw = call_agent("analyst", task)

    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"raw_response": raw}
