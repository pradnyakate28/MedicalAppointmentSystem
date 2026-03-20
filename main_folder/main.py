from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, constr, conint
from typing import Optional
import math

# Day 1 - Initialize app
app = FastAPI(title="MediCare Clinic API")

# Day 1 - Task 2: Doctors list
doctors = [
    {
        "id":1, "name":"Dr.Rahul Kulkarni",
        "specialization":"Cardiologist", 
        "fee":500,
        "experience_years":5,
        "is_available": True
    },
    {
        "id":2, "name":"Dr.Anjali Singh", 
        "specialization":"Dermatologist",
        "fee":300,
        "experience_years":3,
        "is_available": False
    },
    {
        "id":3, "name":"Dr.Arohi Sharma", 
        "specialization":"Pediatrician",
        "fee":600, 
        "experience_years":8,
        "is_available": True
    },
    {
        "id":4,
        "name":"Dr.Arjun Patil",
        "specialization":"General",
        "fee":100,
        "experience_years":1,
        "is_available": False
    },
    {
        "id":5,
        "name":"Dr.Amit Shah",
        "specialization":"Cardiologist",
        "fee":700, 
        "experience_years":10,
        "is_available": True
    },
    {
        "id":6, 
        "name":"Dr.Sneha Deshmukh", 
        "specialization":"Dermatologist",
        "fee":350,
        "experience_years":4, 
        "is_available": False
    }
]

appointments = []
appt_counter = 1

# Day 3 - Helper functions
def find_doctor(doctor_id: int):
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(base_fee: int, appointment_type: str, senior_citizen: bool = False):
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:  # in-person
        fee = base_fee
    if senior_citizen:
        fee = fee * 0.85  # 15% discount
    return round(fee, 2)

def filter_doctors_logic(specialization: Optional[str], max_fee: Optional[int], min_experience: Optional[int], is_available: Optional[bool]):
    filtered = doctors
    if specialization is not None:
        filtered = [d for d in filtered if d["specialization"].lower() == specialization.lower()]
    if max_fee is not None:
        filtered = [d for d in filtered if d["fee"] <= max_fee]
    if min_experience is not None:
        filtered = [d for d in filtered if d["experience_years"] >= min_experience]
    if is_available is not None:
        filtered = [d for d in filtered if d["is_available"] == is_available]
    return filtered

# Day 1 - Task 1: Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}

# Day 1 - Task 2: GET all doctors
@app.get("/doctors")
def get_doctors():
    available_count = sum(1 for d in doctors if d["is_available"])
    return {"doctors": doctors, "total": len(doctors), "available_count": available_count}

# Day 1 - Task 5: Doctors summary
@app.get("/doctors/summary")
def doctors_summary():
    total_doctors = len(doctors)
    available_count = sum(1 for d in doctors if d["is_available"])
    most_experienced = max(doctors, key=lambda d: d["experience_years"])["name"]
    cheapest_fee = min(d["fee"] for d in doctors)
    specialization_count = {}
    for d in doctors:
        specialization_count[d["specialization"]] = specialization_count.get(d["specialization"], 0) + 1
    return {
        "total_doctors": total_doctors,
        "available_count": available_count,
        "most_experienced_doctor": most_experienced,
        "cheapest_consultation_fee": cheapest_fee,
        "doctors_per_specialization": specialization_count
    }

# Day 6 - Task 16 - search doctor
@app.get("/doctors/search")
def search_doctors(keyword: str = Query(..., min_length=1)):
    matches = [d for d in doctors if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    return {"matches": matches, "total_found": len(matches)}

# Day 6 - Task 17 - sort doctor
@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee", order: str = "asc"):
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")
    sorted_list = sorted(doctors, key=lambda d: d[sort_by], reverse=(order=="desc"))
    return {"sorted_doctors": sorted_list, "sort_by": sort_by, "order": order}

# Day 6 - Task 18 - Paginate Doctors
@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    total_pages = math.ceil(len(doctors)/limit)
    start = (page-1)*limit
    end = start + limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "doctors": doctors[start:end]}

# Day 3 - Task 10: GET /doctors/filter
@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
):
    filtered = filter_doctors_logic(specialization, max_fee, min_experience, is_available)
    return {"filtered_doctors": filtered, "total": len(filtered)}

# Day 6 - Task 20 -  Browse
@app.get("/doctors/browse")
def browse_doctors(
    keyword: Optional[str] = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors
    if keyword:
        result = [d for d in result if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")
    result.sort(key=lambda d: d[sort_by], reverse=(order=="desc"))
    total_pages = math.ceil(len(result)/limit)
    start = (page-1)*limit
    end = start + limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "results": result[start:end]}
    
# Day 1 - Task 3: GET doctor by ID
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if doctor:
        return {"doctor": doctor}
    raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found")

# Day 1 - Task 4: GET appointments
@app.get("/appointments")
def get_appointments():
    return {"appointments": appointments, "total": len(appointments)}

# Day 2/3 - AppointmentRequest Model and POST
class AppointmentRequest(BaseModel):
    patient_name: constr(min_length=2)
    doctor_id: conint(gt=0)
    date: constr(min_length=8)
    reason: constr(min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False  # Task 9

@app.post("/appointments")
def create_appointment(request: AppointmentRequest):
    global appt_counter
    doctor = find_doctor(request.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail=f"Doctor with id {request.doctor_id} not found")
    if not doctor["is_available"]:
        raise HTTPException(status_code=400, detail=f"Doctor {doctor['name']} is not available")
    fee = calculate_fee(doctor["fee"], request.appointment_type, request.senior_citizen)
    appointment = {
        "appointment_id": appt_counter,
        "patient_name": request.patient_name,
        "doctor_name": doctor["name"],
        "date": request.date,
        "appointment_type": request.appointment_type,
        "original_fee": doctor["fee"],
        "calculated_fee": fee,
        "status": "scheduled"
    }
    appointments.append(appointment)
    appt_counter += 1
    return {"message": "Appointment created successfully", "appointment": appointment}

# Day 4 - Task 11: Add new doctor
class NewDoctor(BaseModel):
    name: constr(min_length=2)
    specialization: constr(min_length=2)
    fee: conint(gt=0)
    experience_years: conint(gt=0)
    is_available: bool = True

@app.post("/doctors", status_code=201)
def add_doctor(new_doc: NewDoctor):
    if any(d["name"].lower() == new_doc.name.lower() for d in doctors):
        raise HTTPException(status_code=400, detail="Doctor with this name already exists")
    doctor = new_doc.dict()
    doctor["id"] = max(d["id"] for d in doctors) + 1
    doctors.append(doctor)
    return {"message": "Doctor added", "doctor": doctor}

# Day 4 - Task 12: Update doctor
@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: Optional[int] = None, is_available: Optional[bool] = None):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if fee is not None:
        doctor["fee"] = fee
    if is_available is not None:
        doctor["is_available"] = is_available
    return {"message": "Doctor updated", "doctor": doctor}

# Day 4 - Task 13: Delete doctor
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if any(a for a in appointments if a.get("doctor_name") == doctor["name"] and a["status"] == "scheduled"):
        raise HTTPException(status_code=400, detail="Cannot delete doctor with scheduled appointments")
    doctors.remove(doctor)
    return {"message": "Doctor deleted"}

# Day 6 - Task 19–20: Search,Sort, Pagination
@app.get("/appointments/search")
def search_appointments(patient_name: str = Query(..., min_length=1)):
    matches = [a for a in appointments if patient_name.lower() in a["patient_name"].lower()]
    return {"appointments": matches, "total_found": len(matches)}

@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "calculated_fee", order: str = "asc"):
    if sort_by not in ["calculated_fee", "date"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    sorted_list = sorted(appointments, key=lambda a: a[sort_by], reverse=(order=="desc"))
    return {"sorted_appointments": sorted_list, "sort_by": sort_by, "order": order}

@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 3):
    total_pages = math.ceil(len(appointments)/limit)
    start = (page-1)*limit
    end = start + limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "appointments": appointments[start:end]}

# Day 5 - Task 14: Confirm / Cancel appointment
@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "confirmed"
            return {"message": "Appointment confirmed", "appointment": appt}
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "cancelled"
            # Make doctor available again
            doc = find_doctor(next(d["id"] for d in doctors if d["name"] == appt["doctor_name"]))
            if doc:
                doc["is_available"] = True
            return {"message": "Appointment cancelled", "appointment": appt}
    raise HTTPException(status_code=404, detail="Appointment not found")

# Day 5 - Task 15: Complete appointment + Active + by-doctor
@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "completed"
            return {"message": "Appointment completed", "appointment": appt}
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.get("/appointments/active")
def get_active_appointments():
    active = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]
    return {"active_appointments": active, "total": len(active)}

@app.get("/appointments/by-doctor/{doctor_id}")
def get_appointments_by_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor_appts = [a for a in appointments if a["doctor_name"] == doctor["name"]]
    return {"appointments": doctor_appts, "total": len(doctor_appts)}

