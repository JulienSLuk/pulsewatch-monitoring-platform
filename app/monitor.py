import time
import requests

from .database import SessionLocal
from .models import Service


def check_service(service_id: int):
    db = SessionLocal()

    try:
        service = db.query(Service).filter(Service.id == service_id).first()

        if not service:
            print(f"[Monitor] Service {service_id} not found")
            return

        print(f"[Monitor] Checking {service.name} - {service.url}")

        start = time.time()

        try:
            response = requests.get(
                service.url,
                timeout=5,
                allow_redirects=True,
                headers={"User-Agent": "PulseWatch/1.0"}
            )

            duration = round(time.time() - start, 3)

            if 200 <= response.status_code < 400:
                service.status = "UP"
                service.response_time = duration
                print(f"[Monitor] {service.name} is UP ({duration}s)")
            else:
                service.status = "DOWN"
                service.response_time = duration
                print(f"[Monitor] {service.name} is DOWN (status {response.status_code})")

        except Exception as e:
            service.status = "DOWN"
            service.response_time = None
            print(f"[Monitor] Error checking {service.name}: {e}")

        db.commit()

    finally:
        db.close()