from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://rupeshvn:gunner@postgres-postgresql:5432/stocksdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)