import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getAccommodation, deleteAccommodation, type Accommodation } from "../api/accommodations";

export default function AccommodationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [acc, setAcc] = useState<Accommodation | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getAccommodation(Number(id))
      .then(setAcc)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deleteAccommodation(Number(id));
      navigate("/accommodations");
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

  if (!acc) {
    return <div className="text-center py-20 text-gray-500">Accommodation not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{acc.hotel_name}</h1>
          <p className="text-gray-500 text-sm mt-1">{acc.city}</p>
        </div>
        <div className="flex items-center gap-2">
          <Link to={`/accommodations/${id}/edit`}
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
            { label: "Pilgrim", value: acc.pilgrim_name || "-" },
            { label: "Pilgrim Email", value: acc.pilgrim_email || "-" },
            { label: "City", value: acc.city },
            { label: "Building", value: acc.building || "-" },
            { label: "Floor", value: acc.floor || "-" },
            { label: "Room Number", value: acc.room_number },
            { label: "Bed Number", value: acc.bed_number || "-" },
            { label: "Check-in", value: new Date(acc.check_in).toLocaleString() },
            { label: "Check-out", value: new Date(acc.check_out).toLocaleString() },
            { label: "Created", value: new Date(acc.created_at).toLocaleDateString() },
          ].map((field) => (
            <div key={field.label}>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">{field.label}</div>
              <div className="text-sm text-gray-900">{field.value}</div>
            </div>
          ))}
          {acc.address && (
            <div className="sm:col-span-2">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Address</div>
              <div className="text-sm text-gray-900">{acc.address}</div>
            </div>
          )}
        </div>
      </div>

      {showDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Accommodation?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove <strong>{acc.hotel_name}</strong> (Room {acc.room_number}). This action cannot be undone.
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
