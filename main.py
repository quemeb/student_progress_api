from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# ✅ Allow only your frontend to access the API
origins = [
    "https://student-progress-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "API is running."}

@app.get("/get_student_progress")
def get_student_progress(email: str, student_id: str):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = """
            SELECT * FROM student_progress_view
            WHERE calbright_email = %s AND ccc_id = %s
        """
        cur.execute(query, (email, student_id))
        row = cur.fetchone()
        columns = [desc[0] for desc in cur.description] if row else []
        cur.close()
        conn.close()
        return dict(zip(columns, row)) if row else {"message": "Student not found or ID does not match."}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

