import { useState } from 'react';
import { algorithmsAPI } from '../api';

const PRIORITY_LABELS = { high: 'عالية', medium: 'متوسطة', low: 'منخفضة' };

export default function SortingPage({ projectId }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sortBy, setSortBy] = useState('priority');

  const handleSort = async () => {
    setLoading(true);
    try {
      const res = await algorithmsAPI.sort(projectId, sortBy);
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'خطأ في الترتيب');
    }
    setLoading(false);
  };

  const renderAlgoPanel = (data) => (
    <div className="algo-panel">
      <h3>{data.algorithm}</h3>
      <p>⏱ زمن التنفيذ: <strong>{data.time_ms} ms</strong></p>
      <div>
        <span className="complexity-badge">أفضل: {data.complexity_best}</span>
        <span className="complexity-badge">متوسط: {data.complexity_average}</span>
        <span className="complexity-badge">أسوأ: {data.complexity_worst}</span>
      </div>
      <div className="sorted-list">
        {data.sorted_tasks.map((task, i) => (
          <div key={`${data.algorithm}-${task.id}`} className="sorted-item">
            <strong>#{i + 1}</strong> {task.title}
            <span className={`priority priority-${task.priority}`} style={{ marginRight: '0.5rem' }}>
              {PRIORITY_LABELS[task.priority]}
            </span>
            {task.due_date && (
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                📅 {new Date(task.due_date).toLocaleDateString('ar')}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div>
      <h3 style={{ marginBottom: '1rem' }}>خوارزميات الترتيب (Comparison Sorting)</h3>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
        تنفيذ يدوي لـ Merge Sort و Quick Sort — <strong>بدون</strong> استخدام sort() المدمجة.
        المشكلة: ترتيب المهام حسب الأولوية أو أقرب تاريخ استحقاق لمدير المشروع.
      </p>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} style={{ padding: '0.5rem' }}>
          <option value="priority">ترتيب حسب الأولوية (الأعلى أولاً)</option>
          <option value="due_date">ترتيب حسب تاريخ الاستحقاق (الأقرب أولاً)</option>
        </select>
        <button className="btn btn-primary" onClick={handleSort} disabled={loading}>
          {loading ? 'جاري الترتيب...' : '🔄 ترتيب ومقارنة'}
        </button>
      </div>

      {result && (
        <>
          <div className="success-msg">{result.note}</div>
          <div className="analysis-box">
            <h4>تحليل مختصر للمناقشة</h4>
            <ul>
              <li><strong>Merge Sort:</strong> O(n log n) دائماً — مستقر ومتوقع، يستهلك ذاكرة إضافية O(n).</li>
              <li><strong>Quick Sort:</strong> O(n log n) متوسط، O(n²) أسوأ (مصفوفة مرتبة مسبقاً) — أسرع عملياً غالباً.</li>
              <li>كلاهما يعطيان نفس الترتيب المنطقي؛ الفرق في الزمن والاستقرار والذاكرة.</li>
            </ul>
          </div>
          <div className="sort-comparison">
            {renderAlgoPanel(result.merge_sort)}
            {renderAlgoPanel(result.quick_sort)}
          </div>
        </>
      )}
    </div>
  );
}
