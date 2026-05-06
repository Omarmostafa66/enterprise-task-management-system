from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# صيغة الاتصال بـ MySQL:
# mysql+pymysql://[username]:[password]@[host]:[port]/[database_name]
# شيل كلمة password وسيب مكانها فاضي بعد النقطتين
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/task_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()