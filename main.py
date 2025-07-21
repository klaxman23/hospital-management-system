from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# In-memory "database" for demonstration purposes
# In a real application, you'd use a proper database (e.g., PostgreSQL, MongoDB)
patients_db: List[Dict] = []

class Patient(BaseModel):
    patient_name: str
    patient_age: int
    patient_date_of_birth: str  # Consider using datetime.date for better date handling
    patient_disease: str
    patient_gender: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Hospital Management System API"}

@app.post("/patients/", response_model=Patient, status_code=201)
async def create_patient(patient: Patient):
    """
    Adds a new patient to the system.
    """
    patients_db.append(patient.dict())
    return patient

@app.get("/patients/", response_model=List[Patient])
async def get_all_patients():
    """
    Retrieves all registered patients.
    """
    return patients_db

@app.get("/patients/{patient_name}", response_model=Patient)
async def get_patient_by_name(patient_name: str):
    """
    Retrieves a patient by their name.
    """
    for patient in patients_db:
        if patient["patient_name"].lower() == patient_name.lower():
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

# To run the application:
# uvicorn main:app --reload