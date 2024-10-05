from pydantic import BaseModel
from datetime import date

class CourseCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    cut1_percentage: float
    cut2_percentage: float
    cut3_percentage: float

class Course(CourseCreate):
    id: int