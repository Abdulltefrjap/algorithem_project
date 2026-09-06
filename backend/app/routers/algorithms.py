import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.algorithms.divide_conquer import calculate_project_duration
from app.algorithms.sorting import ALGORITHM_INFO, merge_sort, quick_sort
from app.auth import get_current_user
from app.database import get_db
from app.models import Project, Task, User
from app.schemas import DurationResponse, SortComparisonResponse, SortRequest, SortResult, TaskResponse

router = APIRouter(prefix="/api/algorithms", tags=["الخوارزميات - المهندس 4 و 5"])


def _task_to_dict(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "status": task.status.value,
        "task_type": task.task_type.value,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "expected_hours": task.expected_hours,
        "project_id": task.project_id,
        "parent_id": task.parent_id,
        "assignee_id": task.assignee_id,
    }


def _dict_to_response(d: dict, task: Task) -> TaskResponse:
    return TaskResponse(
        id=d["id"],
        title=d["title"],
        description=d.get("description"),
        priority=task.priority,
        status=task.status,
        task_type=task.task_type,
        due_date=task.due_date,
        expected_hours=d["expected_hours"],
        project_id=d["project_id"],
        parent_id=d.get("parent_id"),
        assignee_id=d.get("assignee_id"),
        assignee_name=task.assignee.full_name if task.assignee else None,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.post("/sort", response_model=SortComparisonResponse)
def compare_sorting(
    request: SortRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    مقارنة Merge Sort و Quick Sort على مهام المشروع.
    يعرض النتائج جنباً إلى جنب مع التعقيد الزمني.
    """
    project = db.query(Project).filter(Project.id == request.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")

    tasks = db.query(Task).filter(Task.project_id == request.project_id).all()
    if not tasks:
        raise HTTPException(status_code=400, detail="لا توجد مهام للترتيب")

    task_dicts = [_task_to_dict(t) for t in tasks]
    task_map = {t.id: t for t in tasks}

    start = time.perf_counter()
    merge_result = merge_sort(task_dicts, request.sort_by)
    merge_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    quick_result = quick_sort(task_dicts, request.sort_by)
    quick_time = (time.perf_counter() - start) * 1000

    merge_info = ALGORITHM_INFO["merge_sort"]
    quick_info = ALGORITHM_INFO["quick_sort"]

    return SortComparisonResponse(
        sort_by=request.sort_by,
        merge_sort=SortResult(
            algorithm="Merge Sort",
            sorted_tasks=[_dict_to_response(d, task_map[d["id"]]) for d in merge_result],
            time_ms=round(merge_time, 4),
            complexity_best=merge_info["complexity_best"],
            complexity_worst=merge_info["complexity_worst"],
            complexity_average=merge_info["complexity_average"],
        ),
        quick_sort=SortResult(
            algorithm="Quick Sort",
            sorted_tasks=[_dict_to_response(d, task_map[d["id"]]) for d in quick_result],
            time_ms=round(quick_time, 4),
            complexity_best=quick_info["complexity_best"],
            complexity_worst=quick_info["complexity_worst"],
            complexity_average=quick_info["complexity_average"],
        ),
        note=(
            "كلا الخوارزميتين تعطيان نفس الترتيب المنطقي. "
            "Merge Sort: O(n log n) دائماً ومستقر. "
            "Quick Sort: O(n log n) متوسط و O(n²) أسوأ حالة إذا كانت القائمة مرتبة مسبقاً. "
            "الفرق يظهر في زمن التنفيذ والذاكرة والاستقرار."
        ),
    )


@router.get("/duration/{project_id}", response_model=DurationResponse)
def calculate_duration(
    project_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """حساب المدة الإجمالية باستخدام Divide & Conquer (المهندس 5)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")

    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    task_dicts = [_task_to_dict(t) for t in tasks]
    result = calculate_project_duration(task_dicts)

    return DurationResponse(
        project_id=project_id,
        total_tasks=result["total_tasks"],
        total_hours=result["total_hours"],
        tree=result["tree"],
        complexity=result["complexity"],
        explanation=result["explanation"],
    )
