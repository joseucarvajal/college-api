from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class CourseCreate(BaseModel):
    name: str = Field(..., description="Nombre del curso (campo requerido)")
    start_date: date
    end_date: date
    cut1_percentage: float
    cut2_percentage: float
    cut3_percentage: float

class Course(CourseCreate):
    id: int

class StudentCreate(BaseModel):
    code: str = Field(..., description="Código del estudiante (campo requerido)")
    full_name: str = Field(..., description="Nombre completo del estudiante (campo requerido)")
    emails: str = Field(..., description="Correos electrónicos del estudiante (campo requerido)")

class Student(StudentCreate):
    id: int
    course_id: int
