# Personalized Travel Itinerary Planner
**Skill Wallet Capstone Project 4** — a modular Streamlit travel-planning SaaS prototype.

## Features
- Preference panel: mood, dates, duration, budget, party, pace, interests.
- Smart top-three destination matching from a built-in demo catalog.
- Day-by-day itineraries with time slots, indicative activity costs, daily totals, and USD/INR reference conversions.
- Approximate geographic distance heuristic and activity clustering.
- Single-slot swaps and single-day regeneration that preserve the rest of the itinerary.
- Local JSON trip history and downloadable PDF guide with emergency checklist.
- Demo mode works without API credentials; optional Gemini and Groq providers can enrich itinerary content.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

## AI configuration
Choose **Gemini** or **Groq** in the sidebar and enter an API key in the password field. The app uses session state and does not write the key to `data/trips.json`. Use environment-managed secrets for production deployments where possible. Never commit secrets.

You can alternatively add keys in Streamlit secrets and adapt the sidebar to read `st.secrets`; this starter deliberately keeps the API-key entry simple for a capstone demo.

## Deploy to Streamlit Community Cloud
1. Push `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Create a new app in Streamlit Community Cloud and select `app.py`.
3. Deploy. No database service is required.
4. The app creates `data/trips.json` on first save.

## Architecture notes
- `app.py` keeps UI, domain logic, local persistence, AI adapters, and PDF generation in clearly separated functions for easy capstone review.
- Destination data and currency rates are static demo data. Costs, season tags, and attractions are illustrative, not live inventory or weather data.
- Local JSON storage is appropriate for a single-user prototype. Streamlit Community Cloud files may not be durable across restarts/redeploys; production multi-user persistence requires an external database/object store and authentication.
- Attraction coordinates are approximate. The route heuristic estimates relative proximity but is not a turn-by-turn route engine and does not account for roads, transit schedules, traffic, or accessibility.
- Do not present estimates as confirmed prices. Verify entry fees, opening times, transport, weather, visas, and safety information before travel.

## Security and production hardening checklist
- Add authentication and per-user authorization before storing personal trip details.
- Use managed secrets/environment variables, not user-entered long-lived keys, for team deployments.
- Add API quotas, retries, timeouts, structured logging, and content validation.
- Replace static FX values and demo catalog with trusted live providers where needed.
- Add automated tests for itinerary invariants, persistence, PDF generation, and provider failures.
- Use persistent storage for durable trip history and backups.
