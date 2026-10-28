from __future__ import annotations

import json
import math
import os
import random
import uuid
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import streamlit as st

APP_NAME = "Personalized Travel Itinerary Planner"
DATA_DIR = Path("data")
TRIPS_FILE = DATA_DIR / "trips.json"
DATA_DIR.mkdir(exist_ok=True)

# Demo catalog: coordinates are approximate city/attraction coordinates, intended for itinerary planning,
# not turn-by-turn navigation. Costs are illustrative and should be verified before travel.
DESTINATIONS = [
    {"city": "Jaipur", "country": "India", "vibes": ["Cultural", "Urban"], "budget": "Budget", "season": ["Winter", "Autumn"], "tags": ["Heritage", "Markets", "Architecture"], "currency": "INR", "symbol": "₹", "usd": 0.012, "base_daily": 2600,
     "attractions": [
        ("Amber Fort", "Morning Sightseeing", "History", 26.9855, 75.8513, 500, "Explore the hilltop fort and its courtyards."),
        ("Hawa Mahal", "Morning Sightseeing", "History", 26.9239, 75.8267, 200, "Admire the iconic pink sandstone facade."),
        ("City Palace", "Afternoon Leisure", "History", 26.9258, 75.8237, 500, "Visit royal galleries and palace courtyards."),
        ("Johari Bazaar", "Afternoon Leisure", "Shopping", 26.9196, 75.8267, 300, "Browse jewellery, textiles, and local crafts."),
        ("Masala Chowk", "Lunch Recommendation", "Food", 26.9118, 75.8131, 350, "Sample a variety of Rajasthani street-food favourites."),
        ("Chokhi Dhani", "Evening Dining & Entertainment", "Food", 26.7680, 75.8435, 900, "Enjoy a village-themed dinner and folk performances."),
        ("Nahargarh Fort", "Evening Dining & Entertainment", "Adventure", 26.9370, 75.8150, 250, "Catch panoramic sunset views over the city."),
     ]},
    {"city": "Goa", "country": "India", "vibes": ["Beach", "Adventure", "Urban"], "budget": "Moderate", "season": ["Winter", "Spring"], "tags": ["Beaches", "Seafood", "Sunsets"], "currency": "INR", "symbol": "₹", "usd": 0.012, "base_daily": 4200,
     "attractions": [
        ("Baga Beach", "Morning Sightseeing", "Adventure", 15.5557, 73.7516, 0, "Start with a beach walk and optional water activities."),
        ("Fort Aguada", "Morning Sightseeing", "History", 15.4923, 73.7737, 100, "Explore the Portuguese-era fort and sea views."),
        ("Anjuna Flea Market", "Afternoon Leisure", "Shopping", 15.5736, 73.7408, 300, "Browse stalls for crafts, clothes, and souvenirs."),
        ("Fisherman's Wharf", "Lunch Recommendation", "Food", 15.4984, 73.8290, 650, "Choose a riverside meal; ask about vegetarian options."),
        ("Fontainhas", "Afternoon Leisure", "History", 15.4988, 73.8292, 150, "Wander colourful lanes in the Latin Quarter."),
        ("Candolim Beach", "Evening Dining & Entertainment", "Nightlife", 15.5181, 73.7626, 500, "Relax by the shore and find a sunset café."),
        ("Panaji Market", "Afternoon Leisure", "Food", 15.4989, 73.8278, 250, "Try local snacks and browse the city market."),
     ]},
    {"city": "Manali", "country": "India", "vibes": ["Mountains", "Adventure"], "budget": "Moderate", "season": ["Summer", "Winter"], "tags": ["Mountain Views", "Hikes", "Cafés"], "currency": "INR", "symbol": "₹", "usd": 0.012, "base_daily": 3600,
     "attractions": [
        ("Hadimba Devi Temple", "Morning Sightseeing", "History", 32.2432, 77.1892, 50, "Visit a cedar-forest temple with distinctive architecture."),
        ("Old Manali", "Morning Sightseeing", "Food", 32.2570, 77.1850, 250, "Explore relaxed lanes, bakeries, and small cafés."),
        ("Manu Temple", "Afternoon Leisure", "History", 32.2595, 77.1855, 0, "Walk through a quiet temple area in Old Manali."),
        ("Mall Road", "Afternoon Leisure", "Shopping", 32.2396, 77.1887, 300, "Browse shops and try local snacks."),
        ("Solang Valley", "Morning Sightseeing", "Adventure", 32.3167, 77.1600, 800, "Enjoy mountain scenery; activity charges vary by season."),
        ("Café 1947", "Lunch Recommendation", "Food", 32.2577, 77.1849, 600, "Take a café break by the river."),
        ("Riverside Dinner", "Evening Dining & Entertainment", "Food", 32.2500, 77.1900, 700, "Choose a riverside restaurant and confirm opening hours."),
     ]},
    {"city": "Mumbai", "country": "India", "vibes": ["Urban", "Cultural"], "budget": "Moderate", "season": ["Winter"], "tags": ["Street Food", "Architecture", "Nightlife"], "currency": "INR", "symbol": "₹", "usd": 0.012, "base_daily": 4500,
     "attractions": [
        ("Gateway of India", "Morning Sightseeing", "History", 18.9220, 72.8347, 0, "See the waterfront landmark early to avoid crowds."),
        ("Chhatrapati Shivaji Maharaj Vastu Sangrahalaya", "Morning Sightseeing", "History", 18.9269, 72.8325, 350, "Explore art, archaeology, and natural-history collections."),
        ("Kala Ghoda", "Afternoon Leisure", "Culture", 18.9270, 72.8310, 250, "Walk through galleries, cafés, and design shops."),
        ("Crawford Market", "Afternoon Leisure", "Shopping", 18.9467, 72.8340, 200, "Browse a historic market; check local opening times."),
        ("Café Mondegar", "Lunch Recommendation", "Food", 18.9228, 72.8323, 600, "Take a casual break near Colaba."),
        ("Marine Drive", "Evening Dining & Entertainment", "Adventure", 18.9430, 72.8235, 150, "Walk the promenade around sunset."),
        ("Mohammed Ali Road Food Walk", "Evening Dining & Entertainment", "Food", 18.9568, 72.8330, 500, "Sample local food; verify seasonal availability."),
     ]},
    {"city": "Udaipur", "country": "India", "vibes": ["Cultural", "Relaxed"], "budget": "Moderate", "season": ["Winter", "Autumn"], "tags": ["Lakes", "Palaces", "Slow Travel"], "currency": "INR", "symbol": "₹", "usd": 0.012, "base_daily": 3300,
     "attractions": [
        ("City Palace Udaipur", "Morning Sightseeing", "History", 24.5764, 73.6835, 400, "Explore palace courtyards and lake-facing views."),
        ("Jagdish Temple", "Morning Sightseeing", "History", 24.5797, 73.6830, 0, "Visit a historic temple near the old city."),
        ("Bagore Ki Haveli", "Afternoon Leisure", "Culture", 24.5800, 73.6820, 150, "Explore a restored haveli and local exhibits."),
        ("Lake Pichola Boat Ride", "Afternoon Leisure", "Adventure", 24.5760, 73.6800, 600, "Enjoy lake views; boat schedules depend on conditions."),
        ("Bada Bazaar", "Afternoon Leisure", "Shopping", 24.5780, 73.6900, 250, "Browse textiles, miniature paintings, and crafts."),
        ("Ambrai Restaurant Area", "Evening Dining & Entertainment", "Food", 24.5760, 73.6810, 900, "Look for lake-view dining and reserve ahead if needed."),
        ("Fateh Sagar Lake", "Evening Dining & Entertainment", "Adventure", 24.6010, 73.6770, 100, "Take a lakeside stroll in the evening."),
     ]},
    {"city": "Bali", "country": "Indonesia", "vibes": ["Beach", "Adventure", "Cultural"], "budget": "Moderate", "season": ["Summer", "Spring"], "tags": ["Tropical", "Temples", "Wellness"], "currency": "IDR", "symbol": "Rp", "usd": 0.000064, "base_daily": 650000,
     "attractions": [
        ("Uluwatu Temple", "Morning Sightseeing", "History", -8.8291, 115.0849, 50000, "Visit the cliffside temple respectfully; watch for monkeys."),
        ("Padang Padang Beach", "Morning Sightseeing", "Adventure", -8.8114, 115.1040, 15000, "Spend time on a scenic beach; check surf conditions."),
        ("Ubud Art Market", "Afternoon Leisure", "Shopping", -8.5069, 115.2625, 100000, "Browse local crafts and handmade souvenirs."),
        ("Warung Vegetarian Lunch", "Lunch Recommendation", "Food", -8.5060, 115.2600, 90000, "A sample vegetarian-friendly meal stop; confirm menu locally."),
        ("Tegallalang Rice Terrace", "Afternoon Leisure", "Adventure", -8.4312, 115.2792, 25000, "Walk through iconic rice terraces and viewpoints."),
        ("Jimbaran Seafood Dinner", "Evening Dining & Entertainment", "Food", -8.7680, 115.1670, 250000, "Consider a beachside dinner and verify current prices."),
        ("Ubud Evening Walk", "Evening Dining & Entertainment", "Culture", -8.5065, 115.2620, 0, "Enjoy shops and cultural venues around central Ubud."),
     ]},
]

SEASONS = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Summer",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn",
}
BUDGET_FACTOR = {"Budget": 0.68, "Moderate": 1.0, "Luxury": 1.85}
PACE_SLOTS = {
    "Relaxed": ["Morning Sightseeing", "Lunch Recommendation", "Afternoon Leisure", "Evening Dining & Entertainment"],
    "Moderate": ["Morning Sightseeing", "Lunch Recommendation", "Afternoon Leisure", "Evening Dining & Entertainment"],
    "Fast-Paced": ["Morning Sightseeing", "Lunch Recommendation", "Afternoon Leisure", "Evening Dining & Entertainment"],
}
SLOT_TIMES = {
    "Morning Sightseeing": "09:00–11:30",
    "Lunch Recommendation": "12:00–13:30",
    "Afternoon Leisure": "14:00–16:30",
    "Evening Dining & Entertainment": "18:00–20:30",
}
INTEREST_TO_CATEGORY = {"Food": "Food", "Adventure": "Adventure", "History": "History", "Nightlife": "Nightlife"}

def haversine_km(a: dict, b: dict) -> float:
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [a["lat"], a["lon"], b["lat"], b["lon"]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def current_season(start: date) -> str:
    return SEASONS[start.month]

def load_trips() -> list[dict]:
    try:
        if TRIPS_FILE.exists():
            payload = json.loads(TRIPS_FILE.read_text(encoding="utf-8"))
            return payload if isinstance(payload, list) else []
    except (OSError, json.JSONDecodeError):
        st.warning("Saved trip history could not be read. A fresh local history will be used.")
    return []

def save_trips(trips: list[dict]) -> None:
    try:
        DATA_DIR.mkdir(exist_ok=True)
        temp = TRIPS_FILE.with_suffix(".tmp")
        temp.write_text(json.dumps(trips, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(TRIPS_FILE)
    except OSError as exc:
        st.error(f"Could not save trip history: {exc}. Check that the app directory is writable.")

def destination_by_city(city: str) -> dict:
    return next((d for d in DESTINATIONS if d["city"] == city), DESTINATIONS[0])

def recommend_destinations(vibe: str, budget: str, start: date, interests: list[str]) -> list[dict]:
    season = current_season(start)
    scored = []
    for d in DESTINATIONS:
        score = 0
        if vibe == "Any" or vibe in d["vibes"]: score += 3
        if d["budget"] == budget: score += 2
        elif budget == "Budget" and d["base_daily"] < 4000: score += 1
        if season in d["season"]: score += 2
        matched = [tag for tag in interests if any(tag.lower() in a[2].lower() or tag.lower() in a[1].lower() for a in d["attractions"])]
        score += min(len(matched), 3)
        scored.append((score, d))
    scored.sort(key=lambda x: (-x[0], x[1]["city"]))
    return [d for _, d in scored[:3]]

def _attraction_dict(raw: tuple) -> dict:
    name, slot, category, lat, lon, cost, description = raw
    return {"name": name, "slot": slot, "category": category, "lat": lat, "lon": lon,
            "cost": int(cost), "description": description}

def _select_daily_stops(dest: dict, prefs: dict, day_index: int, used_names: set[str]) -> list[dict]:
    attractions = [_attraction_dict(a) for a in dest["attractions"] if a[0] not in used_names]
    interests = prefs["interests"]
    def rank(a: dict) -> tuple:
        interest_score = 1 if a["category"] in interests else 0
        if a["slot"] == "Lunch Recommendation" and "Food" in interests: interest_score += 2
        return (-interest_score, a["name"])
    attractions.sort(key=rank)
    chosen = []
    for slot in PACE_SLOTS[prefs["pace"]]:
        candidates = [a for a in attractions if a["slot"] == slot]
        if not candidates:
            candidates = [a for a in attractions if slot == a["slot"]]
        if candidates:
            if chosen:
                candidates.sort(key=lambda a: haversine_km(chosen[-1], a))
            selected = candidates[0]
            selected["slot"] = slot
            chosen.append(selected)
            attractions.remove(selected)
            used_names.add(selected["name"])
    # Reorder the selected activities by slot then greedily cluster within each time block.
    chosen.sort(key=lambda a: list(SLOT_TIMES).index(a["slot"]))
    # Add a small estimated local transit allowance based on approximate route hops.
    return chosen

def generate_itinerary(dest: dict, prefs: dict, trip_id: str | None = None) -> dict:
    used: set[str] = set()
    days = []
    factor = BUDGET_FACTOR[prefs["budget"]]
    for i in range(prefs["duration"]):
        stops = _select_daily_stops(dest, prefs, i, used)
        if not stops:
            stops = [_attraction_dict(dest["attractions"][j % len(dest["attractions"])]) for j in range(4)]
        # Estimate transfers using nearest-neighbour ordering within each day while retaining slot sequence.
        total = 0
        previous = None
        for stop in stops:
            transit = 0
            if previous:
                distance = haversine_km(previous, stop)
                transit = int(max(0, distance * 8 * factor))
            stop["cost"] = int(stop["cost"] * factor)
            stop["transit_cost"] = transit
            stop["total_cost"] = stop["cost"] + transit
            stop["time"] = SLOT_TIMES[stop["slot"]]
            total += stop["total_cost"]
            previous = stop
        # Costs are estimates. Accommodation and intercity travel are separately estimated.
        lodging = int(dest["base_daily"] * 0.45 * factor)
        local_transport = int(dest["base_daily"] * 0.12 * factor)
        day_total = total + lodging + local_transport
        days.append({
            "day": i + 1,
            "date": (prefs["start_date"] + timedelta(days=i)).isoformat(),
            "title": f"Day {i + 1} in {dest['city']}",
            "activities": stops,
            "lodging_estimate": lodging,
            "transport_estimate": local_transport,
            "estimated_total": day_total,
            "notes": "Keep entry tickets and local opening times flexible; estimates are indicative."
        })
    return {
        "id": trip_id or str(uuid.uuid4())[:8],
        "name": f"{dest['city']} · {prefs['duration']} days",
        "created_at": date.today().isoformat(),
        "destination": dest["city"],
        "country": dest["country"],
        "currency": dest["currency"],
        "symbol": dest["symbol"],
        "usd_rate": dest["usd"],
        "preferences": {**prefs, "start_date": prefs["start_date"].isoformat()},
        "days": days,
        "total_estimate": sum(d["estimated_total"] for d in days),
        "status": "Draft"
    }

def get_ai_client(provider: str, api_key: str):
    if provider == "Gemini":
        from google import genai
        return genai.Client(api_key=api_key)
    if provider == "Groq":
        from groq import Groq
        return Groq(api_key=api_key)
    raise ValueError("Unsupported AI provider")

def ask_ai(provider: str, api_key: str, prompt: str) -> str:
    if provider == "Gemini":
        client = get_ai_client(provider, api_key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text or ""
    client = get_ai_client(provider, api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a careful travel planner. Return concise valid JSON when asked."},
                  {"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content or ""

def enrich_itinerary_with_ai(trip: dict, provider: str, api_key: str) -> dict:
    prompt = (
        "Improve this travel itinerary while preserving its JSON structure, all day numbers, dates, "
        "slot names, cost fields, and destination. You may improve descriptions and add practical tips, "
        "but do not invent live opening hours or claim prices are verified. Return only JSON.\n"
        + json.dumps(trip, ensure_ascii=False)
    )
    raw = ask_ai(provider, api_key, prompt)
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("AI response did not contain a JSON object.")
    candidate = json.loads(raw[start:end + 1])
    if not isinstance(candidate.get("days"), list) or len(candidate["days"]) != len(trip["days"]):
        raise ValueError("AI returned an incompatible itinerary; the original plan was kept.")
    return candidate

def format_money(amount: float, trip: dict) -> str:
    local = f"{trip['symbol']}{amount:,.0f} {trip['currency']}"
    usd = amount * float(trip.get("usd_rate", 0.012))
    inr = amount if trip["currency"] == "INR" else amount / max(float(trip.get("usd_rate", 0.012)), 0.000001)
    return f"{local}  ·  ${usd:,.2f} USD  ·  ₹{inr:,.0f} INR"

def make_pdf(trip: dict) -> bytes:
    from io import BytesIO
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=17*mm, leftMargin=17*mm, topMargin=16*mm, bottomMargin=16*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=colors.HexColor("#164e63"), alignment=TA_LEFT, spaceAfter=8))
    styles.add(ParagraphStyle(name="Subtle", parent=styles["Normal"], fontSize=9, leading=13, textColor=colors.HexColor("#52616b")))
    styles.add(ParagraphStyle(name="DayHead", parent=styles["Heading2"], textColor=colors.HexColor("#0f766e"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="SmallBody", parent=styles["BodyText"], fontSize=8.5, leading=11))
    story = [
        Paragraph("WANDER / PLAN", styles["Subtle"]),
        Spacer(1, 5*mm),
        Paragraph(f"{trip['destination']} Travel Guide", styles["CoverTitle"]),
        Paragraph(f"{len(trip['days'])}-day personalized itinerary · {trip['country']}", styles["Heading3"]),
        Spacer(1, 3*mm),
        Paragraph(f"Estimated trip budget: <b>{format_money(trip['total_estimate'], trip)}</b>", styles["BodyText"]),
        Paragraph("Budget figures are illustrative estimates, not live quotes. Confirm tickets, transport, opening hours, visa rules, and weather before departure.", styles["Subtle"]),
        Spacer(1, 6*mm),
    ]
    prefs = trip.get("preferences", {})
    pref_line = f"Budget: {prefs.get('budget','—')} · Party: {prefs.get('party','—')} · Pace: {prefs.get('pace','—')} · Interests: {', '.join(prefs.get('interests', [])) or 'General'}"
    story += [Paragraph(pref_line, styles["SmallBody"]), Spacer(1, 5*mm)]
    for day in trip["days"]:
        story.append(Paragraph(f"Day {day['day']} · {day.get('date','')}", styles["DayHead"]))
        rows = [["Time", "Plan", "Estimate"]]
        for activity in day.get("activities", []):
            rows.append([
                activity.get("time", SLOT_TIMES.get(activity.get("slot", ""), "")),
                f"<b>{activity.get('name','Activity')}</b><br/><font color='#52616b'>{activity.get('description','')}</font>",
                f"{trip['symbol']}{activity.get('total_cost', activity.get('cost',0)):,}"
            ])
        rows.append(["", "Accommodation estimate", f"{trip['symbol']}{day.get('lodging_estimate',0):,}"])
        rows.append(["", "Local transport estimate", f"{trip['symbol']}{day.get('transport_estimate',0):,}"])
        rows.append(["", "<b>Day total</b>", f"<b>{trip['symbol']}{day.get('estimated_total',0):,}</b>"])
        table = Table(rows, colWidths=[28*mm, 105*mm, 35*mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#164e63")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#d8e1e5")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f4f8f8")]),
            ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story += [table, Spacer(1, 4*mm), Paragraph(day.get("notes", ""), styles["Subtle"])]
    story += [
        PageBreak(),
        Paragraph("Before You Go", styles["Heading1"]),
        Paragraph("Emergency & practical checklist", styles["Heading2"]),
        Paragraph("□ Save local emergency number and nearest hospital<br/>□ Save accommodation address offline<br/>□ Share itinerary with a trusted contact<br/>□ Check travel insurance and required documents<br/>□ Keep copies of passport/ID separate from originals<br/>□ Confirm transport, reservations, and attraction hours<br/>□ Download offline maps and translation support<br/>□ Carry required medication and a power bank", styles["BodyText"]),
        Spacer(1, 4*mm),
        Paragraph("Emergency contacts (fill in before travel)", styles["Heading2"]),
        Paragraph("Local emergency number: __________________________________<br/>Accommodation / host: ______________________________________<br/>Travel insurance: ___________________________________________<br/>Trusted contact: ____________________________________________", styles["BodyText"]),
        Spacer(1, 8*mm),
        Paragraph("Generated by Personalized Travel Itinerary Planner. Activity prices, travel times, and currency conversions are estimates and may change.", styles["Subtle"])
    ]
    doc.build(story)
    return buffer.getvalue()

def apply_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root { --ink:#173b3b; --teal:#0f766e; --mint:#dff5ec; --sand:#fbf7ef; }
    .stApp { background: linear-gradient(180deg,#f7fbf8 0%,#fbf8f1 100%); color:var(--ink); }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    h1,h2,h3 { font-family:'Playfair Display',serif !important; color:#173b3b; }
    .hero { padding:2rem 2rem 1.6rem; border-radius:24px; background:linear-gradient(125deg,#dff5ec 0%,#f7e9d4 100%); border:1px solid #d4e8dd; margin-bottom:1rem; }
    .eyebrow { text-transform:uppercase; letter-spacing:.16em; font-size:.72rem; font-weight:700; color:#0f766e; }
    .hero h1 { font-size:2.5rem; line-height:1.08; margin:.35rem 0 .6rem; }
    .hero p { max-width:780px; color:#49605b; font-size:1.03rem; }
    .metric-card { background:rgba(255,255,255,.82); border:1px solid #e1e9e3; padding:1rem 1.1rem; border-radius:18px; min-height:92px; }
    .tag { display:inline-block; padding:.25rem .6rem; margin:.15rem .2rem .15rem 0; border-radius:999px; background:#dff5ec; color:#0f625a; font-size:.78rem; font-weight:600; }
    [data-testid="stSidebar"] { background:#eef7f1; border-right:1px solid #dbe9df; }
    div.stButton > button, div.stDownloadButton > button { border-radius:12px; border:1px solid #0f766e; font-weight:700; }
    div.stButton > button[kind="primary"] { background:#0f766e; color:white; }
    div[data-testid="stExpander"] { border-radius:14px; border:1px solid #dce8e1; background:rgba(255,255,255,.6); }
    .small-note { font-size:.82rem; color:#61736d; }
    </style>
    """, unsafe_allow_html=True)

def init_state():
    defaults = {
        "trip": None, "trips": load_trips(), "destination": "Jaipur",
        "duration": 3, "start_date": date.today() + timedelta(days=14),
        "budget": "Moderate", "party": "Couple", "pace": "Moderate",
        "vibe": "Any", "interests": ["Food", "History"],
        "provider": "Demo mode", "api_key": "", "last_saved_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def prefs_from_form() -> dict:
    return {
        "duration": int(st.session_state.duration),
        "start_date": st.session_state.start_date,
        "budget": st.session_state.budget,
        "party": st.session_state.party,
        "pace": st.session_state.pace,
        "vibe": st.session_state.vibe,
        "interests": st.session_state.interests,
    }

def regenerate_day(trip: dict, day_number: int, slot: str, instruction: str, provider: str, api_key: str) -> dict:
    new_trip = json.loads(json.dumps(trip))
    day = next(d for d in new_trip["days"] if d["day"] == day_number)
    dest = destination_by_city(trip["destination"])
    current_names = {a["name"] for a in day["activities"]}
    candidates = [_attraction_dict(a) for a in dest["attractions"] if a[1] == slot and a[0] not in current_names]
    # Add slot-matching suggestions from the entire catalog if a destination's local list is limited.
    if not candidates:
        candidates = [_attraction_dict(a) for a in dest["attractions"] if a[0] not in current_names]
    if provider != "Demo mode" and api_key.strip():
        prompt = (
            f"Suggest one realistic replacement activity for {trip['destination']} in the time slot {slot}. "
            f"User request: {instruction}. Budget level: {trip['preferences']['budget']}. "
            "Return JSON only: {name, description, estimated_cost_local, category}. Do not claim live availability."
        )
        try:
            raw = ask_ai(provider, api_key, prompt)
            s, e = raw.find("{"), raw.rfind("}")
            obj = json.loads(raw[s:e+1])
            replacement = {
                "name": str(obj.get("name", "Local discovery stop")),
                "slot": slot, "category": str(obj.get("category", "Culture")),
                "lat": candidates[0]["lat"] if candidates else 0,
                "lon": candidates[0]["lon"] if candidates else 0,
                "cost": int(obj.get("estimated_cost_local", 300)),
                "description": str(obj.get("description", "A suggested stop; verify details locally.")),
            }
        except Exception:
            replacement = None
    else:
        replacement = None
    if not replacement:
        if candidates:
            replacement = candidates[0]
            if instruction.strip():
                replacement["description"] += f" Personalization: {instruction.strip()}."
        else:
            replacement = {"name": "Flexible local discovery", "slot": slot, "category": "Culture", "lat": 0, "lon": 0,
                           "cost": 250, "description": f"Choose a local activity matching: {instruction or 'your current mood'}."}
    factor = BUDGET_FACTOR[trip["preferences"]["budget"]]
    replacement["cost"] = int(replacement.get("cost", 250) * factor)
    replacement["transit_cost"] = 0
    replacement["total_cost"] = replacement["cost"]
    replacement["time"] = SLOT_TIMES[slot]
    old = next((a for a in day["activities"] if a["slot"] == slot), None)
    if old:
        day["activities"].remove(old)
    day["activities"].append(replacement)
    day["activities"].sort(key=lambda a: list(SLOT_TIMES).index(a["slot"]))
    day["estimated_total"] = sum(a.get("total_cost", a.get("cost", 0)) for a in day["activities"]) + day["lodging_estimate"] + day["transport_estimate"]
    new_trip["total_estimate"] = sum(d["estimated_total"] for d in new_trip["days"])
    return new_trip

def render_trip_summary(trip: dict):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="small-note">Estimated total</div><h3>{trip["symbol"]}{trip["total_estimate"]:,.0f}</h3><div class="small-note">Local currency</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="small-note">Trip length</div><h3>{len(trip["days"])} days</h3><div class="small-note">{trip["preferences"]["party"]} · {trip["preferences"]["pace"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="small-note">USD / INR reference</div><h3>${trip["total_estimate"]*trip["usd_rate"]:,.0f}</h3><div class="small-note">₹{(trip["total_estimate"] if trip["currency"]=="INR" else trip["total_estimate"]/max(trip["usd_rate"],0.000001)):,.0f} INR</div></div>', unsafe_allow_html=True)
    st.caption("Cost estimates are illustrative. Currency conversion uses a static demo rate and is not a live exchange quote.")

def main():
    st.set_page_config(page_title=APP_NAME, page_icon="🧭", layout="wide")
    apply_css()
    init_state()

    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Skill Wallet · Capstone Project 4</div>
      <h1>Personalized Travel<br/>Itinerary Planner</h1>
      <p>Build thoughtful, budget-aware journeys with clustered daily plans, flexible activity swaps, and a travel guide you can take offline.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ✦ Your travel brief")
        st.selectbox("AI engine", ["Demo mode", "Gemini", "Groq"], key="provider", help="Demo mode works without credentials. API keys stay in session memory and are not written to trip history.")
        if st.session_state.provider != "Demo mode":
            st.text_input("API key", type="password", key="api_key", help="Use a restricted key where possible. Never commit secrets to source control.")
            st.caption("The key is used only for AI requests in this running session.")
        st.selectbox("Travel mood", ["Any", "Beach", "Mountains", "Cultural", "Urban"], key="vibe")
        st.number_input("Trip duration (days)", min_value=1, max_value=14, step=1, key="duration")
        st.date_input("Start date", key="start_date", min_value=date.today())
        st.selectbox("Budget level", ["Budget", "Moderate", "Luxury"], key="budget")
        st.selectbox("Travel party", ["Solo", "Couple", "Family", "Friends"], key="party")
        st.selectbox("Pace", ["Relaxed", "Moderate", "Fast-Paced"], key="pace")
        st.multiselect("Interests", ["Food", "Adventure", "History", "Nightlife"], key="interests")
        st.markdown('<div class="small-note">Built-in demo catalog: Jaipur, Goa, Manali, Mumbai, Udaipur and Bali. Add a provider key for AI-enhanced suggestions.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "✦ Destination Recommender", "🗺️ Day-by-Day Itinerary", "🎛️ Vibe & Activity Swaps", "📚 Trip Vault & PDF"
    ])

    with tab1:
        st.subheader("Find the place that fits your kind of trip")
        left, right = st.columns([1.05, 1])
        with left:
            st.markdown("#### Do you have a destination in mind?")
            destination_options = ["Surprise me"] + [d["city"] for d in DESTINATIONS]
            selected = st.selectbox("Destination", destination_options, key="destination_choice")
            st.caption("Choose “Surprise me” to match your vibe, budget, season, and interests.")
            if st.button("Recommend destinations", type="primary", use_container_width=True):
                recs = recommend_destinations(st.session_state.vibe, st.session_state.budget, st.session_state.start_date, st.session_state.interests)
                st.session_state.recommendations = recs
        with right:
            st.markdown("#### Your travel profile")
            st.write(f"**Season:** {current_season(st.session_state.start_date)} · **Budget:** {st.session_state.budget}")
            st.write(f"**Mood:** {st.session_state.vibe} · **Interests:** {', '.join(st.session_state.interests) or 'Open to anything'}")
            st.write(f"**Party:** {st.session_state.party} · **Pace:** {st.session_state.pace}")
        if selected != "Surprise me":
            d = destination_by_city(selected)
            st.markdown(f"### {d['city']}, {d['country']}")
            st.markdown("".join(f'<span class="tag">{tag}</span>' for tag in d["tags"]), unsafe_allow_html=True)
            st.write(f"Best-fit mood: {', '.join(d['vibes'])}. Typical estimated daily spend starts around {d['symbol']}{d['base_daily']:,} before your selected budget adjustment.")
            if st.button(f"Build my {d['city']} itinerary", type="primary", key="build_fixed"):
                prefs = prefs_from_form()
                trip = generate_itinerary(d, prefs)
                if st.session_state.provider != "Demo mode" and st.session_state.api_key.strip():
                    with st.spinner("Polishing itinerary with your AI provider…"):
                        try:
                            trip = enrich_itinerary_with_ai(trip, st.session_state.provider, st.session_state.api_key.strip())
                        except Exception as exc:
                            st.warning(f"AI enhancement was skipped; demo itinerary is ready. Details: {exc}")
                st.session_state.trip = trip
                st.success("Itinerary created. Open the Day-by-Day tab to explore it.")
        recs = st.session_state.get("recommendations", [])
        if recs:
            st.markdown("### Your top 3 matches")
            cols = st.columns(3)
            for i, d in enumerate(recs):
                with cols[i]:
                    st.markdown(f"#### {i+1}. {d['city']}")
                    st.markdown("".join(f'<span class="tag">{tag}</span>' for tag in d["tags"]), unsafe_allow_html=True)
                    st.caption(f"{d['country']} · {d['budget']} leaning · {', '.join(d['season'])}")
                    st.write(f"**Travel mood:** {', '.join(d['vibes'])}")
                    if st.button(f"Plan {d['city']}", key=f"plan_{d['city']}", use_container_width=True):
                        st.session_state.trip = generate_itinerary(d, prefs_from_form())
                        st.success(f"{d['city']} plan created. Open the itinerary tab.")
        st.info("Season matching is a broad heuristic, not a weather forecast. Check the destination's local forecast before booking.")

    with tab2:
        st.subheader("Your itinerary, paced for real life")
        trip = st.session_state.trip
        if not trip:
            st.info("Create a trip in the Destination Recommender tab to see your day-by-day plan.")
        else:
            render_trip_summary(trip)
            st.markdown(f"### {trip['destination']} · {trip['preferences']['duration']} days")
            running = 0
            for day in trip["days"]:
                running += day["estimated_total"]
                with st.expander(f"Day {day['day']} · {day.get('date','')} — {trip['symbol']}{day['estimated_total']:,}", expanded=(day["day"] == 1)):
                    for activity in day["activities"]:
                        st.markdown(f"**{activity.get('time', SLOT_TIMES.get(activity['slot'],''))} · {activity['slot']}**")
                        st.markdown(f"#### {activity['name']}")
                        st.write(activity.get("description", ""))
                        st.caption(f"Activity: {trip['symbol']}{activity.get('cost',0):,} · Transit estimate: {trip['symbol']}{activity.get('transit_cost',0):,} · Total: {trip['symbol']}{activity.get('total_cost',0):,}")
                    st.divider()
                    st.write(f"Accommodation: **{trip['symbol']}{day['lodging_estimate']:,}** · Local transport: **{trip['symbol']}{day['transport_estimate']:,}**")
                    st.write(f"**Running trip total through this day:** {trip['symbol']}{running:,}")
                    st.caption(day.get("notes", ""))
            st.caption("Clustering uses approximate attraction coordinates and a nearest-neighbour heuristic. It is not a live route optimizer; check real travel times and traffic.")
            if st.button("Save current trip to Trip Vault", type="primary"):
                trips = load_trips()
                existing = next((i for i, item in enumerate(trips) if item.get("id") == trip["id"]), None)
                if existing is None: trips.insert(0, trip)
                else: trips[existing] = trip
                save_trips(trips)
                st.session_state.trips = trips
                st.session_state.last_saved_id = trip["id"]
                st.success("Trip saved locally.")

    with tab3:
        st.subheader("Tune the vibe without rebuilding the whole trip")
        trip = st.session_state.trip
        if not trip:
            st.info("Create an itinerary first, then swap an individual time slot or regenerate one day.")
        else:
            day_nums = [d["day"] for d in trip["days"]]
            day_number = st.selectbox("Choose a day", day_nums, format_func=lambda n: f"Day {n} · {trip['days'][n-1].get('date','')}")
            slot = st.selectbox("Time slot to customize", list(SLOT_TIMES.keys()))
            instruction = st.text_input("What would you like instead?", placeholder="e.g. outdoor market, vegetarian lunch, kid-friendly activity")
            st.caption("Only the selected slot is replaced; all other days and slots remain unchanged.")
            if st.button("Swap selected activity", type="primary"):
                try:
                    st.session_state.trip = regenerate_day(trip, day_number, slot, instruction, st.session_state.provider, st.session_state.api_key)
                    st.success("Activity swapped. Your other days were preserved.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not swap activity: {exc}")
            st.divider()
            regenerate_num = st.selectbox("Regenerate a single day", day_nums, key="regen_day")
            day_instruction = st.text_input("Day-level direction", placeholder="e.g. slower pace, more history, less walking", key="day_instruction")
            if st.button("Regenerate this day only"):
                try:
                    original = trip
                    replacement = generate_itinerary(destination_by_city(trip["destination"]), {
                        **trip["preferences"],
                        "start_date": date.fromisoformat(trip["preferences"]["start_date"]),
                        "duration": 1,
                    })
                    replacement_day = replacement["days"][0]
                    replacement_day["day"] = regenerate_num
                    replacement_day["date"] = original["days"][regenerate_num-1]["date"]
                    if day_instruction:
                        replacement_day["notes"] += f" Requested direction: {day_instruction}."
                    updated = json.loads(json.dumps(original))
                    updated["days"][regenerate_num-1] = replacement_day
                    updated["total_estimate"] = sum(d["estimated_total"] for d in updated["days"])
                    st.session_state.trip = updated
                    st.success(f"Day {regenerate_num} regenerated. Other days remain unchanged.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not regenerate day: {exc}")

    with tab4:
        st.subheader("Your Trip Vault")
        st.write("Trip history is stored in a local JSON file (`data/trips.json`) with no external database. On Streamlit Community Cloud, local files may reset across app restarts/redeploys; download a copy for durable backup.")
        trip = st.session_state.trip
        if trip:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("Save current trip", type="primary", use_container_width=True):
                    trips = load_trips()
                    idx = next((i for i, item in enumerate(trips) if item.get("id") == trip["id"]), None)
                    if idx is None: trips.insert(0, trip)
                    else: trips[idx] = trip
                    save_trips(trips)
                    st.session_state.trips = trips
                    st.success("Trip saved to local history.")
            with col_b:
                try:
                    pdf_bytes = make_pdf(trip)
                    st.download_button("⬇ Download offline PDF guide", data=pdf_bytes,
                        file_name=f"{trip['destination'].lower()}_travel_itinerary.pdf",
                        mime="application/pdf", use_container_width=True)
                except Exception as exc:
                    st.error(f"PDF export failed: {exc}")
            st.markdown("#### Current trip")
            st.write(f"**{trip['name']}** · {trip['country']} · {len(trip['days'])} days · {format_money(trip['total_estimate'], trip)}")
        st.divider()
        trips = load_trips()
        st.session_state.trips = trips
        if not trips:
            st.info("No saved trips yet. Create a trip and use Save current trip.")
        else:
            st.markdown(f"### Saved trip history ({len(trips)})")
            for item in trips:
                with st.expander(f"{item.get('name','Unnamed trip')} · {item.get('created_at','')} · {item.get('symbol','')}{item.get('total_estimate',0):,.0f}"):
                    st.write(f"{item.get('country','')} · {len(item.get('days', []))} days · ID: {item.get('id','')}")
                    a, b = st.columns(2)
                    with a:
                        if st.button("Load this trip", key=f"load_{item.get('id')}"):
                            st.session_state.trip = item
                            st.success("Trip loaded. Switch to the itinerary tab.")
                    with b:
                        try:
                            st.download_button("Export this trip PDF", data=make_pdf(item),
                                file_name=f"{item.get('destination','trip').lower()}_itinerary.pdf",
                                mime="application/pdf", key=f"pdf_{item.get('id')}")
                        except Exception as exc:
                            st.caption(f"PDF unavailable: {exc}")
            if st.button("Clear local trip history", type="secondary"):
                save_trips([])
                st.session_state.trips = []
                st.success("Local history cleared.")
                st.rerun()

    st.markdown("---")
    st.markdown('<div class="small-note">Travel responsibly · Estimates are illustrative · Verify local conditions, accessibility, safety guidance, and booking details before departure.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
