from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/metrologi_ia")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StatusEnum(enum.Enum):
    aberto = "Em aberto"
    concluido = "Concluído"
    em_validacao = "Em validação"

class Pericia(Base):
    __tablename__ = "pericias"

    id = Column(Integer, primary_key=True, index=True)
    nome_fiscal = Column(String, index=True)
    peso = Column(String)
    validade = Column(String)
    destinatario = Column(String)
    numero_termo = Column(String)
    local_pericia = Column(String)
    endereco_pericia = Column(String)
    data_hora_pericia = Column(String)
    produto = Column(String)
    marca = Column(String)
    local_coleta = Column(String)
    endereco_coleta = Column(String)
    hora = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.aberto)
    data_criacao = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)
