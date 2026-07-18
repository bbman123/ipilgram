import { useState, useEffect, useCallback } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { listPreferences, type Preference } from "../api/preferences";

const langColors: Record<string, string> = {
  English: "bg-blue-100 text-blue-700",
  Hausa: "bg-emerald-100 text-emerald-700",
  Yoruba: "bg-amber-100 text-amber-700",
  Igbo: "bg-purple-100 text-purple-700",
  Arabic: "bg-red-100 text-red-700",
};

const modeColors: Record<string, string> = {
  Text: "bg-gray-100 text-gray-700",
  Audio: "bg-indigo-100 text-indigo-700",
  "Text + Audio": "bg-teal-100 text-teal-700",
};

export default function PreferencesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState<Preference[]>([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const page = Number(searchParams.get("page")) || 1;
  const search = searchParams.get("search") || "";
  const [searchInput, setSearchInput] = useState(search);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listPreferences(page, 10, search);
      setItems(data.items);
      setTotal(data.total);
      setPages(data.pages);
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setSearchParams({ search: searchInput, page: "1" });
  }

  function goToPage(p: number) {
    setSearchParams({ search, page: String(p) });
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">User Preferences</h1>
          <p className="text-gray-500 text-sm mt-1">{total} preferences configured</p>
        </div>
      </div>

      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search pilgrim name or email..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <button type="submit" className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
          Search
        </button>
        {search && (
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
                <th className="text-left px-4 py-3 font-medium text-gray-600">Pilgrim</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Language</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Delivery</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Font Size</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Notifications</th>
                <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-12 text-center text-gray-500">Loading...</td></tr>
              ) : items.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-12 text-center text-gray-500">No preferences found.</td></tr>
              ) : (
                items.map((p) => (
                  <tr key={p.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-900">{p.pilgrim_name || "-"}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full ${langColors[p.preferred_language] || "bg-gray-100 text-gray-700"}`}>
                        {p.preferred_language}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full ${modeColors[p.delivery_mode] || "bg-gray-100 text-gray-700"}`}>
                        {p.delivery_mode}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-600">{p.font_size}px</td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full ${p.notifications_enabled ? "bg-emerald-100 text-emerald-700" : "bg-red-100 text-red-700"}`}>
                        {p.notifications_enabled ? "On" : "Off"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <Link to={`/settings/${p.id}`} className="text-emerald-600 hover:text-emerald-800 text-xs">Edit</Link>
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
