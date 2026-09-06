"""
إنشاء بيانات تجريبية شاملة للاختبار — فريق 6 مهندسين.
الاستخدام:
  python seed_data.py
  python seed_data.py --reset
"""
import sys
from datetime import datetime, timedelta

from app.database import SessionLocal, engine, Base
from app.models import User, Project, Task, ActivityLog, TaskPriority, TaskStatus, TaskType
from app.auth import hash_password

Base.metadata.create_all(bind=engine)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("[RESET] Database cleared.")


def seed():
    db = SessionLocal()
    now = datetime.utcnow()

    users_data = [
        {"username": "mohamad_abosaad", "email": "abosaad@algo.com", "full_name": "محمد أبو سعد", "password": "123456"},
        {"username": "mohamad_jaber", "email": "jaber@algo.com", "full_name": "محمد الجابر", "password": "123456"},
        {"username": "mahmoud", "email": "mahmoud@algo.com", "full_name": "محمود هنداوي", "password": "123456"},
        {"username": "yousef", "email": "yousef@algo.com", "full_name": "يوسف حسن", "password": "123456"},
        {"username": "abdullatif", "email": "abdullatif@algo.com", "full_name": "عبد اللطيف حاج رجب", "password": "123456"},
        {"username": "hasan", "email": "hasan@algo.com", "full_name": "حسن سليمان", "password": "123456"},
    ]

    users = []
    for u in users_data:
        user = User(
            username=u["username"],
            email=u["email"],
            full_name=u["full_name"],
            hashed_password=hash_password(u["password"]),
        )
        db.add(user)
        users.append(user)
    db.flush()
    abosaad, jaber, mahmoud, yousef, abdullatif, hasan = users

    project1 = Project(
        name="تطبيق إدارة المهام",
        description="مشروع الخوارزميات - نظام Kanban مع تطبيق خوارزميات الترتيب وفرق تسد",
        start_date=now - timedelta(days=30),
        end_date=now + timedelta(days=60),
    )
    db.add(project1)
    db.flush()

    m1_design = Task(
        title="المرحلة الأولى: التصميم",
        description="تصميم النظام وقاعدة البيانات والواجهات",
        priority=TaskPriority.HIGH,
        task_type=TaskType.MILESTONE,
        status=TaskStatus.DONE,
        expected_hours=10,
        project_id=project1.id,
        assignee_id=abosaad.id,
        due_date=now - timedelta(days=10),
    )
    db.add(m1_design)
    db.flush()

    t_db = Task(
        title="تصميم قاعدة البيانات", description="ERD + Models",
        priority=TaskPriority.HIGH, task_type=TaskType.TASK,
        status=TaskStatus.DONE, expected_hours=4,
        project_id=project1.id, parent_id=m1_design.id,
        assignee_id=abosaad.id, due_date=now - timedelta(days=20),
    )
    t_ui = Task(
        title="تصميم واجهة المستخدم", description="Wireframes + UI Kit",
        priority=TaskPriority.MEDIUM, task_type=TaskType.TASK,
        status=TaskStatus.DONE, expected_hours=6,
        project_id=project1.id, parent_id=m1_design.id,
        assignee_id=jaber.id, due_date=now - timedelta(days=15),
    )
    db.add_all([t_db, t_ui])
    db.flush()

    m1_dev = Task(
        title="المرحلة الثانية: التطوير",
        description="بناء Backend و Frontend والخوارزميات",
        priority=TaskPriority.HIGH,
        task_type=TaskType.MILESTONE,
        status=TaskStatus.IN_PROGRESS,
        expected_hours=20,
        project_id=project1.id,
        assignee_id=mahmoud.id,
        due_date=now + timedelta(days=30),
    )
    db.add(m1_dev)
    db.flush()

    t_backend = Task(
        title="Backend API (FastAPI)", priority=TaskPriority.HIGH,
        task_type=TaskType.SUBTASK, status=TaskStatus.DONE,
        expected_hours=8, project_id=project1.id,
        parent_id=m1_dev.id, assignee_id=mahmoud.id,
        due_date=now + timedelta(days=5),
    )
    t_frontend = Task(
        title="Frontend React", priority=TaskPriority.HIGH,
        task_type=TaskType.SUBTASK, status=TaskStatus.IN_PROGRESS,
        expected_hours=8, project_id=project1.id,
        parent_id=m1_dev.id, assignee_id=yousef.id,
        due_date=now + timedelta(days=15),
    )
    t_sorting = Task(
        title="خوارزميات الترتيب", description="Merge Sort + Quick Sort",
        priority=TaskPriority.MEDIUM, task_type=TaskType.SUBTASK,
        status=TaskStatus.IN_PROGRESS, expected_hours=4,
        project_id=project1.id, parent_id=m1_dev.id,
        assignee_id=abdullatif.id, due_date=now + timedelta(days=20),
    )
    t_dnc = Task(
        title="Divide & Conquer", description="حساب مدة المشروع عودياً",
        priority=TaskPriority.MEDIUM, task_type=TaskType.SUBTASK,
        status=TaskStatus.NEW, expected_hours=3,
        project_id=project1.id, parent_id=m1_dev.id,
        assignee_id=hasan.id, due_date=now + timedelta(days=25),
    )
    db.add_all([t_backend, t_frontend, t_sorting, t_dnc])
    db.flush()

    m1_test = Task(
        title="المرحلة الثالثة: الاختبار والتسليم",
        priority=TaskPriority.HIGH,
        task_type=TaskType.MILESTONE,
        status=TaskStatus.NEW,
        expected_hours=8,
        project_id=project1.id,
        assignee_id=hasan.id,
        due_date=now + timedelta(days=55),
    )
    db.add(m1_test)
    db.flush()

    t_unit = Task(
        title="اختبار الوحدات", priority=TaskPriority.MEDIUM,
        task_type=TaskType.TASK, status=TaskStatus.NEW,
        expected_hours=3, project_id=project1.id,
        parent_id=m1_test.id, assignee_id=yousef.id,
    )
    t_report = Task(
        title="كتابة التقرير النهائي", priority=TaskPriority.HIGH,
        task_type=TaskType.TASK, status=TaskStatus.NEW,
        expected_hours=5, project_id=project1.id,
        parent_id=m1_test.id, assignee_id=hasan.id,
        due_date=now + timedelta(days=50),
    )
    db.add_all([t_unit, t_report])

    project2 = Project(
        name="موقع الجامعة الإلكتروني",
        description="مشروع ثانوي - بوابة إلكترونية لكلية الهندسة",
        start_date=now - timedelta(days=10),
        end_date=now + timedelta(days=80),
    )
    db.add(project2)
    db.flush()

    p2_tasks = [
        Task(title="تحليل المتطلبات", priority=TaskPriority.HIGH,
             task_type=TaskType.TASK, status=TaskStatus.DONE,
             expected_hours=6, project_id=project2.id,
             assignee_id=abosaad.id, due_date=now - timedelta(days=5)),
        Task(title="بناء الصفحة الرئيسية", priority=TaskPriority.MEDIUM,
             task_type=TaskType.TASK, status=TaskStatus.IN_PROGRESS,
             expected_hours=10, project_id=project2.id,
             assignee_id=jaber.id, due_date=now + timedelta(days=20)),
        Task(title="نظام التسجيل", priority=TaskPriority.HIGH,
             task_type=TaskType.TASK, status=TaskStatus.NEW,
             expected_hours=12, project_id=project2.id,
             assignee_id=mahmoud.id, due_date=now + timedelta(days=40)),
        Task(title="لوحة تحكم الإدارة", priority=TaskPriority.LOW,
             task_type=TaskType.TASK, status=TaskStatus.NEW,
             expected_hours=8, project_id=project2.id,
             assignee_id=yousef.id, due_date=now + timedelta(days=60)),
    ]
    db.add_all(p2_tasks)
    db.flush()

    activity_data = [
        (t_db, abosaad, "إنشاء مهمة", None, "تصميم قاعدة البيانات", now - timedelta(days=28)),
        (t_db, abosaad, "تغيير الحالة", "new", "in_progress", now - timedelta(days=27)),
        (t_db, abosaad, "تغيير الحالة", "in_progress", "done", now - timedelta(days=22)),
        (t_ui, jaber, "إنشاء مهمة", None, "تصميم واجهة المستخدم", now - timedelta(days=25)),
        (t_ui, jaber, "تغيير الحالة", "new", "in_progress", now - timedelta(days=24)),
        (t_ui, jaber, "تغيير الحالة", "in_progress", "done", now - timedelta(days=16)),
        (m1_design, abosaad, "تغيير الحالة", "in_progress", "done", now - timedelta(days=15)),
        (t_backend, mahmoud, "إنشاء مهمة", None, "Backend API", now - timedelta(days=14)),
        (t_backend, mahmoud, "تغيير الحالة", "new", "in_progress", now - timedelta(days=13)),
        (t_backend, mahmoud, "تغيير الحالة", "in_progress", "done", now - timedelta(days=7)),
        (t_frontend, yousef, "إنشاء مهمة", None, "Frontend React", now - timedelta(days=10)),
        (t_frontend, yousef, "تغيير الحالة", "new", "in_progress", now - timedelta(days=8)),
        (t_sorting, abdullatif, "إنشاء مهمة", None, "خوارزميات الترتيب", now - timedelta(days=5)),
        (t_sorting, abdullatif, "تغيير الحالة", "new", "in_progress", now - timedelta(days=3)),
        (t_dnc, hasan, "إنشاء مهمة", None, "Divide & Conquer", now - timedelta(days=2)),
        (p2_tasks[0], abosaad, "إنشاء مهمة", None, "تحليل المتطلبات", now - timedelta(days=9)),
        (p2_tasks[0], abosaad, "تغيير الحالة", "new", "done", now - timedelta(days=6)),
        (p2_tasks[1], jaber, "تغيير الحالة", "new", "in_progress", now - timedelta(days=2)),
    ]

    for task, user, action, old_val, new_val, ts in activity_data:
        db.add(ActivityLog(
            task_id=task.id,
            user_id=user.id,
            action=action,
            old_value=old_val,
            new_value=new_val,
            timestamp=ts,
        ))

    db.commit()

    print("=" * 50)
    print("SEED DATA CREATED SUCCESSFULLY (6 engineers)")
    print("=" * 50)
    print(f"Users:    {db.query(User).count()}")
    print(f"Projects: {db.query(Project).count()}")
    print(f"Tasks:    {db.query(Task).count()}")
    print(f"Logs:     {db.query(ActivityLog).count()}")
    print("-" * 50)
    print("LOGIN (password: 123456):")
    for u in users_data:
        print(f"  - {u['username']:18} | {u['email']}")
    print("=" * 50)
    db.close()


if __name__ == "__main__":
    if "--reset" in sys.argv:
        reset_db()
        seed()
    else:
        db = SessionLocal()
        if db.query(Project).first():
            print("Data already exists. Use --reset to recreate.")
            db.close()
            sys.exit(0)
        db.close()
        seed()
