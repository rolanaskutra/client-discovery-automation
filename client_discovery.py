"""
Pagrindinis skriptas: B2B gamintojo LinkedIn automatizavimas su Claude AI.

Paleidžia agentų komandą, kuri:
1. Generuoja natūralų LinkedIn turinį
2. Ieško potencialių klientų
3. Kuria tinklo augimo strategiją
4. Analizuoja rezultatus ir teikia rekomendacijas

Rezultatai rašomi į Google Sheets žmogaus peržiūrai ir patvirtinimui.
"""
import json
import sys
from datetime import datetime

from config import COMPANY_PROFILE, CONTENT_CONFIG
from agents import (
    generate_linkedin_post,
    research_potential_clients,
    create_engagement_plan,
    analyze_and_recommend,
)
def _try_load_sheets():
    """Bando užkrauti Google Sheets modulį (gali nepavykti lokaliai)."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "-c", "from sheets_integration import save_posts"],
        capture_output=True, timeout=10,
    )
    if result.returncode == 0:
        import sheets_integration
        return sheets_integration
    print("  [~] Google Sheets nepasiekiamas – rezultatai bus saugomi lokaliai")
    return None


def run_content_generation():
    """1 agentas: Turinio kūrėjas – generuoja savaitės postus."""
    print("\n--- TURINIO KŪRĖJAS ---")
    content_types = list(CONTENT_CONFIG["content_mix"].keys())
    posts_needed = CONTENT_CONFIG["posts_per_week"]

    posts = []
    for i in range(posts_needed):
        content_type = content_types[i % len(content_types)]
        print(f"  Generuojamas postas {i+1}/{posts_needed} ({content_type})...")
        post = generate_linkedin_post(content_type)
        posts.append(post)
        print(f"  ✓ Postas sukurtas ({len(post.get('post_text', ''))} simbolių)")

    return posts


def run_lead_research():
    """2 agentas: Klientų tyrėjas – ieško potencialių klientų."""
    print("\n--- KLIENTŲ TYRĖJAS ---")
    all_leads = []

    for industry in COMPANY_PROFILE["tiksliniai_klientai"]:
        for region in COMPANY_PROFILE["regionai"][:2]:  # Pirmi 2 regionai
            print(f"  Ieškoma: {industry} / {region}...")
            leads = research_potential_clients(industry, region, count=5)
            all_leads.extend(leads)
            print(f"  ✓ Rasta {len(leads)} potencialių klientų")

    return all_leads


def run_network_growth():
    """3 agentas: Tinklo augimo strategas."""
    print("\n--- TINKLO AUGIMO STRATEGAS ---")
    plan = create_engagement_plan(current_followers=0, target=500)
    print("  ✓ Savaitės planas sukurtas")
    return plan


def run_analysis(metrics: dict = None):
    """4 agentas: Analitikos specialistas."""
    print("\n--- ANALITIKOS SPECIALISTAS ---")
    if metrics is None:
        metrics = {
            "followers": 0,
            "posts_last_week": 0,
            "avg_engagement_rate": 0,
            "top_post_impressions": 0,
            "connection_requests_sent": 0,
            "connection_requests_accepted": 0,
            "profile_views": 0,
            "note": "Pradinė analizė – puslapio startas",
        }
    analysis = analyze_and_recommend(metrics)
    print("  ✓ Analizė atlikta")
    return analysis


def main():
    """Paleidžia visus agentus ir išsaugo rezultatus."""
    print("=" * 60)
    print(f"B2B LinkedIn automatizavimas – {COMPANY_PROFILE['pavadinimas']}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Claude AI agentų komanda startuoja...")
    print("=" * 60)

    # Nustatome ką paleisti
    tasks = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    results = {}

    sheets = _try_load_sheets()

    if "all" in tasks or "content" in tasks:
        posts = run_content_generation()
        results["posts"] = posts
        _save(sheets, "save_posts", posts, "posts")

    if "all" in tasks or "leads" in tasks:
        leads = run_lead_research()
        results["leads"] = leads
        _save(sheets, "save_leads", leads, "leads")

    if "all" in tasks or "growth" in tasks:
        plan = run_network_growth()
        results["plan"] = plan
        _save(sheets, "save_engagement_plan", plan, "growth_plan")

    if "all" in tasks or "analyze" in tasks:
        analysis = run_analysis()
        results["analysis"] = analysis
        _save(sheets, "save_analysis", analysis, "analysis")

    print("\n" + "=" * 60)
    print("Visi agentai baigė darbą.")
    print("Peržiūrėkite rezultatus Google Sheets ir patvirtinkite prieš publikuojant.")
    print("=" * 60)

    return results


def _save(sheets_module, func_name: str, data, local_name: str):
    """Bando išsaugoti į Sheets, jei nepavyksta – lokaliai."""
    if sheets_module:
        try:
            getattr(sheets_module, func_name)(data)
            print(f"  → Išsaugota į Google Sheets")
            return
        except Exception as e:
            print(f"  ⚠ Sheets klaida: {e}")
    _save_local(data, local_name)


def _save_local(data, name: str):
    """Išsaugo rezultatus lokaliai JSON faile."""
    filename = f"output_{name}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  → Išsaugota lokaliai: {filename}")


if __name__ == "__main__":
    main()
