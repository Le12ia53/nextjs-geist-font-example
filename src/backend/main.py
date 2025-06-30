from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import uvicorn
from datetime import timedelta
from src.backend.auth import create_access_token, verify_token
from src.backend.database import SessionLocal, Pericia, StatusEnum, init_db
from sqlalchemy.orm import Session
from fastapi import status as http_status

app = FastAPI(title="Metrologi_IA Backend")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Initialize database
init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy user store for example
fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": "fakehashedpassword",
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

class Token(BaseModel):
    access_token: str
    token_type: str

class PericiaCreate(BaseModel):
    nome_fiscal: str
    peso: str
    validade: str
    destinatario: str
    numero_termo: str
    local_pericia: str
    endereco_pericia: str
    data_hora_pericia: str
    produto: str
    marca: str
    local_coleta: str
    endereco_coleta: str
    hora: str

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_dict["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/pericia/upload")
async def upload_pericia(file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(verify_token)):
    # TODO: Implement hybrid OCR processing with Google Vision and Tesseract
    # For now, just save file info and return
    return {"message": "File received", "filename": file.filename}

@app.get("/andamento/listar")
async def listar_andamento(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    pericias = db.query(Pericia).all()
    return pericias

@app.post("/andamento/atualizar")
async def atualizar_andamento(id: int, status: StatusEnum, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    pericia = db.query(Pericia).filter(Pericia.id == id).first()
    if not pericia:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Perícia not found")
    pericia.status = status
    db.commit()
    return {"message": "Status updated"}

@app.post("/ocr/processar")
async def processar_ocr():
    # TODO: Process OCR hybrid
    return {"message": "OCR processed"}

@app.post("/laudo/analisar")
async def analisar_laudo():
    # TODO: Analyze laudo and extract fields
    return {"message": "Laudo analyzed"}

@app.post("/decisao/gerar_boleto")
async def gerar_boleto():
    # TODO: Generate boleto with extracted data
    return {"message": "Boleto generated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
