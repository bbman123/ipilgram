import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getFlight, deleteFlight, type Flight } from "../api/flights";

const statusColors: Record<string, string> = {
  scheduled: "bg-gray-100 text-gray-700",
  confirmed: "bg-blue-100 text-blue-700",
  boarding: "bg-amber-100 text-amber-700",
  departed: "bg-purple-100 text-purple-700",
  in_air: "bg-indigo-100 text-indigo-700",
  landed: "bg-emerald-100 text-emerald-700",
  cancelled: "bg-red-100 text-red-700",
  delayed: "bg-orange-100 text-orange-700",
};

export default function FlightDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [flight, setFlight] = useState<Flight | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getFlight(Number(id))
      .then(setFlight)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deleteFlight(Number(id));
      navigate("/flights");
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

  if (!flight) {
    return <div className="text-center py-20 text-gray-500">Flight not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{flight.flight_number}</h1>
          <p className="text-gray-500 text-sm mt-1">{flight.airline}</p>
        </div>
        <div className="flex items-center gap-2">
          <Link to={`/flights/${id}/edit`}
            className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors">
            Edit
          </Link>
          <button onClick={() => setShowDelete(true)}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
            Delete
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            { label: "Pilgrim", value: flight.pilgrim_name || "-" },
            { label: "Pilgrim Email", value: flight.pilgrim_email || "-" },
            { label: "Route", value: `${flight.departure_airport} → ${flight.arrival_airport}` },
            { label: "Status", value: flight.status.replace("_", " "), badge: true },
            { label: "Departure", value: new Date(flight.departure_datetime).toLocaleString() },
            { label: "Arrival", value: new Date(flight.arrival_datetime).toLocaleString() },
            { label: "Gate", value: flight.gate || "-" },
            { label: "Seat", value: flight.seat_number || "-" },
            { label: "Created", value: new Date(flight.created_at).toLocaleDateString() },
            { label: "Updated", value: new Date(flight.updated_at).toLocaleDateString() },
          ].map((field) => (
            <div key={field.label}>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">{field.label}</div>
              {field.badge ? (
                <span className={`text-sm px-2 py-0.5 rounded-full capitalize ${statusColors[flight.status] || "bg-gray-100 text-gray-700"}`}>
                  {field.value}
                </span>
              ) : (
                <div className="text-sm text-gray-900">{field.value}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {showDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Flight?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove flight <strong>{flight.flight_number}</strong>. This action cannot be undone.
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
