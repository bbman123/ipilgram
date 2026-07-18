import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getTransport, deleteTransport, type Transport } from "../api/transports";

const typeColors: Record<string, string> = {
  bus: "bg-blue-100 text-blue-700",
  van: "bg-indigo-100 text-indigo-700",
  taxi: "bg-amber-100 text-amber-700",
  car: "bg-emerald-100 text-emerald-700",
  other: "bg-gray-100 text-gray-700",
};

export default function TransportDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [t, setT] = useState<Transport | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getTransport(Number(id))
      .then(setT)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deleteTransport(Number(id));
      navigate("/transports");
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

  if (!t) {
    return <div className="text-center py-20 text-gray-500">Transport not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t.bus_number}</h1>
          <p className="text-gray-500 text-sm mt-1">{t.driver_name}</p>
        </div>
        <div className="flex items-center gap-2">
          <Link to={`/transports/${id}/edit`}
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
            { label: "Pilgrim", value: t.pilgrim_name || "-" },
            { label: "Pilgrim Email", value: t.pilgrim_email || "-" },
            { label: "Bus/Vehicle Number", value: t.bus_number },
            { label: "Transport Type", value: t.transport_type, badge: true },
            { label: "Pickup Location", value: t.pickup_location },
            { label: "Destination", value: t.destination },
            { label: "Pickup Time", value: new Date(t.pickup_time).toLocaleString() },
            { label: "Driver Name", value: t.driver_name },
            { label: "Driver Phone", value: t.driver_phone },
            { label: "Created", value: new Date(t.created_at).toLocaleDateString() },
          ].map((field) => (
            <div key={field.label}>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">{field.label}</div>
              {field.badge ? (
                <span className={`text-sm px-2 py-0.5 rounded-full capitalize ${typeColors[t.transport_type] || "bg-gray-100 text-gray-700"}`}>
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
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Transport?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove transport <strong>{t.bus_number}</strong>. This action cannot be undone.
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
