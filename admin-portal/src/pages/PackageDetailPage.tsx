import { useState, useEffect, useCallback } from "react";
import { useNavigate, useParams, Link, useSearchParams } from "react-router-dom";
import { getPackage, deletePackage, getPackagePilgrims, type PackageDetail } from "../api/packages";
import type { Pilgrim } from "../api/pilgrims";

export default function PackageDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [pkg, setPkg] = useState<PackageDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [pilgrims, setPilgrims] = useState<Pilgrim[]>([]);
  const [pilgrimTotal, setPilgrimTotal] = useState(0);
  const [pilgrimPages, setPilgrimPages] = useState(1);
  const [pilgrimLoading, setPilgrimLoading] = useState(true);
  const [pilgrimPage, setPilgrimPage] = useState(1);
  const [pilgrimSearch, setPilgrimSearch] = useState("");
  const [pilgrimSearchInput, setPilgrimSearchInput] = useState("");

  const fetchPilgrims = useCallback(async () => {
    if (!id) return;
    setPilgrimLoading(true);
    try {
      const data = await getPackagePilgrims(Number(id), pilgrimPage, 10, pilgrimSearch);
      setPilgrims(data.items);
      setPilgrimTotal(data.total);
      setPilgrimPages(data.pages);
    } finally {
      setPilgrimLoading(false);
    }
  }, [id, pilgrimPage, pilgrimSearch]);

  useEffect(() => {
    if (!id) return;
    getPackage(Number(id))
      .then((p) => {
        setPkg(p);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    fetchPilgrims();
  }, [fetchPilgrims]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deletePackage(Number(id));
      navigate("/packages");
    } catch {
      setDeleting(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!pkg) {
    return <div className="text-center py-20 text-gray-500">Package not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{pkg.name}</h1>
          {pkg.description && <p className="text-gray-500 text-sm mt-1">{pkg.description}</p>}
        </div>
        <div className="flex items-center gap-2">
          <Link to={`/packages/${id}/edit`}
            className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            Edit
          </Link>
          <button onClick={() => setShowDelete(true)}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
            Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Package Details</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Created</div>
              <div className="text-sm text-gray-900">{new Date(pkg.created_at).toLocaleString()}</div>
            </div>
            <div>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Updated</div>
              <div className="text-sm text-gray-900">{new Date(pkg.updated_at).toLocaleString()}</div>
            </div>
          </div>
        </div>

        {pkg.flight && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Flight</h2>
              <Link to={`/flights/${pkg.flight.id}`} className="text-sm text-emerald-600 hover:text-emerald-800">View details</Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Airline</div>
                <div className="text-sm text-gray-900">{pkg.flight.airline}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Flight Number</div>
                <div className="text-sm text-gray-900">{pkg.flight.flight_number}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Route</div>
                <div className="text-sm text-gray-900">{pkg.flight.departure_airport} → {pkg.flight.arrival_airport}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Status</div>
                <span className="text-sm px-2 py-0.5 rounded-full bg-gray-100 text-gray-700 capitalize">{pkg.flight.status.replace("_", " ")}</span>
              </div>
            </div>
          </div>
        )}

        {pkg.accommodation && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Accommodation</h2>
              <Link to={`/accommodations/${pkg.accommodation.id}`} className="text-sm text-emerald-600 hover:text-emerald-800">View details</Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Hotel</div>
                <div className="text-sm text-gray-900">{pkg.accommodation.hotel_name}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Room</div>
                <div className="text-sm text-gray-900">{pkg.accommodation.room_number}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">City</div>
                <div className="text-sm text-gray-900">{pkg.accommodation.city}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Check-in / Check-out</div>
                <div className="text-sm text-gray-900">
                  {new Date(pkg.accommodation.check_in).toLocaleDateString()} — {new Date(pkg.accommodation.check_out).toLocaleDateString()}
                </div>
              </div>
            </div>
          </div>
        )}

        {pkg.transport && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Transport</h2>
              <Link to={`/transports/${pkg.transport.id}`} className="text-sm text-emerald-600 hover:text-emerald-800">View details</Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Vehicle</div>
                <div className="text-sm text-gray-900">{pkg.transport.bus_number}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Type</div>
                <span className="text-sm px-2 py-0.5 rounded-full bg-gray-100 text-gray-700 capitalize">{pkg.transport.transport_type}</span>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Route</div>
                <div className="text-sm text-gray-900">{pkg.transport.pickup_location} → {pkg.transport.destination}</div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Driver</div>
                <div className="text-sm text-gray-900">{pkg.transport.driver_name}</div>
              </div>
            </div>
          </div>
        )}

        {!pkg.flight && !pkg.accommodation && !pkg.transport && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-500 text-center py-4">No flight, accommodation, or transport assigned to this package yet.</p>
          </div>
        )}

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Assigned Pilgrims</h2>
              <p className="text-gray-500 text-sm mt-0.5">{pilgrimTotal} pilgrim{pilgrimTotal !== 1 ? "s" : ""} in this package</p>
            </div>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); setPilgrimSearch(pilgrimSearchInput); setPilgrimPage(1); }}
            className="mb-3 flex gap-2">
            <input
              type="text"
              value={pilgrimSearchInput}
              onChange={(e) => setPilgrimSearchInput(e.target.value)}
              placeholder="Search pilgrims..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button type="submit" className="px-3 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800">
              Search
            </button>
            {pilgrimSearch && (
              <button type="button" onClick={() => { setPilgrimSearchInput(""); setPilgrimSearch(""); setPilgrimPage(1); }}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50">
                Clear
              </button>
            )}
          </form>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Phone</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                  <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {pilgrimLoading ? (
                  <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-500">Loading...</td></tr>
                ) : pilgrims.length === 0 ? (
                  <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-500">
                    {pilgrimSearch ? "No pilgrims match your search." : "No pilgrims assigned to this package yet."}
                  </td></tr>
                ) : (
                  pilgrims.map((p) => (
                    <tr key={p.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <Link to={`/pilgrims/${p.id}`} className="text-gray-900 font-medium hover:text-emerald-600">
                          {p.full_name}
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-gray-600">{p.email}</td>
                      <td className="px-4 py-3 text-gray-600">{p.phone || "-"}</td>
                      <td className="px-4 py-3">
                        <span className={`inline-block text-xs px-2 py-0.5 rounded-full ${p.is_active ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>
                          {p.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Link to={`/pilgrims/${p.id}`} className="text-gray-500 hover:text-gray-700 text-xs">View</Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {pilgrimPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 mt-3">
              <span className="text-sm text-gray-500">Page {pilgrimPage} of {pilgrimPages}</span>
              <div className="flex gap-1">
                <button onClick={() => setPilgrimPage(pilgrimPage - 1)} disabled={pilgrimPage <= 1}
                  className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 hover:bg-gray-50">Prev</button>
                <button onClick={() => setPilgrimPage(pilgrimPage + 1)} disabled={pilgrimPage >= pilgrimPages}
                  className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 hover:bg-gray-50">Next</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {showDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Package?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove package <strong>{pkg.name}</strong>. Assigned pilgrims will be unlinked. This action cannot be undone.
            </p>
            <div className="flex items-center gap-3 justify-end">
              <button onClick={() => setShowDelete(false)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50">Cancel</button>
              <button onClick={handleDelete} disabled={deleting}
                className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50">
                {deleting ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
