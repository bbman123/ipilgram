import { useState, useEffect, useCallback } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { listAnnouncements, type Announcement } from "../api/announcements";

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

const targetTypeOptions = [
  { value: "", label: "All Targets" },
  { value: "all", label: "All Pilgrims" },
  { value: "pilgrim", label: "Pilgrim" },
  { value: "package", label: "Package" },
  { value: "flight", label: "Flight" },
  { value: "accommodation", label: "Accommodation" },
  { value: "transport", label: "Transport" },
];

export default function AnnouncementsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState<Announcement[]>([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const page = Number(searchParams.get("page")) || 1;
  const search = searchParams.get("search") || "";
  const priorityFilter = searchParams.get("priority") || "";
  const targetTypeFilter = searchParams.get("target_type") || "";
  const [searchInput, setSearchInput] = useState(search);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listAnnouncements(
        page, 10, search,
        priorityFilter || undefined,
        targetTypeFilter || undefined,
      );
      setItems(data.items);
      setTotal(data.total);
      setPages(data.pages);
    } finally {
      setLoading(false);
    }
  }, [page, search, priorityFilter, targetTypeFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const params: Record<string, string> = { page: "1" };
    if (searchInput) params.search = searchInput;
    if (priorityFilter) params.priority = priorityFilter;
    if (targetTypeFilter) params.target_type = targetTypeFilter;
    setSearchParams(params);
  }

  function goToPage(p: number) {
    const params: Record<string, string> = { page: String(p) };
    if (search) params.search = search;
    if (priorityFilter) params.priority = priorityFilter;
    if (targetTypeFilter) params.target_type = targetTypeFilter;
    setSearchParams(params);
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Announcements</h1>
          <p className="text-gray-500 text-sm mt-1">{total} announcements published</p>
        </div>
        <Link
          to="/announcements/new"
          className="inline-flex items-center gap-2 bg-emerald-600 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          New Announcement
        </Link>
      </div>

      <form onSubmit={handleSearch} className="mb-4 flex flex-col sm:flex-row gap-2">
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search title or message..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <select
          value={targetTypeFilter}
          onChange={(e) => {
            const v = e.target.value;
            const params: Record<string, string> = { page: "1" };
            if (searchInput) params.search = searchInput;
            if (v) params.target_type = v;
            if (priorityFilter) params.priority = priorityFilter;
            setSearchParams(params);
          }}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          {targetTypeOptions.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <select
          value={priorityFilter}
          onChange={(e) => {
            const v = e.target.value;
            const params: Record<string, string> = { page: "1" };
            if (searchInput) params.search = searchInput;
            if (targetTypeFilter) params.target_type = targetTypeFilter;
            if (v) params.priority = v;
            setSearchParams(params);
          }}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>
        <button type="submit" className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
          Search
        </button>
        {(search || priorityFilter || targetTypeFilter) && (
          <button
            type="button"
            onClick={() => { setSearchInput(""); setSearchParams({ page: "1" }); }}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors"
          >
            Clear
          </button>
        )}
      </form>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left px-4 py-3 font-medium text-gray-600">Title</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Target</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Priority</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Publish</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Expiry</th>
                <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-12 text-center text-gray-500">Loading...</td></tr>
              ) : items.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-12 text-center text-gray-500">No announcements found.</td></tr>
              ) : (
                items.map((a) => (
                  <tr key={a.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <Link to={`/announcements/${a.id}`} className="text-gray-900 font-medium hover:text-emerald-600 line-clamp-1">
                        {a.title}
                      </Link>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full capitalize ${targetColors[a.target_type]}`}>
                        {a.target_type === "all" ? "All" : a.target_type}
                        {a.target_id ? ` #${a.target_id}` : ""}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full capitalize ${priorityColors[a.priority]}`}>
                        {a.priority}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-600">{new Date(a.publish_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3 text-gray-600">{new Date(a.expiry_date).toLocaleDateString()}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link to={`/announcements/${a.id}`} className="text-gray-500 hover:text-gray-700 text-xs">View</Link>
                        <Link to={`/announcements/${a.id}/edit`} className="text-emerald-600 hover:text-emerald-800 text-xs">Edit</Link>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {pages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200">
            <span className="text-sm text-gray-500">Page {page} of {pages}</span>
            <div className="flex gap-1">
              <button onClick={() => goToPage(page - 1)} disabled={page <= 1}
                className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50">Prev</button>
              <button onClick={() => goToPage(page + 1)} disabled={page >= pages}
                className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50">Next</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
