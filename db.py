# db.py
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DB_URL", "sqlite:///chatlogs.db")

# Verifica se o banco de dados SQLite é gravável
if DB_URL.startswith("sqlite:///"):
    db_path = DB_URL.replace("sqlite:///", "")
    if not os.access(os.path.dirname(db_path) or ".", os.W_OK):
        raise PermissionError(f"Sem permissão de escrita no diretório do banco de dados: {os.path.dirname(db_path) or '.'}")

engine  = create_engine(DB_URL, echo=False)
Base    = declarative_base()
Session = sessionmaker(bind=engine)

class Message(Base):
    __tablename__ = "messages"
    id, role, content = Column(Integer, primary_key=True), Column(Text), Column(Text)
    timestamp         = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
