from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from .database import engine, SessionLocal
from .models import Base, Service
from .schemas import ServiceCreate
from .monitor import check_service
from .models import Base, Service, ServiceCheck

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PulseWatch Monitoring Platform")

scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.start()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def dashboard():
    return FileResponse("static/dashboard.html")


@app.post("/services")
def add_service(service: ServiceCreate, db: Session = Depends(get_db)):
    existing = db.query(Service).filter(Service.url == service.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Service already exists")

    new_service = Service(
        name=service.name,
        url=service.url,
        status="UNKNOWN",
        response_time=None
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    scheduler.add_job(
        check_service,
        trigger="interval",
        seconds=10,
        id=f"service_{new_service.id}",
        replace_existing=True,
        args=[new_service.id]
    )

    return new_service


@app.get("/services")
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    job_id = f"service_{service_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    db.delete(service)
    db.commit()

    return {"message": "Service deleted"}


@app.get("/services/{service_id}/history")
def get_service_history(service_id: int, db: Session = Depends(get_db)):
    history = (
        db.query(ServiceCheck)
        .filter(ServiceCheck.service_id == service_id)
        .order_by(ServiceCheck.id.asc())
        .all()
    )

    return history