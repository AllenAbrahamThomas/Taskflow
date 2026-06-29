import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LogOut, FolderKanban, CheckSquare, LayoutDashboard, User } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export default function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth(true);

  if (!user) return null;

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Projects', href: '/projects', icon: FolderKanban },
    { name: 'Tasks', href: '/tasks', icon: CheckSquare },
  ];

  return (
    <nav className="border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center text-xl font-bold text-slate-900">
              Task<span className="text-indigo-600">Flow</span>
            </Link>
            
            {/* Tabs */}
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => {
                const isActive = pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition ${
                      isActive
                        ? 'bg-indigo-55 bg-indigo-50 text-indigo-600'
                        : 'text-slate-650 text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* User Details & Logout */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 border-r border-slate-200 pr-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
                <User className="h-4 w-4" />
              </div>
              <div className="text-left">
                <p className="text-xs font-semibold text-slate-900">{user.name}</p>
                <span className={`inline-flex items-center rounded-full px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wider ${
                  user.role === 'admin' 
                    ? 'bg-indigo-50 text-indigo-600 border border-indigo-200' 
                    : 'bg-emerald-50 text-emerald-600 border border-emerald-200'
                }`}>
                  {user.role}
                </span>
              </div>
            </div>

            <button
              onClick={logout}
              className="flex items-center gap-2 rounded-md bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-200 hover:text-slate-900"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
