import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getPreference,
  updatePreference,
  createPreference,
  type Preference,
} from "../api/preferences";
import { listPilgrims, type Pilgrim } from "../api/pilgrims";

export default function PreferenceEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [pilgrims, setPilgrims] = useState<Pilgrim[]>([]);

  const [pilgrimId, setPilgrimId] = useState("");
  const [preferredLanguage, setPreferredLanguage] = useState("English");
  const [deliveryMode, setDeliveryMode] = useState("Text");
  const [fontSize, setFontSize] = useState(16);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [isEdit, setIsEdit] = useState(false);

  useEffect(() => {
    listPilgrims(1, 100).then((d) => setPilgrims(d.items)).catch(() => {});

    if (id) {
      getPreference(Number(id))
        .then((p) => {
          setIsEdit(true);
          setPilgrimId(String(p.pilgrim_id));
          setPreferredLanguage(p.preferred_language);
          setDeliveryMode(p.delivery_mode);
          setFontSize(p.font_size);
          setNotificationsEnabled(p.notifications_enabled);
        })
        .catch(() => setError("Failed to load preference"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      if (isEdit && id) {
        await updatePreference(Number(id), {
          preferred_language: preferredLanguage as Preference["preferred_language"],
          delivery_mode: deliveryMode as Preference["delivery_mode"],
          font_size: fontSize,
          notifications_enabled: notificationsEnabled,
        });
        navigate("/settings");
      } else {
        if (!pilgrimId) {
          setError("Please select a pilgrim");
          setSaving(false);
          return;
        }
        await createPreference({
          pilgrim_id: Number(pilgrimId),
          preferred_language: preferredLanguage as Preference["preferred_language"],
          delivery_mode: deliveryMode as Preference["delivery_mode"],
          font_size: fontSize,
          notifications_enabled: notificationsEnabled,
        });
        navigate("/settings");
      }
    } catch {
      setError("Failed to save preference");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {isEdit ? "Edit Preference" : "Create Preference"}
        </h1>
        <p className="text-gray-500 text-sm mt-1">
          {isEdit ? "Update pilgrim preferences" : "Set preferences for a pilgrim"}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

        {!isEdit && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Pilgrim *</label>
            <select value={pilgrimId} onChange={(e) => setPilgrimId(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">Select a pilgrim</option>
              {pilgrims.map((p) => (
                <option key={p.id} value={p.id}>{p.full_name} ({p.email})</option>
              ))}
            </select>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Preferred Language</label>
            <select value={preferredLanguage} onChange={(e) => setPreferredLanguage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="English">English</option>
              <option value="Hausa">Hausa</option>
              <option value="Yoruba">Yoruba</option>
              <option value="Igbo">Igbo</option>
              <option value="Arabic">Arabic</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Delivery Mode</label>
            <select value={deliveryMode} onChange={(e) => setDeliveryMode(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="Text">Text</option>
              <option value="Audio">Audio</option>
              <option value="Text + Audio">Text + Audio</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Font Size: <span className="font-bold">{fontSize}px</span>
          </label>
          <input
            type="range"
            min={8}
            max={48}
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
            className="w-full accent-emerald-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>8px (Small)</span>
            <span>48px (Large)</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Notifications</label>
          <button
            type="button"
            onClick={() => setNotificationsEnabled(!notificationsEnabled)}
            className={`relative w-11 h-6 rounded-full transition-colors ${notificationsEnabled ? "bg-emerald-600" : "bg-gray-300"}`}
          >
            <span className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${notificationsEnabled ? "translate-x-5" : ""}`} />
          </button>
          <span className="text-sm text-gray-600">{notificationsEnabled ? "Enabled" : "Disabled"}</span>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={saving}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            {saving ? "Saving..." : isEdit ? "Save Changes" : "Create Preference"}
          </button>
          <button type="button" onClick={() => navigate("/settings")}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
