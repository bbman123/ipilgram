import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getPilgrim, deletePilgrim, type Pilgrim } from "../api/pilgrims";

export default function PilgrimDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [pilgrim, setPilgrim] = useState<Pilgrim | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getPilgrim(Number(id))
      .then(setPilgrim)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deletePilgrim(Number(id));
      navigate("/pilgrims");
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

  if (!pilgrim) {
    return (
      <div className="text-center py-20 text-gray-500">Pilgrim not found.</div>
    );
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{pilgrim.full_name}</h1>
          <p className="text-gray-500 text-sm mt-1">{pilgrim.email}</p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            to={`/pilgrims/${id}/edit`}
            className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"
          >
            Edit
          </Link>
          <button
            onClick={() => setShowDelete(true)}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            { label: "Phone", value: pilgrim.phone || "-" },
            { label: "Nationality", value: pilgrim.nationality || "-" },
            { label: "Passport Number", value: pilgrim.passport_number || "-" },
            { label: "Status", value: pilgrim.is_active ? "Active" : "Inactive", badge: true },
            { label: "Created", value: new Date(pilgrim.created_at).toLocaleDateString() },
            { label: "Updated", value: new Date(pilgrim.updated_at).toLocaleDateString() },
          ].map((field) => (
            <div key={field.label}>
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                {field.label}
              </div>
              {field.badge ? (
                <span className={`text-sm px-2 py-0.5 rounded-full ${pilgrim.is_active ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>
                  {field.value}
                </span>
              ) : (
                <div className="text-sm text-gray-900">{field.value}</div>
              )}
            </div>
          ))}
          {pilgrim.emergency_contact && (
            <div className="sm:col-span-2">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                Emergency Contact
              </div>
              <div className="text-sm text-gray-900 whitespace-pre-wrap">{pilgrim.emergency_contact}</div>
            </div>
          )}
        </div>
      </div>

      {showDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Pilgrim?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove <strong>{pilgrim.full_name}</strong>. This action cannot be undone.
            </p>
            <div className="flex items-center gap-3 justify-end">
              <button
                onClick={() => setShowDelete(false)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50"
              >
                {deleting ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
