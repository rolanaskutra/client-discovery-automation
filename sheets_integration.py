"""
Google Sheets integracija: rezultatų saugojimas ir skaitymas.
"""
import json
import os
from datetime import datetime

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from config import GOOGLE_SHEETS_CREDENTIALS, SPREADSHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_service():
    """Prisijungia prie Google Sheets API."""
    creds_json = GOOGLE_SHEETS_CREDENTIALS
    if not creds_json:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS nenustatytas")

    creds_data = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_data, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def _ensure_sheet_exists(service, sheet_name: str):
    """Sukuria lapą jei jo dar nėra."""
    spreadsheet = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID
    ).execute()

    existing = [s["properties"]["title"] for s in spreadsheet["sheets"]]
    if sheet_name not in existing:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]},
        ).execute()


def save_posts(posts: list[dict]):
    """Išsaugo sugeneruotus postus į 'Postai' lapą."""
    service = get_sheets_service()
    sheet_name = "Postai"
    _ensure_sheet_exists(service, sheet_name)

    # Antraštė
    header = ["Data", "Post tekstas", "Siūloma nuotrauka", "Hashtagas", "Statusas"]

    rows = [header]
    for post in posts:
        rows.append([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            post.get("post_text", ""),
            post.get("suggested_image", ""),
            ", ".join(post.get("hashtags", [])),
            "Laukia patvirtinimo",
        ])

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()


def save_leads(leads: list[dict]):
    """Išsaugo potencialius klientus į 'Klientai' lapą."""
    service = get_sheets_service()
    sheet_name = "Klientai"
    _ensure_sheet_exists(service, sheet_name)

    header = [
        "Data", "Įmonė", "Kodėl tinka", "Sprendimų priėmėjai",
        "Kreipimosi strategija", "Prioritetas", "Statusas",
    ]

    rows = [header]
    for lead in leads:
        rows.append([
            datetime.now().strftime("%Y-%m-%d"),
            lead.get("company_name", ""),
            lead.get("why_fit", ""),
            ", ".join(lead.get("decision_makers", [])),
            lead.get("approach_strategy", ""),
            lead.get("priority", ""),
            "Naujas",
        ])

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()


def save_engagement_plan(plan: dict):
    """Išsaugo tinklo augimo planą į 'Planas' lapą."""
    service = get_sheets_service()
    sheet_name = "Savaitės planas"
    _ensure_sheet_exists(service, sheet_name)

    rows = [["Savaitės veiksmų planas", datetime.now().strftime("%Y-%m-%d")], []]

    # Savaitiniai veiksmai
    rows.append(["VEIKSMAS", "DAŽNUMAS", "LAUKIAMAS EFEKTAS", "LAIKAS (min)"])
    for action in plan.get("weekly_actions", []):
        rows.append([
            action.get("action", ""),
            action.get("frequency", ""),
            action.get("expected_impact", ""),
            str(action.get("time_minutes", "")),
        ])

    rows.append([])

    # Turinio kalendorius
    rows.append(["DIENA", "TURINIO TIPAS", "TEMA"])
    for day in plan.get("content_calendar_week", []):
        rows.append([
            day.get("day", ""),
            day.get("content_type", ""),
            day.get("topic", ""),
        ])

    rows.append([])

    # Connection strategija
    conn = plan.get("connection_strategy", {})
    rows.append(["Connection strategija"])
    rows.append(["Dieniniai connection requests", str(conn.get("daily_connection_requests", ""))])
    rows.append(["Žinutės šablonas", conn.get("message_template", "")])
    rows.append(["Tikslinės pareigybės", ", ".join(conn.get("target_roles", []))])

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()


def save_analysis(analysis: dict):
    """Išsaugo analizės rezultatus."""
    service = get_sheets_service()
    sheet_name = "Analizė"
    _ensure_sheet_exists(service, sheet_name)

    rows = [
        ["LinkedIn analizė", datetime.now().strftime("%Y-%m-%d")],
        [],
        ["Santrauka", analysis.get("analysis_summary", "")],
        [],
        ["KAS VEIKIA:"],
    ]
    for item in analysis.get("whats_working", []):
        rows.append(["✓", item])

    rows.append([])
    rows.append(["KAS NEVEIKIA:"])
    for item in analysis.get("whats_not_working", []):
        rows.append(["✗", item])

    rows.append([])
    rows.append(["REKOMENDACIJOS", "PRIEŽASTIS", "PRIORITETAS"])
    for rec in analysis.get("recommendations", []):
        rows.append([
            rec.get("action", ""),
            rec.get("reason", ""),
            rec.get("priority", ""),
        ])

    rows.append([])
    rows.append(["Kitos savaitės fokusas", analysis.get("next_week_focus", "")])

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()
