from fastapi import FastAPI

app = FastAPI()

alerts = []

@app.get("/")
def home():
    return {"status": "SOAR Running"}

@app.post("/alert")
def alert(data: dict):

    alerts.append(data)

    return {
        "message": "Alert Saved",
        "data": data
    }

@app.get("/alerts")
def get_alerts():
    return alerts