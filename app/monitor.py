import time
import requests
from datetime import datetime

from .database import SessionLocal
from .models import Service, ServiceCheck


def check_service(service_id: int):
    db = SessionLocal()

    try:
        service = db.query(Service).filter(Service.id == service_id).first()

        if not service:
            print(f"[Monitor] Service {service_id} not found")
            return

        print(f"[Monitor] Checking {service.name} - {service.url}")

        start = time.time()
        status = "DOWN"
        response_time = None

        try:
            response = requests.get(
                service.url,
                timeout=5,
                allow_redirects=True,
                headers={"User-Agent": "PulseWatch/1.0"}
            )

            response_time = round(time.time() - start, 3)

            if 200 <= response.status_code < 400:
                status = "UP"
            else:
                status = "DOWN"

        except Exception as e:
            print(f"[Monitor] Error checking {service.name}: {e}")
            status = "DOWN"
            response_time = None

        service.status = status
        service.response_time = response_time

        history = ServiceCheck(
            service_id=service.id,
            status=status,
            response_time=response_time,
            checked_at=datetime.now().strftime("%H:%M:%S")
        )

        db.add(history)
        db.commit()

        print(f"[Monitor] {service.name} is {status} ({response_time}s)")

    finally:
        db.close()