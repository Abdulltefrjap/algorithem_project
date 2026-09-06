"""
اختبار شامل لجميع API endpoints.
الاستخدام: python test_api.py
"""
import sys
import requests

BASE = "http://localhost:8000"
passed = 0
failed = 0
token = None


def test(name, method, url, expected_status=200, json=None, data=None, auth=True):
    global passed, failed
    headers = {}
    if auth and token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        if method == "GET":
            r = requests.get(f"{BASE}{url}", headers=headers)
        elif method == "POST":
            r = requests.post(f"{BASE}{url}", headers=headers, json=json, data=data)
        elif method == "PUT":
            r = requests.put(f"{BASE}{url}", headers=headers, json=json)
        elif method == "PATCH":
            r = requests.patch(f"{BASE}{url}", headers=headers)
        elif method == "DELETE":
            r = requests.delete(f"{BASE}{url}", headers=headers)
        else:
            raise ValueError(f"Unknown method: {method}")

        ok = r.status_code == expected_status
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {name} -> {r.status_code}")
        if not ok:
            print(f"         Expected {expected_status}, got {r.status_code}: {r.text[:200]}")
        return r
    except Exception as e:
        failed += 1
        print(f"  [FAIL] {name} -> ERROR: {e}")
        return None


print("=" * 55)
print("  KANBAN ALGORITHMS - API TEST SUITE")
print("=" * 55)

# 1. Health
print("\n[1] Health Check")
test("Root endpoint", "GET", "/", auth=False)

# 2. Auth
print("\n[2] Authentication")
r = test("Register new user", "POST", "/api/auth/register", 201, auth=False, json={
    "username": "testuser", "email": "test@test.com",
    "password": "123456", "full_name": "Test User"
})
r = test("Login ahmed", "POST", "/api/auth/login", 200, auth=False,
         data={"username": "ahmed", "password": "123456"})
if r and r.status_code == 200:
    token = r.json()["access_token"]
    print(f"         Token obtained: {token[:20]}...")
else:
    print("  FATAL: Cannot login. Is the server running?")
    sys.exit(1)

test("Get current user", "GET", "/api/auth/me")
test("List users", "GET", "/api/auth/users")

# 3. Projects
print("\n[3] Projects")
r = test("List projects", "GET", "/api/projects/")
projects = r.json() if r else []
test("Get project 1", "GET", "/api/projects/1")

# 4. Tasks
print("\n[4] Tasks")
r = test("List project 1 tasks", "GET", "/api/tasks/project/1")
tasks = r.json() if r else []
print(f"         Found {len(tasks)} tasks")

test("Create new task", "POST", "/api/tasks/", 201, json={
    "title": "مهمة اختبار", "description": "تم إنشاؤها أثناء الاختبار",
    "priority": "high", "task_type": "task", "expected_hours": 2,
    "project_id": 1, "assignee_id": 1,
})
r = test("Update task status", "PATCH", "/api/tasks/1/status?new_status=in_progress")

# 5. Kanban
print("\n[5] Kanban Board")
r = test("Get kanban board", "GET", "/api/kanban/1")
if r:
    board = r.json()
    cols = board.get("columns", {})
    print(f"         new={len(cols.get('new',{}).get('tasks',[]))}  "
          f"in_progress={len(cols.get('in_progress',{}).get('tasks',[]))}  "
          f"done={len(cols.get('done',{}).get('tasks',[]))}")

r = test("Get activity log", "GET", "/api/kanban/1/activity")
if r:
    print(f"         {len(r.json())} activity entries")

# 6. Algorithms - Sorting
print("\n[6] Sorting Algorithms")
r = test("Sort by priority", "POST", "/api/algorithms/sort", json={
    "project_id": 1, "sort_by": "priority"
})
if r:
    data = r.json()
    ms = data["merge_sort"]
    qs = data["quick_sort"]
    print(f"         Merge Sort: {ms['time_ms']}ms | Quick Sort: {qs['time_ms']}ms")
    print(f"         Merge tasks: {len(ms['sorted_tasks'])} | Quick tasks: {len(qs['sorted_tasks'])}")
    merge_ids = [t["id"] for t in ms["sorted_tasks"]]
    quick_ids = [t["id"] for t in qs["sorted_tasks"]]
    match = merge_ids == quick_ids
    print(f"         Results match: {match}")

r = test("Sort by due_date", "POST", "/api/algorithms/sort", json={
    "project_id": 1, "sort_by": "due_date"
})

# 7. Divide & Conquer
print("\n[7] Divide & Conquer")
r = test("Calculate duration", "GET", "/api/algorithms/duration/1")
if r:
    data = r.json()
    print(f"         Total tasks: {data['total_tasks']}")
    print(f"         Total hours: {data['total_hours']}")
    print(f"         Complexity:  {data['complexity']}")
    print(f"         Tree nodes:  {len(data['tree'])}")

# 8. Reports
print("\n[8] Reports")
r = test("Sprint report", "GET", "/api/reports/sprint/1")
if r:
    data = r.json()
    print(f"         Completion: {data['completion_percentage']}%")
    print(f"         Done: {data['done_tasks']}/{data['total_tasks']}")

r = test("Sprint report project 2", "GET", "/api/reports/sprint/2")

# Summary
print("\n" + "=" * 55)
print(f"  RESULTS: {passed} passed, {failed} failed")
print("=" * 55)
sys.exit(0 if failed == 0 else 1)
