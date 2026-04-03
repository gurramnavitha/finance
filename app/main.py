from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, user, finance, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Data Processing API",
    description="Role-based financial records management",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(finance.router, prefix="/records", tags=["Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "Welcome to the Finance API"}
