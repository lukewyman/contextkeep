"""
FastAPI application setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.projects.api import router as projects_router

app = FastAPI(
    title="ContextKeep API",
    description="Backend API for ContextKeep IDE",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server (CRA)
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api", tags=["projects"])


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "ContextKeep API"}