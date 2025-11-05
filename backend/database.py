import json
import os
from typing import List, Dict, Any

JSON_FILE = "students.json"

def read_students() -> List[Dict[str, Any]]:
    """Read students from JSON file"""
    try:
        # Check if the file exists and is not empty
        if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
            with open(JSON_FILE, 'r') as f:
                # Handle case where file exists but is empty/invalid JSON
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Warning: students.json exists but is empty or invalid. Returning empty list.")
                    return []
        return []
    except Exception as e:
        print(f"Error reading students: {e}")
        return []

def write_students(students: List[Dict[str, Any]]) -> bool:
    """Write students to JSON file"""
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(students, f, indent=4)
        return True
    except Exception as e:
        print(f"Error writing students: {e}")
        return False

def get_next_id() -> str:
    """Generate a simple ID for new students"""
    students = read_students()
    if not students:
        return "1"
    
    # Ensure all IDs are integers before finding max
    try:
        max_id = max(int(student.get('id', 0)) for student in students)
        return str(max_id + 1)
    except ValueError:
        # Handle case where IDs might not be convertible to int
        print("Warning: Non-integer IDs found. Falling back to ID '1'.")
        return "1"