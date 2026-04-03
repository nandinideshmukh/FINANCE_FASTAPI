from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv,os
dotenv.load_dotenv()

sql_url = os.getenv("SQL_URL") 
engine = create_engine(sql_url, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    except Exception as e:
        print(f"Database error: {e}")
        raise 
    finally:
        db.close()
        
# https://dev.to/bkhalifeh/fastapi-performance-the-hidden-thread-pool-overhead-you-might-be-missing-2ok6