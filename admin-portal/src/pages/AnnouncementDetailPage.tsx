import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getAnnouncement, deleteAnnouncement, type Announcement } from "../api/announcements";

const categoryColors: Record<string, string> = {
  emergency: "bg-red-100 text-red-700",
  general: "bg-gray-100 text-gray-700",
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

export default function AnnouncementDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [a, setA] = useState<Announcement | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDelete, setShowDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    getAnnouncement(Number(id))
      .then(setA)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  async function handleDelete() {
    if (!id) return;
    setDeleting(true);
    try {
      await deleteAnnouncement(Number(id));
      navigate("/announcements");
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

  if (!a) {
    return <div className="text-center py-20 text-gray-500">Announcement not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{a.title}</h1>
          <p className="text-gray-500 text-sm mt-1">
            Published {new Date(a.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link to={`/announcements/${id}/edit`}
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
        <div className="flex items-center gap-2 mb-4">
          <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${categoryColors[a.category]}`}>{a.category}</span>
          <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${priorityColors[a.priority]}`}>{a.priority}</span>
          <span className="text-xs text-gray-500 uppercase">{a.language}</span>
        </div>

        <div className="text-sm text-gray-700 whitespace-pre-wrap mb-6">{a.message}</div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-gray-200 pt-4">
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Publish Date</div>
            <div className="text-sm text-gray-900">{new Date(a.publish_date).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Expiry Date</div>
            <div className="text-sm text-gray-900">{new Date(a.expiry_date).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Created</div>
            <div className="text-sm text-gray-900">{new Date(a.created_at).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Updated</div>
            <div className="text-sm text-gray-900">{new Date(a.updated_at).toLocaleString()}</div>
          </div>
        </div>
      </div>

      {showDelete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Announcement?</h3>
            <p className="text-sm text-gray-600 mb-6">
              This will permanently remove <strong>{a.title}</strong>. This action cannot be undone.
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
