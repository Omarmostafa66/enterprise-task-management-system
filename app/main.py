import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.routers import users, tasks, projects
from app.db.database import engine, Base, SessionLocal
from app.utils.logger import logger
from app.core.security import (
    SECRET_KEY,
    ALGORITHM,
    get_password_hash
)
from app.utils.cache import redis_client
from app.models.user import User, UserRole


# 1. Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    description="Backend API with JWT, RBAC, Redis Caching, and Monitoring",
    version="1.0.0"
)


# 2. CORS Configuration for Frontend Integration
app.add_middleware(
    CORSMiddleware,

    # Allow frontend applications during development
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Monitoring Dashboard Setup
Instrumentator().instrument(app).expose(app)


# 4. Advanced Logging Middleware (Audit Logs Integration)
# Records details for every request:
# User Identity, Method, Path, Status Code, and Execution Time
@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    # Attempt to extract user identity from the JWT Token for Audit Logs
    user_identity = "Anonymous"

    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            user_identity = payload.get("sub", "Anonymous")

        except JWTError:

            logger.warning(
                f"Invalid JWT token received | path={request.url.path}"
            )

    # Process the request and receive the response
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    formatted_process_time = "{0:.2f}".format(process_time)

    # Structured logging for the Audit Dashboard
    logger.info(
        f"User: {user_identity} | "
        f"Method: {request.method} | "
        f"Path: {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {formatted_process_time}ms"
    )

    return response


# 5. Router Registration
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(projects.router)


# 6. Lifecycle Events
@app.on_event("startup")
async def startup_event():

    logger.info("**************************************************")
    logger.info("The Task Management System is starting up...")
    logger.info("Monitoring metrics available at: http://localhost:8000/metrics")
    logger.info("Swagger documentation at: http://localhost:8000/docs")

    # Verify Redis connection during startup
    try:
        redis_client.ping()

        logger.info("Redis connection established successfully.")

    except Exception as e:

        logger.warning(
            f"Redis connection failed during startup: {str(e)}"
        )

    # Create default admin account if no admin exists
    db: Session = SessionLocal()

    try:

        existing_admin = db.query(User).filter(
            User.role == UserRole.ADMIN
        ).first()

        if not existing_admin:

            default_admin = User(
                email="admin@system.com",
                full_name="Default System Admin",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            )

            db.add(default_admin)
            db.commit()

            logger.info(
                "Default admin account created successfully."
            )

            logger.info(
                "Default Admin Credentials | "
                "Email: admin@system.com | "
                "Password: admin123"
            )

        else:

            logger.info(
                "Admin account already exists. "
                "Skipping default admin creation."
            )

    except Exception as e:

        logger.error(
            f"Failed to create default admin account: {str(e)}"
        )

    finally:

        db.close()

    logger.info("**************************************************")


@app.on_event("shutdown")
async def shutdown_event():

    logger.warning("The Task Management System is shutting down...")


# 7. Root Endpoint
@app.get("/", tags=["Root"])
def root():

    return {
        "project": "DSC 306 - Task Management System",
        "semester": "Winter 2026",
        "status": "Running",
        "docs": "/docs",
        "metrics": "/metrics",
        "cache": "Redis Enabled"
    }