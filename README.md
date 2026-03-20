# Medical Appointment System

**MediCare Clinic API** is a FastAPI backend project to manage doctors, appointments, and consultations. It demonstrates real-world API development skills including validation, CRUD, filters, search, sorting, and pagination.

> Developed during the **Innomatics Research Labs FastAPI Internship**.

## Features
- Manage doctors: add, update, delete, check availability  
- Manage appointments: schedule, confirm, cancel, complete  
- Filter doctors by specialization, fee, experience, availability  
- Search & sort doctors and appointments  
- Pagination for large lists  
- Senior citizen discount on appointments  
- Fully documented API via Swagger UI

## Technologies
- Python 3.x  
- FastAPI  
- Pydantic  
- Uvicorn (server)  
- Swagger UI (interactive API docs)

## Setup & Run
1. Clone repo  
2. Create & activate virtual environment  
3. Install dependencies (`pip install -r requirements.txt`)  
4. Run FastAPI (`uvicorn main:app --reload`)  
5. Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Doctors
- `GET /doctors` – List all doctors  
- `GET /doctors/{doctor_id}` – Get doctor by ID  
- `POST /doctors` – Add new doctor  
- `PUT /doctors/{doctor_id}` – Update doctor  
- `DELETE /doctors/{doctor_id}` – Delete doctor  
- `GET /doctors/filter` – Filter doctors  
- `GET /doctors/search` – Search doctors  
- `GET /doctors/sort` – Sort doctors  
- `GET /doctors/page` – Paginate doctors  
- `GET /doctors/browse` – Filter + sort + paginate  

### Appointments
- `GET /appointments` – List all appointments  
- `POST /appointments` – Schedule appointment  
- `POST /appointments/{appointment_id}/confirm` – Confirm appointment  
- `POST /appointments/{appointment_id}/cancel` – Cancel appointment  
- `POST /appointments/{appointment_id}/complete` – Complete appointment  
- `GET /appointments/active` – Active appointments  
- `GET /appointments/by-doctor/{doctor_id}` – Appointments by doctor  
- `GET /appointments/search` – Search appointments  
- `GET /appointments/sort` – Sort appointments  
- `GET /appointments/page` – Paginate appointments  

## Author
**Pradnya Kate** – BBA-CA Graduate | MCA Student | FastAPI Intern  
> Internship done at **Innomatics Research Labs**

