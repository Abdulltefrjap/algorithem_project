from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, projects, tasks, kanban, algorithms, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="نظام إدارة المهام - مشروع الخوارزميات",
    description="نظام Kanban مع تطبيق خوارزميات الترتيب وفرق تسد",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(kanban.router)
app.include_router(algorithms.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "نظام إدارة المهام - مشروع الخوارزميات",
        "docs": "/docs",
        "team": 5,
        "deadline": "2026-09-14",
    }
