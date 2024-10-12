from fastapi import APIRouter, HTTPException
from app.models import CourseCreate, Course, StudentCreate, Student
from app.database import get_db_connection
from typing import List

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

@router.post("/courses/{course_id}/students/", response_model=List[Student])
def create_students_bulk(course_id: int, students: List[StudentCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si el curso existe
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        created_students = []
        for student in students:
            query = """
            INSERT INTO students (code, full_name, emails, course_id)
            VALUES (%s, %s, %s, %s)
            """
            values = (student.code, student.full_name, student.emails, course_id)
            
            cursor.execute(query, values)
            student_id = cursor.lastrowid
            created_students.append(Student(id=student_id, course_id=course_id, **student.dict()))
        
        conn.commit()
        return created_students
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
