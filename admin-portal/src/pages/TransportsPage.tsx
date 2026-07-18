import { useState, useEffect, useCallback } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { listTransports, type Transport } from "../api/transports";

const typeColors: Record<string, string> = {
  bus: "bg-blue-100 text-blue-700",
  van: "bg-indigo-100 text-indigo-700",
  taxi: "bg-amber-100 text-amber-700",
  car: "bg-emerald-100 text-emerald-700",
  other: "bg-gray-100 text-gray-700",
};

export default function TransportsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState<Transport[]>([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const page = Number(searchParams.get("page")) || 1;
  const search = searchParams.get("search") || "";
  const typeFilter = searchParams.get("type") || "";
  const [searchInput, setSearchInput] = useState(search);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listTransports(page, 10, search, typeFilter || undefined);
      setItems(data.items);
      setTotal(data.total);
      setPages(data.pages);
    } finally {
      setLoading(false);
    }
  }, [page, search, typeFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const params: Record<string, string> = { page: "1" };
    if (searchInput) params.search = searchInput;
    if (typeFilter) params.type = typeFilter;
    setSearchParams(params);
  }

  function goToPage(p: number) {
    const params: Record<string, string> = { page: String(p) };
    if (search) params.search = search;
    if (typeFilter) params.type = typeFilter;
    setSearchParams(params);
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Transports</h1>
          <p className="text-gray-500 text-sm mt-1">{total} transport records</p>
        </div>
        <Link
          to="/transports/new"
          className="inline-flex items-center gap-2 bg-emerald-600 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Add Transport
        </Link>
      </div>

      <form onSubmit={handleSearch} className="mb-4 flex flex-col sm:flex-row gap-2">
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search bus number, driver, location..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <select
          value={typeFilter}
          onChange={(e) => {
            const v = e.target.value;
            const params: Record<string, string> = { page: "1" };
            if (search) params.search = search;
            if (v) params.type = v;
            setSearchParams(params);
          }}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          <option value="">All Types</option>
          <option value="bus">Bus</option>
          <option value="van">Van</option>
          <option value="taxi">Taxi</option>
          <option value="car">Car</option>
          <option value="other">Other</option>
        </select>
        <button type="submit" className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors">
          Search
        </button>
        {(search || typeFilter) && (
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
                <th className="text-left px-4 py-3 font-medium text-gray-600">Bus/Vehicle</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Type</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Route</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Pickup Time</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Driver</th>
                <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={7} className="px-4 py-12 text-center text-gray-500">Loading...</td></tr>
              ) : items.length === 0 ? (
                <tr><td colSpan={7} className="px-4 py-12 text-center text-gray-500">No transports found.</td></tr>
              ) : (
                items.map((t) => (
                  <tr key={t.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-900">{t.pilgrim_name || "-"}</td>
                    <td className="px-4 py-3 font-mono text-gray-900">{t.bus_number}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-block text-xs px-2 py-0.5 rounded-full capitalize ${typeColors[t.transport_type] || "bg-gray-100 text-gray-700"}`}>
                        {t.transport_type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-600">{t.pickup_location} → {t.destination}</td>
                    <td className="px-4 py-3 text-gray-600">{new Date(t.pickup_time).toLocaleString()}</td>
                    <td className="px-4 py-3 text-gray-600">{t.driver_name}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link to={`/transports/${t.id}`} className="text-gray-500 hover:text-gray-700 text-xs">View</Link>
                        <Link to={`/transports/${t.id}/edit`} className="text-emerald-600 hover:text-emerald-800 text-xs">Edit</Link>
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
