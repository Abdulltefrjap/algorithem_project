import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => API.post('/api/auth/register', data),
  login: (username, password) => {
    const form = new URLSearchParams();
    form.append('username', username);
    form.append('password', password);
    return API.post('/api/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  me: () => API.get('/api/auth/me'),
  users: () => API.get('/api/auth/users'),
};

export const projectsAPI = {
  list: () => API.get('/api/projects/'),
  get: (id) => API.get(`/api/projects/${id}`),
  create: (data) => API.post('/api/projects/', data),
  delete: (id) => API.delete(`/api/projects/${id}`),
};

export const tasksAPI = {
  list: (projectId) => API.get(`/api/tasks/project/${projectId}`),
  create: (data) => API.post('/api/tasks/', data),
  update: (id, data) => API.put(`/api/tasks/${id}`, data),
  updateStatus: (id, status) => API.patch(`/api/tasks/${id}/status?new_status=${status}`),
  delete: (id) => API.delete(`/api/tasks/${id}`),
};

export const kanbanAPI = {
  board: (projectId) => API.get(`/api/kanban/${projectId}`),
  activity: (projectId) => API.get(`/api/kanban/${projectId}/activity`),
};

export const algorithmsAPI = {
  sort: (projectId, sortBy) => API.post('/api/algorithms/sort', { project_id: projectId, sort_by: sortBy }),
  duration: (projectId) => API.get(`/api/algorithms/duration/${projectId}`),
};

export const reportsAPI = {
  sprint: (projectId) => API.get(`/api/reports/sprint/${projectId}`),
};

export default API;
