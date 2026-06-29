'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import api from '@/services/api';
import Navbar from '@/components/Navbar';
import { 
  FolderKanban, 
  CheckSquare, 
  Clock, 
  CheckCircle2, 
  ArrowRight,
  TrendingUp
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, loading } = useAuth(true);
  const [stats, setStats] = useState({
    projectsCount: 0,
    todoCount: 0,
    inProgressCount: 0,
    doneCount: 0,
    totalTasks: 0,
  });
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchDashboardData = async () => {
      try {
        setFetching(true);
        // Fetch projects
        const projRes = await api.get('/projects/');
        const projects = projRes.data;

        // Fetch tasks
        const tasksRes = await api.get('/tasks/?limit=100');
        const tasks = tasksRes.data.items;

        const todo = tasks.filter((t: any) => t.status === 'todo').length;
        const progress = tasks.filter((t: any) => t.status === 'in_progress').length;
        const review = tasks.filter((t: any) => t.status === 'review').length;
        const done = tasks.filter((t: any) => t.status === 'done').length;

        setStats({
          projectsCount: projects.length,
          todoCount: todo + review,
          inProgressCount: progress,
          doneCount: done,
          totalTasks: tasksRes.data.total,
        });
      } catch (err) {
        console.error('Failed to load dashboard statistics', err);
      } finally {
        setFetching(false);
      }
    };

    fetchDashboardData();
  }, [user]);

  if (loading || !user) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-slate-50 text-slate-900">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-indigo-650 border-t-indigo-600"></div>
      </div>
    );
  }

  const statCards = [
    {
      name: 'Total Projects',
      value: stats.projectsCount,
      icon: FolderKanban,
      color: 'text-indigo-600 bg-indigo-50 border-indigo-200',
      href: '/projects'
    },
    {
      name: 'Tasks Pending',
      value: stats.todoCount + stats.inProgressCount,
      icon: Clock,
      color: 'text-amber-600 bg-amber-50 border-amber-200',
      href: '/tasks'
    },
    {
      name: 'Tasks Completed',
      value: stats.doneCount,
      icon: CheckCircle2,
      color: 'text-emerald-600 bg-emerald-50 border-emerald-200',
      href: '/tasks?status=done'
    },
    {
      name: 'Total Tasks Created',
      value: stats.totalTasks,
      icon: CheckSquare,
      color: 'text-sky-600 bg-sky-50 border-sky-200',
      href: '/tasks'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 md:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold md:text-3xl text-slate-900">
                Welcome back, {user.name}!
              </h1>
              <p className="mt-2 text-sm text-slate-500">
                Here is a summary of what is happening across your company projects today.
              </p>
            </div>
            <div className="flex items-center gap-2 rounded-xl bg-indigo-50 border border-indigo-100 px-4 py-3 text-indigo-600">
              <TrendingUp className="h-5 w-5" />
              <span className="text-sm font-semibold">Active Sprint Active</span>
            </div>
          </div>
        </div>

        {/* Statistics Grid */}
        <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {statCards.map((card, index) => {
            const Icon = card.icon;
            return (
              <div
                key={index}
                className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div className={`rounded-lg p-2.5 border ${card.color.split(' ').slice(1).join(' ')}`}>
                    <Icon className={`h-5 w-5 ${card.color.split(' ')[0]}`} />
                  </div>
                  <Link 
                    href={card.href}
                    className="flex items-center gap-1 text-xs font-semibold text-slate-400 hover:text-indigo-600 transition"
                  >
                    View <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
                <div className="mt-4">
                  <p className="text-sm font-medium text-slate-500">{card.name}</p>
                  <h3 className="mt-1 text-3xl font-bold text-slate-900">
                    {fetching ? '...' : card.value}
                  </h3>
                </div>
              </div>
            );
          })}
        </div>

        {/* Roles Details */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-900">Role Guidelines</h3>
            <div className="mt-4 space-y-3 text-sm text-slate-600">
              <div className="flex items-start gap-2">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-650 bg-indigo-600" />
                <p>
                  <strong className="text-slate-900">Admin privileges:</strong> Create/update/delete projects, register new users, create new tasks, and assign them.
                </p>
              </div>
              <div className="flex items-start gap-2">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-600" />
                <p>
                  <strong className="text-slate-900">Developer privileges:</strong> View project lists, read task details, and transition status on tasks assigned to you.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-col justify-between rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Quick Actions</h3>
              <p className="mt-1 text-sm text-slate-500">Jump directly to task management boards or view open files.</p>
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                href="/tasks"
                className="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 transition"
              >
                Go to Tasks Board
              </Link>
              <Link
                href="/projects"
                className="rounded-lg bg-white border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              >
                View Project List
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
