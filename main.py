from fastapi import FastAPI

app = FastAPI()

alerts = []

def get_risk_score(severity):

    if severity == "high":
        return "High"

    elif severity == "medium":
        return "Medium"

    return "Low"


@app.get("/")
def home():
    return {"status": "SOAR Running"}


@app.post("/alert")
def alert(data: dict):

    normalized_alert = {
        "source_ip": data.get("src_ip"),
        "severity": data.get("severity"),
        "timestamp": data.get("time"),
        "alert_type": data.get("alert_type")
    }

    # Add risk score
    normalized_alert["risk_score"] = get_risk_score(
        normalized_alert["severity"]
    )

    alerts.append(normalized_alert)

    return {
        "message": "Alert Saved",
        "normalized_alert": normalized_alert
    }


@app.get("/alerts")
def get_alerts():
    return alerts