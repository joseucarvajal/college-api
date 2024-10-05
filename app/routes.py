from fastapi import APIRouter, HTTPException
from app.models import CourseCreate, Course
from app.database import get_db_connection

router = APIRouter()

@router.post("/courses/", response_model=Course)
def create_course(course: CourseCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO courses (name, start_date, end_date, cut1_percentage, cut2_percentage, cut3_percentage)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (course.name, course.start_date, course.end_date, course.cut1_percentage, course.cut2_percentage, course.cut3_percentage)
        
        cursor.execute(query, values)
        conn.commit()
        
        course_id = cursor.lastrowid
        return Course(id=course_id, **course.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/courses/", response_model=list[Course])
def list_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM courses"
        cursor.execute(query)
        courses = cursor.fetchall()
        return [Course(**course) for course in courses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()