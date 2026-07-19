import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getActiveAnnouncements, type Announcement } from "../api/announcements";
import apiClient from "../api/client";

interface DashboardStats {
  total_pilgrims: number;
  total_packages: number;
  total_flights: number;
  total_accommodations: number;
  total_transports: number;
  total_announcements: number;
  total_notifications: number;
  total_preferences: number;
  active_pilgrims: number;
}

const targetColors: Record<string, string> = {
  all: "bg-indigo-100 text-indigo-700",
  pilgrim: "bg-emerald-100 text-emerald-700",
  package: "bg-amber-100 text-amber-700",
  flight: "bg-blue-100 text-blue-700",
  accommodation: "bg-teal-100 text-teal-700",
  transport: "bg-orange-100 text-orange-700",
};

const priorityColors: Record<string, string> = {
  low: "bg-gray-100 text-gray-600",
  medium: "bg-blue-100 text-blue-600",
  high: "bg-amber-100 text-amber-700",
  urgent: "bg-red-100 text-red-700",
};

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activeAnnouncements, setActiveAnnouncements] = useState<Announcement[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingAnnouncements, setLoadingAnnouncements] = useState(true);

  useEffect(() => {
    apiClient
      .get<DashboardStats>("/stats")
      .then((res) => setStats(res.data))
      .catch(() => {})
      .finally(() => setLoadingStats(false));
  }, []);

  useEffect(() => {
    getActiveAnnouncements()
      .then(setActiveAnnouncements)
      .catch(() => {})
      .finally(() => setLoadingAnnouncements(false));
  }, []);

  const statCards = [
    { label: "Total Pilgrims", value: stats?.total_pilgrims ?? 0, color: "bg-emerald-50 text-emerald-700" },
    { label: "Active Pilgrims", value: stats?.active_pilgrims ?? 0, color: "bg-green-50 text-green-700" },
    { label: "Packages", value: stats?.total_packages ?? 0, color: "bg-amber-50 text-amber-700" },
    { label: "Flights", value: stats?.total_flights ?? 0, color: "bg-blue-50 text-blue-700" },
    { label: "Accommodations", value: stats?.total_accommodations ?? 0, color: "bg-teal-50 text-teal-700" },
    { label: "Transports", value: stats?.total_transports ?? 0, color: "bg-orange-50 text-orange-700" },
    { label: "Announcements", value: stats?.total_announcements ?? 0, color: "bg-indigo-50 text-indigo-700" },
    { label: "Notifications", value: stats?.total_notifications ?? 0, color: "bg-purple-50 text-purple-700" },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Welcome back, {user?.full_name}
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-xl border border-gray-200 p-5"
          >
            <div className={`inline-block text-xs font-medium px-2 py-1 rounded-full mb-3 ${stat.color}`}>
              {stat.label}
            </div>
            <div className="text-3xl font-bold text-gray-900">
              {loadingStats ? (
                <span className="text-gray-300">...</span>
              ) : (
                stat.value
              )}
            </div>
          </div>
        ))}
      </div>

      {activeAnnouncements.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Active Announcements</h2>
            <Link to="/announcements" className="text-sm text-emerald-600 hover:text-emerald-700 font-medium">View all</Link>
          </div>
          <div className="space-y-3">
            {activeAnnouncements.map((a) => (
              <Link
                key={a.id}
                to={`/announcements/${a.id}`}
                className="flex items-center gap-3 p-3 rounded-lg border border-gray-100 hover:border-emerald-200 hover:bg-emerald-50 transition-colors"
              >
                <span className={`text-xs px-2 py-0.5 rounded-full capitalize shrink-0 ${priorityColors[a.priority]}`}>
                  {a.priority}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full capitalize shrink-0 ${targetColors[a.target_type]}`}>
                  {a.target_type === "all" ? "All" : a.target_type}
                </span>
                <span className="text-sm font-medium text-gray-900 line-clamp-1 flex-1">{a.title}</span>
                <span className="text-xs text-gray-500 shrink-0">
                  {new Date(a.expiry_date).toLocaleDateString()}
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {activeAnnouncements.length === 0 && !loadingAnnouncements && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Active Announcements</h2>
            <Link to="/announcements/new" className="text-sm text-emerald-600 hover:text-emerald-700 font-medium">Create one</Link>
          </div>
          <p className="text-sm text-gray-500">No active announcements at the moment.</p>
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <Link to="/pilgrims/new"
            className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 transition-colors text-left">
            <div className="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
              </svg>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900">Add Pilgrim</div>
              <div className="text-xs text-gray-500">Register new user</div>
            </div>
          </Link>

          <Link to="/flights/new"
            className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors text-left">
            <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
              </svg>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900">Add Flight</div>
              <div className="text-xs text-gray-500">Schedule a flight</div>
            </div>
          </Link>

          <Link to="/transports/new"
            className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-orange-300 hover:bg-orange-50 transition-colors text-left">
            <div className="w-10 h-10 bg-orange-100 text-orange-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 17h8M5 10h14a2 2 0 012 2v7a2 2 0 01-2 2H5a2 2 0 01-2-2v-7a2 2 0 012-2zM3 17v3M21 17v3M7 14v-1M12 14v-1M17 14v-1" />
              </svg>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900">Add Transport</div>
              <div className="text-xs text-gray-500">Schedule transport</div>
            </div>
          </Link>

          <Link to="/notifications"
            className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-colors text-left">
            <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900">Send Notification</div>
              <div className="text-xs text-gray-500">Push to mobile</div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
