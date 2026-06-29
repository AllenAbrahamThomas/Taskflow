'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import api from '@/services/api';
import Navbar from '@/components/Navbar';
import TaskModal from '@/components/TaskModal';
import { 
  Plus, 
  Calendar, 
  User, 
  FolderKanban, 
  ChevronLeft, 
  ChevronRight,
  Filter
} from 'lucide-react';

interface Project {
  id: string;
  name: string;
}

interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'review' | 'done';
  project_id: string;
  assigned_to: string | null;
  due_date: string | null;
  created_at: string;
  project: {
    id: string;
    name: string;
  };
  assignee: UserProfile | null;
}

export default function TasksPage() {
  const { user, loading } = useAuth(true);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<UserProfile[]>([]);
  
  // Filters and Pagination
  const [projectId, setProjectId] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [page, setPage] = useState(1);
  const [limit] = useState(6); // 6 tasks per page
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const [fetching, setFetching] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchFilters = async () => {
    try {
      const [projRes, usersRes] = await Promise.all([
        api.get('/projects/'),
        api.get('/users/')
      ]);
      setProjects(projRes.data);
      setUsers(usersRes.data);
    } catch (err) {
      console.error('Failed to fetch filters data', err);
    }
  };

  const fetchTasks = async () => {
    try {
      setFetching(true);
      const queryParams = new URLSearchParams();
      if (projectId) queryParams.append('project_id', projectId);
      if (statusFilter) queryParams.append('status', statusFilter);
      if (assignedTo) queryParams.append('assigned_to', assignedTo);
      queryParams.append('page', page.toString());
      queryParams.append('limit', limit.toString());

      const response = await api.get(`/tasks/?${queryParams.toString()}`);
      setTasks(response.data.items);
      setTotalPages(response.data.pages);
      setTotalItems(response.data.total);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    } finally {
      setFetching(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchFilters();
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, projectId, statusFilter, assignedTo, page]);

  const handleStatusChange = async (taskId: string, newStatus: string) => {
    try {
      await api.put(`/tasks/${taskId}/status`, { status: newStatus });
      fetchTasks();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to update task status');
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'todo':
        return 'bg-slate-100 text-slate-655 text-slate-600 border-slate-200';
      case 'in_progress':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'review':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'done':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      default:
        return 'bg-slate-100 text-slate-600 border-slate-200';
    }
  };

  if (loading || !user) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-slate-50 text-slate-900">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-indigo-600"></div>
      </div>
    );
  }

  const isAdmin = user.role === 'admin';

  return (
    <div className="min-h-screen bg-slate-55 bg-slate-50 text-slate-900">
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold md:text-3xl text-slate-900">Tasks Board</h1>
            <p className="mt-1 text-sm text-slate-500">
              Manage, filter, and update task workflows across projects.
            </p>
          </div>
          {isAdmin && (
            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 transition"
            >
              <Plus className="h-4 w-4" /> Create Task
            </button>
          )}
        </div>

        {/* Filters Panel */}
        <div className="mt-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
            <Filter className="h-4 w-4 text-indigo-600" />
            <span>Filter Tasks</span>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label className="text-xs font-medium text-slate-500">Project</label>
              <select
                value={projectId}
                onChange={(e) => {
                  setProjectId(e.target.value);
                  setPage(1);
                }}
                className="mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs text-slate-800 focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600 focus:outline-none"
              >
                <option value="">All Projects</option>
                {projects.map((proj) => (
                  <option key={proj.id} value={proj.id}>
                    {proj.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-500">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value);
                  setPage(1);
                }}
                className="mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs text-slate-800 focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600 focus:outline-none"
              >
                <option value="">All Statuses</option>
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="review">Review</option>
                <option value="done">Done</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-medium text-slate-500">Assigned User</label>
              <select
                value={assignedTo}
                onChange={(e) => {
                  setAssignedTo(e.target.value);
                  setPage(1);
                }}
                className="mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs text-slate-800 focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600 focus:outline-none"
              >
                <option value="">All Users</option>
                {users.map((usr) => (
                  <option key={usr.id} value={usr.id}>
                    {usr.name} ({usr.role})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Task Cards Grid */}
        {fetching ? (
          <div className="mt-12 flex justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-indigo-600"></div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="mt-8 rounded-xl border border-dashed border-slate-200 bg-white p-12 text-center shadow-sm">
            <h3 className="text-lg font-semibold text-slate-900">No tasks matching criteria</h3>
            <p className="mt-2 text-sm text-slate-505 text-slate-500">Try adjusting your filters or create a new task.</p>
          </div>
        ) : (
          <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {tasks.map((task) => {
              // Enforce RBAC: Can this user edit the status of this task?
              const canEditStatus = isAdmin || (task.assigned_to === user.id);
              
              return (
                <div
                  key={task.id}
                  className="flex flex-col justify-between rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-slate-300 hover:shadow"
                >
                  <div>
                    {/* Project and Title */}
                    <div className="flex items-center gap-1.5 text-xs text-indigo-650 text-indigo-600 font-semibold">
                      <FolderKanban className="h-3.5 w-3.5" />
                      <span>{task.project.name}</span>
                    </div>
                    <h3 className="mt-2 text-base font-bold text-slate-900 leading-tight">
                      {task.title}
                    </h3>
                    <p className="mt-2 text-xs text-slate-600 line-clamp-3">
                      {task.description || 'No description provided.'}
                    </p>
                  </div>

                  {/* Metadata and Status Transitions */}
                  <div className="mt-6 space-y-4 border-t border-slate-100 pt-4">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <div className="flex items-center gap-1.5">
                        <Calendar className="h-3.5 w-3.5" />
                        <span>
                          {task.due_date 
                            ? new Date(task.due_date).toLocaleDateString() 
                            : 'No due date'}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <User className="h-3.5 w-3.5" />
                        <span>{task.assignee ? task.assignee.name : 'Unassigned'}</span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between gap-4">
                      {/* Current Status Badge */}
                      <span className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-semibold uppercase tracking-wide ${getStatusBadgeClass(task.status)}`}>
                        {task.status.replace('_', ' ')}
                      </span>

                      {/* Dropdown status update controller */}
                      <select
                        disabled={!canEditStatus}
                        value={task.status}
                        onChange={(e) => handleStatusChange(task.id, e.target.value)}
                        className={`rounded-lg border border-slate-305 border-slate-300 bg-white px-2.5 py-1 text-xs text-slate-700 focus:border-indigo-600 focus:outline-none focus:ring-1 focus:ring-indigo-600 disabled:cursor-not-allowed disabled:opacity-40`}
                        title={canEditStatus ? "Update status" : "Only the assignee or an Admin can change status"}
                      >
                        <option value="todo">To Do</option>
                        <option value="in_progress">In Progress</option>
                        <option value="review">Review</option>
                        <option value="done">Done</option>
                      </select>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Pagination controls */}
        {totalPages > 1 && (
          <div className="mt-10 flex items-center justify-between border-t border-slate-205 border-slate-200 pt-6">
            <span className="text-xs text-slate-500">
              Showing page {page} of {totalPages} ({totalItems} total tasks)
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => setPage((p) => Math.max(p - 1, 1))}
                disabled={page === 1}
                className="flex items-center justify-center rounded-lg border border-slate-300 bg-white p-2 text-slate-500 hover:text-slate-900 disabled:opacity-30 disabled:hover:text-slate-500"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                disabled={page === totalPages}
                className="flex items-center justify-center rounded-lg border border-slate-300 bg-white p-2 text-slate-500 hover:text-slate-900 disabled:opacity-30 disabled:hover:text-slate-500"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Create Task Modal */}
        {isModalOpen && (
          <TaskModal
            onClose={() => setIsModalOpen(false)}
            onSuccess={() => {
              setIsModalOpen(false);
              fetchTasks();
            }}
          />
        )}
      </main>
    </div>
  );
}
