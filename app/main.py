import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from jose import jwt, JWTError

from app.routers import users, tasks, projects
from app.db.database import engine, Base
from app.utils.logger import logger
from app.core.security import SECRET_KEY, ALGORITHM

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Monitoring Dashboard Setup
Instrumentator().instrument(app).expose(app)


# 4. Advanced Logging Middleware (Audit Logs Integration)
# Records details for every request: User Identity, Method, Path, Status Code, and Execution Time
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Attempt to extract user identity from the JWT Token for Audit Logs
    user_identity = "Anonymous"
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_identity = payload.get("sub", "Anonymous")
        except JWTError:
            pass  # Invalid token, keep as Anonymous

    # Process the request and receive the response
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)

    # Structured logging for the Audit Dashboard
    logger.info(
        f"User: {user_identity} | Method: {request.method} | Path: {request.url.path} | "
        f"Status: {response.status_code} | Duration: {formatted_process_time}ms"
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
        "metrics": "/metrics"
    }