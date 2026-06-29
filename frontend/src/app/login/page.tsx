'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';
import { LogIn, Key, User, ShieldAlert } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Redirect if already logged in
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        router.push('/dashboard');
      }
    }
  }, [router]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      router.push('/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        'Failed to connect to the server. Please check your credentials or backend status.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFillCredentials = (role: 'admin' | 'dev') => {
    if (role === 'admin') {
      setEmail('admin@taskflow.com');
      setPassword('AdminPass123!');
    } else {
      setEmail('dev@taskflow.com');
      setPassword('DevPass123!');
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center bg-slate-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 rounded-2xl border border-slate-200 bg-white p-8 shadow-lg">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
            Task<span className="text-indigo-600">Flow</span>
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Sign in to manage company projects and tasks
          </p>
        </div>

        {error && (
          <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-600">
            <ShieldAlert className="h-5 w-5 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="space-y-4 rounded-md">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <User className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full rounded-lg border border-slate-300 bg-white py-3 pl-10 pr-3 text-sm text-slate-900 placeholder-slate-400 shadow-sm focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600 focus:outline-none"
                  placeholder="name@company.com"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <Key className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full rounded-lg border border-slate-300 bg-white py-3 pl-10 pr-3 text-sm text-slate-900 placeholder-slate-400 shadow-sm focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600 focus:outline-none"
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
            >
              {loading ? (
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-white/30 border-t-white"></div>
              ) : (
                <span className="flex items-center gap-2">
                  <LogIn className="h-4 w-4" /> Sign In
                </span>
              )}
            </button>
          </div>
        </form>

        <div className="mt-6 border-t border-slate-200 pt-6">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Quick Fill Demo Accounts:
          </p>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <button
              onClick={() => handleFillCredentials('admin')}
              className="flex flex-col items-start rounded-lg border border-slate-200 bg-slate-50 p-3 text-left hover:border-slate-300 transition"
            >
              <span className="text-xs font-semibold text-indigo-600">Admin</span>
              <span className="mt-1 text-[10px] text-slate-500">Full Access</span>
            </button>
            <button
              onClick={() => handleFillCredentials('dev')}
              className="flex flex-col items-start rounded-lg border border-slate-200 bg-slate-50 p-3 text-left hover:border-slate-300 transition"
            >
              <span className="text-xs font-semibold text-emerald-600">Developer</span>
              <span className="mt-1 text-[10px] text-slate-500">Assigned Tasks Only</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
