import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
from flask import Flask, Response

app = Flask(__name__)

@app.route("/forex_usd_news.ics")
def forex_calendar():
    url = "https://www.forexfactory.com/calendar?week=this"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    cal = Calendar()

    for row in soup.select("tr.calendar__row"):
        currency = row.select_one(".calendar__currency")
        impact = row.select_one(".calendar__impact span")
        event = row.select_one(".calendar__event-title")
        time = row.select_one(".calendar__time")

        if not currency or not impact or not event or not time:
            continue

        currency = currency.get_text(strip=True)
        impact_title = impact.get("title", "")
        event_name = event.get_text(strip=True)
        event_time = time.get_text(strip=True)

        # Only USD & High/Medium
        if currency == "USD" and ("High" in impact_title or "Medium" in impact_title):
            e = Event()
            e.name = f"{impact_title} Impact: {event_name}"
            
            # ⚠️ NOTE: Parsing time needs refinement, placeholder example
            e.begin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            e.duration = timedelta(minutes=30)
            
            cal.events.add(e)

    return Response(str(cal), mimetype="text/calendar")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
