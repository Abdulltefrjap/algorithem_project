"""
اختبارات وحدة للخوارزميات — تثبت أن التنفيذ يدوي وصحيح.
تشغيل: python -m pytest tests/ -v
أو من مجلد backend: python tests/test_algorithms.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.algorithms.sorting import merge_sort, quick_sort
from app.algorithms.divide_conquer import calculate_project_duration


SAMPLE = [
    {"id": 1, "title": "A", "priority": "low", "due_date": "2026-09-20T00:00:00"},
    {"id": 2, "title": "B", "priority": "high", "due_date": "2026-09-10T00:00:00"},
    {"id": 3, "title": "C", "priority": "medium", "due_date": "2026-09-15T00:00:00"},
    {"id": 4, "title": "D", "priority": "high", "due_date": "2026-09-05T00:00:00"},
]


def test_merge_sort_by_priority():
    result = merge_sort(SAMPLE, "priority")
    priorities = [t["priority"] for t in result]
    assert priorities == ["high", "high", "medium", "low"]


def test_quick_sort_by_priority():
    result = quick_sort(SAMPLE, "priority")
    priorities = [t["priority"] for t in result]
    assert priorities == ["high", "high", "medium", "low"]


def test_sort_by_due_date():
    merge_r = merge_sort(SAMPLE, "due_date")
    quick_r = quick_sort(SAMPLE, "due_date")
    assert [t["id"] for t in merge_r] == [4, 2, 3, 1]
    assert [t["id"] for t in quick_r] == [4, 2, 3, 1]


def test_does_not_mutate_original():
    original_ids = [t["id"] for t in SAMPLE]
    merge_sort(SAMPLE, "priority")
    quick_sort(SAMPLE, "priority")
    assert [t["id"] for t in SAMPLE] == original_ids


def test_divide_conquer_tree():
    tasks = [
        {"id": 1, "title": "Root", "parent_id": None, "expected_hours": 2, "task_type": "milestone"},
        {"id": 2, "title": "Child A", "parent_id": 1, "expected_hours": 3, "task_type": "task"},
        {"id": 3, "title": "Child B", "parent_id": 1, "expected_hours": 4, "task_type": "subtask"},
        {"id": 4, "title": "Grand", "parent_id": 2, "expected_hours": 1, "task_type": "subtask"},
    ]
    result = calculate_project_duration(tasks)
    # Root = 2 + ChildA(3+1) + ChildB(4) = 2+4+4 = 10
    assert result["total_hours"] == 10
    assert result["total_tasks"] == 4
    assert result["complexity"] == "O(n)"
    assert result["tree"][0]["total_hours"] == 10


def test_empty_project():
    result = calculate_project_duration([])
    assert result["total_hours"] == 0
    assert result["total_tasks"] == 0


if __name__ == "__main__":
    test_merge_sort_by_priority()
    test_quick_sort_by_priority()
    test_sort_by_due_date()
    test_does_not_mutate_original()
    test_divide_conquer_tree()
    test_empty_project()
    print("All algorithm tests PASSED")
