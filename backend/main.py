from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import Student, StudentUpdate
from database import read_students, write_students, get_next_id
import os

app = FastAPI(title="Student Management System")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current directory path (backend folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the parent and then into the frontend folder
frontend_dir = os.path.join(current_dir, '..', 'frontend')

# Routes
@app.get("/")
def read_idex():

    index_path = os.path.join(frontend_dir, 'index.html') 
    
    if not os.path.exists(index_path):
        raise HTTPException(status_code=500, detail=f"Frontend index file not found at: {index_path}")
        
    return FileResponse(index_path)

@app.get("/students")
def get_all_students():
    return read_students()
    

@app.post("/students")
def create_students(student: Student):
    """Create a new student"""
    students = read_students()
    
    new_student = student.dict()
    new_student['id'] = get_next_id()
    
    students.append(new_student)
    
    if write_students(students):
        return new_student
    else:
        raise HTTPException(status_code=500, detail="Failed to save student")

@app.put("/students/{student_id}")
async def update_student(student_id: str, student_update: StudentUpdate):
    """Update a student"""
    students = read_students()
    # find student to update
    student_index = None
    for i, student in enumerate(students):
        if student.get('id') == student_id:
            student_index = i
            break
    
    if student_index is None:
        raise HTTPException(status_code=404, detail="Student not found")
        
    # update the student
    update_data = {k: v for k, v in student_update.dict().items() if v is not None}
    students[student_index].update(update_data)
    
    if write_students(students):
        return students[student_index]
    else:
        raise HTTPException(status_code=500, detail="Failed to update student")
    
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    """Delete a student"""
    students = read_students()
    # find student to delete
    new_students = [student for student in students if student.get('id') != student_id]
    
    # Check if student was found and deleted
    if len(new_students) == len(students):
        raise HTTPException(status_code=404, detail="Student not found")
        
    if write_students(new_students):
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete student")
    

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 and use PORT from the environment for platform compatibility (e.g., Railway)
    uvicorn.run(app, host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 8000)))