from fastapi import FastAPI, Query, Body, HTTPException
from datetime import datetime
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Age Calculator API", version="1.0")

Instrumentator().instrument(app).expose(app)

class AgeRequest(BaseModel):
    birth_date: str

def calculete_age(birth_date: str):
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        now = datetime.now()

        if birth > now:
            raise HTTPException(status_code=400, detail="Дата рождения не может быть в будущем")

        delta = now - birth

        seconds = delta.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = delta.days
        months = days / 30.44

        return {
            "birth_date": birth_date,
            "age_in_seconds": round(seconds),
            "age_in_minutes": round(minutes),
            "age_in_hours": round(hours),
            "age_in_days": days,
            "age_in_months": round(months),
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")

@app.get("/age")
def get_age(
    birth_date: str = Query(..., description="Дата рождения в формате YYYY-MM-DD")
):
    return calculete_age(birth_date)

@app.post("/age")
def post_age(
    request: AgeRequest
):
    return calculete_age(request.birth_date)