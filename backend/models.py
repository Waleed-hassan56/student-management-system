from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Student(BaseModel):
    name: str
    age : int
    grade : str 
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    enrollment_date : str = datetime.now().strftime("%Y-%m-%d")

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age : Optional[int] = None
    grade : Optional[str] = None 
    email: Optional[str] = None
    phone: Optional[str] = None
    enrollment_date: Optional[str] = None