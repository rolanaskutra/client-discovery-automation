#!/usr/bin/env python3
"""
Lokalus paleidimas su interaktyviu meniu.
Naudojimas: python run_local.py
"""
import sys
import os

# Užkraunam .env
from dotenv import load_dotenv
load_dotenv()

from config import ANTHROPIC_API_KEY, GOOGLE_SHEETS_CREDENTIALS, SPREADSHEET_ID


def check_setup():
    """Patikrina ar viskas sukonfigūruota."""
    ok = True

    if not ANTHROPIC_API_KEY:
        print("  [!] ANTHROPIC_API_KEY nenustatytas .env faile")
        ok = False
    else:
        print(f"  [OK] ANTHROPIC_API_KEY: ...{ANTHROPIC_API_KEY[-8:]}")

    if not GOOGLE_SHEETS_CREDENTIALS:
        print("  [~] GOOGLE_SHEETS_CREDENTIALS nenustatytas (rezultatai bus saugomi lokaliai)")
    else:
        print("  [OK] GOOGLE_SHEETS_CREDENTIALS: nustatytas")

    if not SPREADSHEET_ID:
        print("  [~] SPREADSHEET_ID nenustatytas (rezultatai bus saugomi lokaliai)")
    else:
        print(f"  [OK] SPREADSHEET_ID: {SPREADSHEET_ID}")

    return ok


def main():
    print("=" * 50)
    print("B2B LinkedIn automatizavimas – lokalus režimas")
    print("=" * 50)
    print("\nTikrinu konfigūraciją...")
    if not check_setup():
        print("\nSukurkite .env failą:")
        print("  cp .env.example .env")
        print("  # ir užpildykite ANTHROPIC_API_KEY")
        sys.exit(1)

    print("\nKą paleisti?")
    print("  1. Visus agentus")
    print("  2. Tik turinio generavimą")
    print("  3. Tik klientų paiešką")
    print("  4. Tik augimo planą")
    print("  5. Tik analizę")
    print("  0. Išeiti")

    choice = input("\nPasirinkimas [1]: ").strip() or "1"

    task_map = {
        "1": ["all"],
        "2": ["content"],
        "3": ["leads"],
        "4": ["growth"],
        "5": ["analyze"],
    }

    if choice == "0":
        print("Iki!")
        sys.exit(0)

    tasks = task_map.get(choice, ["all"])
    sys.argv = ["client_discovery.py"] + tasks

    from client_discovery import main as run
    run()


if __name__ == "__main__":
    main()
