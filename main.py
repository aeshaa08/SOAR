from fastapi import FastAPI
import hashlib
import os
from datetime import datetime

app = FastAPI()


FIRMWARE_FILE = "firmware.bin"
SIGNATURE_FILE = "firmware.sig"


firmware_info = {
    "version": "1.0.0",
    "release_date": str(datetime.now()),
    "hash": "",
    "signature_file": SIGNATURE_FILE
}

security_logs = []


def generate_hash(filename):

    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as f:
        data = f.read()

    return hashlib.sha256(data).hexdigest()


@app.get("/")
def home():
    return {
        "status": "Secure OTA Server Running"
    }


@app.get("/firmware/latest")
def get_latest_firmware():

    firmware_hash = generate_hash(FIRMWARE_FILE)

    if firmware_hash is None:
        return {
            "error": "Firmware file not found"
        }

    firmware_info["hash"] = firmware_hash

    return {
        "message": "Latest firmware available",
        "firmware": firmware_info
    }


@app.get("/firmware/download")
def download_firmware():

    if not os.path.exists(FIRMWARE_FILE):
        return {
            "error": "Firmware file not found"
        }

    return {
        "firmware_file": FIRMWARE_FILE,
        "signature_file": SIGNATURE_FILE,
        "hash": generate_hash(FIRMWARE_FILE)
    }

@app.post("/security/log")
def add_security_log(data: dict):

    log = {
        "timestamp": str(datetime.now()),
        "device_id": data.get("device_id"),
        "event": data.get("event"),
        "status": data.get("status")
    }

    security_logs.append(log)

    return {
        "message": "Security log stored successfully",
        "log": log
    }

@app.get("/security/logs")
def get_logs():
    return security_logs