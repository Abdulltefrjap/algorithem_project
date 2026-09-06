import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectsAPI } from '../api';

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', description: '', start_date: '', end_date: '' });
  const navigate = useNavigate();

  const loadProjects = () => {
    projectsAPI.list().then((res) => setProjects(res.data));
  };

  useEffect(() => { loadProjects(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await projectsAPI.create({
      ...form,
      start_date: new Date(form.start_date).toISOString(),
      end_date: new Date(form.end_date).toISOString(),
    });
    setShowForm(false);
    setForm({ name: '', description: '', start_date: '', end_date: '' });
    loadProjects();
  };

  return (
  <div>
      <div className="page-header">
        <h2>المشاريع</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'إلغاء' : '+ مشروع جديد'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>إنشاء مشروع جديد</h3>
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>اسم المشروع *</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>الوصف</label>
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label>تاريخ البداية *</label>
                <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>تاريخ النهاية *</label>
                <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} required />
              </div>
            </div>
            <button type="submit" className="btn btn-primary">إنشاء</button>
          </form>
        </div>
      )}

      <div className="projects-grid">
        {projects.map((p) => (
          <div key={p.id} className="card project-card" onClick={() => navigate(`/project/${p.id}`)}>
            <h3>{p.name}</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: '0.5rem 0' }}>
              {p.description || 'بدون وصف'}
            </p>
            <div className="meta">
              <span>📋 {p.task_count} مهمة</span>
              <br />
              <span>📅 {new Date(p.start_date).toLocaleDateString('ar')} - {new Date(p.end_date).toLocaleDateString('ar')}</span>
            </div>
          </div>
        ))}
      </div>
      {projects.length === 0 && !showForm && (
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '2rem' }}>
          لا توجد مشاريع بعد. أنشئ مشروعك الأول!
        </p>
      )}
    </div>
  );
}
