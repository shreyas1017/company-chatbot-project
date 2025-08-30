# app/routers/documents.py

import shutil
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from .. import models, crud, security
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/routers/documents.py

# ... (keep all the imports)

# ... (keep the get_db function)

@router.post("/upload")
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_admin: dict = Depends(security.get_current_admin_user),
    db: Session = Depends(get_db)
):
    company_id = current_admin["company_id"]

    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_document = models.Document(
        filename=file.filename,
        company_id=company_id,
        status='processing'
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    from ..processing import process_and_store_document
    # Update this call to pass the filename
    background_tasks.add_task(
        process_and_store_document,
        file_path=temp_file_path,
        filename=file.filename, # Pass the original filename
        company_id=company_id,
        document_id=db_document.id
    )

    return {
        "message": "File uploaded and processing has started.",
        "document_id": db_document.id,
        "filename": file.filename
    }