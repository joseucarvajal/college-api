from fastapi import FastAPI
from app.routes import router
from pydantic import BaseModel, Field
from datetime import date

# Esta clase ya se ha definido en models.py, por lo que se puede eliminar de aquí.
# Si es necesario usarla, se debe importar desde models.py
from app.models import CourseCreate

app = FastAPI()

app.include_router(router)