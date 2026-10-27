
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Student API")
students = []
next_id = 1

class Student(BaseModel):
    name: str = Field(min_length=2)
    roll_no: str = Field(min_length=3)
    marks: float = Field(ge=0, le=100)

@app.get("/")
def home():
    return {"message": "Student API is running"}

@app.get("/students")
def get_students():
    return students

@app.post("/students", status_code=201)
def add_student(s: Student):
    global next_id
    if any(x["roll_no"] == s.roll_no for x in students):
        raise HTTPException(409, "Roll number already exists")
    record = {"id": next_id, **s.model_dump()}
    students.append(record)
    next_id += 1
    return record

@app.get("/students/{sid}")
def get_student(sid: int):
    for s in students:
        if s["id"] == sid:
            return s
    raise HTTPException(404, "Student not found")

@app.put("/students/{sid}")
def update_student(sid: int, data: Student):
    for s in students:
        if s["id"] == sid:
            if any(x["roll_no"] == data.roll_no and x["id"] != sid for x in students):
                raise HTTPException(409, "Roll number already exists")
            s.update(data.model_dump())
            return s
    raise HTTPException(404, "Student not found")

@app.delete("/students/{sid}")
def delete_student(sid: int):
    for s in students:
        if s["id"] == sid:
            students.remove(s)
            return {"message": "Student deleted"}
    raise HTTPException(404, "Student not found")
