from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import llamalense
import logging

logger = logging.getLogger("uvicorn")
app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for sessions
SESSIONS = {}
UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Restrict file formats
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(
            status_code=400, detail="Invalid file format. Only PDF and DOCX files are allowed."
        )

    # Save file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Simulate document processing
    session_id = len(SESSIONS) + 1
    SESSIONS[session_id] = {"document_path": file_path, "conversation": []}

    if llamalense.app_main(file_path=file_path):
        return {"session_id": session_id, "message": "Document processed. You can start asking questions."}
    return {"session_id": session_id, "message": "Something went wrong!"}


@app.post("/query/")
async def chat(request: Request):
    try:
        input_data = await request.json()
        session_id = input_data["session_id"]
        question = input_data["question"]

        if session_id not in SESSIONS:
            raise HTTPException(status_code=400, detail="Invalid session. Please upload a document first.")

        # Handle "/bye" to reset the session
        if question.strip().lower() == "bye":
            del SESSIONS[session_id]
            return {"message": "Session reset. Please upload a new document to start over."}

        # Simulate chatbot response
        response = llamalense.app_get_ans(question)
        session_data = SESSIONS[session_id]
        session_data["conversation"].append({"user": question, "bot": response})

        return {"message": response}

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")


@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot API!"}

