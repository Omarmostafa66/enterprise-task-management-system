import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import users, tasks, projects
from app.db.database import engine, Base
from app.utils.logger import logger

# 1. إنشاء الجداول في قاعدة البيانات تلقائياً عند بدء التشغيل
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    description="Backend API with JWT, RBAC, Redis Caching, and Monitoring",
    version="1.0.0"
)

# 2. إعداد الـ CORS (ضروري جداً لعمل الـ Frontend المعتمد على JavaScript)
# يسمح لملف index.html بالتواصل مع الـ API دون مشاكل أمنية من المتصفح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج يفضل تحديد رابط الـ Frontend فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. إعداد الـ Monitoring Dashboard (المتطلب رقم 8)
# يقوم بإنشاء endpoint باسم /metrics لجمع بيانات الأداء
Instrumentator().instrument(app).expose(app)


# 4. Middleware للـ Logging المتقدم (المتطلب رقم 8)
# يسجل تفاصيل كل طلب: Method, Path, Status Code, Execution Time
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # معالجة الطلب وتلقي الرد
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)

    # تسجيل اللوج بشكل منظم باستخدام Loguru
    logger.info(
        f"Method: {request.method} | Path: {request.url.path} | "
        f"Status: {response.status_code} | Duration: {formatted_process_time}ms"
    )

    return response


# 5. تسجيل الـ Routers (المتطلب رقم 1)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(projects.router)


# 6. أحداث بدء وإيقاف التطبيق (Startup & Shutdown)
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


# 7. الـ Root Endpoint (واجهة ترحيبية)
@app.get("/", tags=["Root"])
def root():
    return {
        "project": "DSC 306 - Task Management System",
        "semester": "Winter 2026",
        "status": "Running",
        "docs": "/docs",
        "metrics": "/metrics"
    }