"""
خوارزميات الترتيب المقارن (Comparison Sorting)
المهندس 4 — ممنوع استخدام list.sort() أو sorted() أو أي مكتبة ترتيب جاهزة.

المشكلة التي يحلها النظام (حسب الدكتور):
  مدير المشروع يحتاج رؤية المهام مرتبة حسب الأولوية (الأعلى أولاً)
  أو حسب التاريخ المتبقي (الأقرب أولاً).

المطلوب:
  تنفيذ خوارزميتين مختلفتين يدوياً (Merge Sort و Quick Sort مفضّلتان)
  عند الضغط على زر «ترتيب»: عرض القائمة مرتبة + زمن التنفيذ بالميلي ثانية
  جنبًا إلى جنب لمقارنة الأداء.

التحليل المطلوب في التقرير:
  شرح تعقيد كل خوارزمية في أفضل وأسوأ حالة
  O(n log n) vs O(n²) ولماذا تتفوق إحداهما في هذه الحالة.
"""

from datetime import datetime
from typing import Any, Callable


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _normalize_due(due: Any):
    """توحيد تاريخ الاستحقاق للمقارنة (naive UTC)."""
    if due is None:
        return datetime.max
    if isinstance(due, str):
        due = datetime.fromisoformat(due.replace("Z", "+00:00"))
    if getattr(due, "tzinfo", None) is not None:
        due = due.replace(tzinfo=None)
    return due


def _get_sort_key(task: dict, sort_by: str):
    """مفتاح المقارنة حسب نوع الترتيب المطلوب من الدكتور."""
    if sort_by == "priority":
        return PRIORITY_ORDER.get(task.get("priority", "medium"), 1)
    if sort_by == "due_date":
        return _normalize_due(task.get("due_date"))
    return 0


def _merge(left: list, right: list, key_fn: Callable) -> list:
    """
    دمج قائمتين مرتبتين — مرحلة Combine في Merge Sort.
    التعقيد: O(n) حيث n = len(left) + len(right)
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_fn(left[i]) <= key_fn(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(tasks: list[dict], sort_by: str = "priority") -> list[dict]:
    """
    Merge Sort — خوارزمية فرق تسد مستقرة.

    الخطوات:
      1) Divide: قسّم القائمة إلى نصفين
      2) Conquer: رتّب كل نصف عودياً
      3) Combine: ادمج النصفين المرتبة

    التعقيد الزمني:
      أفضل: O(n log n) | متوسط: O(n log n) | أسوأ: O(n log n)
    التعقيد المكاني: O(n)
    """
    if len(tasks) <= 1:
        return list(tasks)

    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], sort_by)
    right = merge_sort(tasks[mid:], sort_by)
    key_fn = lambda t: _get_sort_key(t, sort_by)
    return _merge(left, right, key_fn)


def _partition(tasks: list[dict], low: int, high: int, sort_by: str) -> int:
    """
    تقسيم المصفوفة حول المحور (آخر عنصر).
    العناصر الأصغر أو المساوية للمحور على اليسار، والأكبر على اليمين.
    """
    key_fn = lambda t: _get_sort_key(t, sort_by)
    pivot = key_fn(tasks[high])
    i = low - 1
    for j in range(low, high):
        if key_fn(tasks[j]) <= pivot:
            i += 1
            tasks[i], tasks[j] = tasks[j], tasks[i]
    tasks[i + 1], tasks[high] = tasks[high], tasks[i + 1]
    return i + 1


def _quick_sort_recursive(tasks: list[dict], low: int, high: int, sort_by: str):
    """التنفيذ العودي لـ Quick Sort."""
    if low < high:
        pi = _partition(tasks, low, high, sort_by)
        _quick_sort_recursive(tasks, low, pi - 1, sort_by)
        _quick_sort_recursive(tasks, pi + 1, high, sort_by)


def quick_sort(tasks: list[dict], sort_by: str = "priority") -> list[dict]:
    """
    Quick Sort — خوارزمية فرق تسد في المكان (in-place تقريباً).

    الخطوات:
      1) اختر محوراً (Pivot)
      2) قسّم القائمة: أصغر من المحور | المحور | أكبر من المحور
      3) رتّب الجزأين عودياً

    التعقيد الزمني:
      أفضل: O(n log n) | متوسط: O(n log n) | أسوأ: O(n²)
      أسوأ حالة تحدث عندما تكون المصفوفة مرتبة مسبقاً
      (المحور دائماً أصغر/أكبر عنصر → قسمة غير متوازنة).
    التعقيد المكاني: O(log n) لعمق الاستدعاء في الحالة المتوسطة.
    """
    arr = list(tasks)
    if len(arr) > 1:
        _quick_sort_recursive(arr, 0, len(arr) - 1, sort_by)
    return arr


ALGORITHM_INFO = {
    "merge_sort": {
        "name": "Merge Sort",
        "complexity_best": "O(n log n)",
        "complexity_worst": "O(n log n)",
        "complexity_average": "O(n log n)",
        "space": "O(n)",
        "stable": True,
        "description": (
            "تقسيم القائمة إلى نصفين، ترتيب كل نصف عودياً، ثم دمج النتائج. "
            "مستقرة ومتوقعة الأداء دائماً."
        ),
        "why_here": (
            "مناسبة عندما نحتاج ترتيباً مستقراً وموثوقاً "
            "(مثلاً المهام بنفس الأولوية تحافظ على ترتيبها النسبي)."
        ),
    },
    "quick_sort": {
        "name": "Quick Sort",
        "complexity_best": "O(n log n)",
        "complexity_worst": "O(n²)",
        "complexity_average": "O(n log n)",
        "space": "O(log n)",
        "stable": False,
        "description": (
            "اختيار عنصر محوري وتقسيم القائمة حوله ثم ترتيب الجزأين عودياً. "
            "سريعة عملياً لكنها غير مستقرة وقد تصل لـ O(n²)."
        ),
        "why_here": (
            "غالباً أسرع من Merge Sort في الممارسة بسبب Cache Locality، "
            "لكن يجب الحذر من أسوأ حالة."
        ),
    },
}
