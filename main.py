from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "API is running."}

@app.get("/get_student_progress")
def get_student_progress(email: str):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    query = """
        SELECT * FROM student_progress_view
        WHERE calbright_email = %s
    """
    cur.execute(query, (email,))
    row = cur.fetchone()

    columns = [desc[0] for desc in cur.description] if row else []
    cur.close()
    conn.close()

    if row:
        return dict(zip(columns, row))
    else:
        return {"message": "Student not found."}
