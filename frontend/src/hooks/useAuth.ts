import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'developer';
  created_at: string;
}

export function useAuth(requireAuth = true) {
  const router = useRouter();
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedUser = localStorage.getItem('user');
      const token = localStorage.getItem('token');

      if (!token || !storedUser) {
        if (requireAuth) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          router.push('/login');
        } else {
          setLoading(false);
        }
      } else {
        setUser(JSON.parse(storedUser));
        setLoading(false);
      }
    }
  }, [router, requireAuth]);

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    }
  };

  return { user, loading, logout };
}
