from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import get_current_user
from app.database import get_db
from app.models import Project, Task, User
from app.schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/projects", tags=["المشاريع - المهندس 1"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """إنشاء مشروع جديد (اسم، وصف، تاريخ بداية ونهاية)."""
    if project_data.end_date <= project_data.start_date:
        raise HTTPException(status_code=400, detail="تاريخ النهاية يجب أن يكون بعد تاريخ البداية")

    project = Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        created_at=project.created_at,
        task_count=0,
    )


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """قائمة جميع المشاريع."""
    projects = db.query(Project).all()
    result = []
    for p in projects:
        count = db.query(func.count(Task.id)).filter(Task.project_id == p.id).scalar()
        result.append(
            ProjectResponse(
                id=p.id,
                name=p.name,
                description=p.description,
                start_date=p.start_date,
                end_date=p.end_date,
                created_at=p.created_at,
                task_count=count or 0,
            )
        )
    return result


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """الحصول على مشروع محدد."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    count = db.query(func.count(Task.id)).filter(Task.project_id == project_id).scalar()
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        created_at=project.created_at,
        task_count=count or 0,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """حذف مشروع."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    db.delete(project)
    db.commit()
