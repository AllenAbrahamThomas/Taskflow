from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import SessionLocal
from app.db.seed import seed_db

# Import routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events. Runs database seed on application startup.
    """
    db = SessionLocal()
    try:
        seed_db(db)
    except Exception as e:
        print(f"Failed to seed database on startup: {e}")
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual Next.js domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API routes
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(projects_router, prefix=f"{settings.API_V1_STR}/projects", tags=["Projects"])
app.include_router(tasks_router, prefix=f"{settings.API_V1_STR}/tasks", tags=["Tasks"])

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to TaskFlow Project Management API. Visit /docs for Swagger documentation."
    }
