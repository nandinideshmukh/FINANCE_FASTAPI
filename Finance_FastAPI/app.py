from fastapi import FastAPI, Depends, HTTPException
from routes import users , records,dashboard
from db.create_db import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Finance Management API",
              version = "1.0.0",
              description="API for managing financial data with role-based access control")

app.router.include_router(users.router)
app.router.include_router(records.router)
app.router.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance Management API!"}
