import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getPackage, deletePackage, type PackageDetail } from "../api/packages";

export default function PackageDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [pkg, setPkg] = useState<PackageDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getPackage(Number(id))
      .then(setPkg)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

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
