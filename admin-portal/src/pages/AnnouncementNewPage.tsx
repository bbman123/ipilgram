import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createAnnouncement } from "../api/announcements";

export default function AnnouncementNewPage() {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [showPreview, setShowPreview] = useState(false);

  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const [category, setCategory] = useState("general");
  const [language, setLanguage] = useState("en");
  const [priority, setPriority] = useState("medium");
  const [publishDate, setPublishDate] = useState("");
  const [expiryDate, setExpiryDate] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const a = await createAnnouncement({
        title,
        message,
        category: category as "general",
        language,
        priority: priority as "medium",
        publish_date: publishDate,
        expiry_date: expiryDate,
      });
      navigate(`/announcements/${a.id}`);
    } catch {
      setError("Failed to create announcement. Check all fields.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">New Announcement</h1>
          <p className="text-gray-500 text-sm mt-1">Create and publish an announcement</p>
        </div>
        <button
          onClick={() => setShowPreview(!showPreview)}
          className="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors"
        >
          {showPreview ? "Editor" : "Preview"}
        </button>
      </div>

      {showPreview ? (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${
              category === "emergency" ? "bg-red-100 text-red-700" :
              category === "flight" ? "bg-blue-100 text-blue-700" :
              category === "accommodation" ? "bg-teal-100 text-teal-700" :
              category === "transport" ? "bg-orange-100 text-orange-700" :
              "bg-gray-100 text-gray-700"
            }`}>{category}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${
              priority === "urgent" ? "bg-red-100 text-red-700" :
              priority === "high" ? "bg-amber-100 text-amber-700" :
              priority === "medium" ? "bg-blue-100 text-blue-600" :
              "bg-gray-100 text-gray-600"
            }`}>{priority}</span>
            <span className="text-xs text-gray-500 uppercase">{language}</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-3">{title || "Untitled"}</h2>
          <div className="text-sm text-gray-700 whitespace-pre-wrap mb-4">{message || "No message content."}</div>
          <div className="flex gap-4 text-xs text-gray-500 border-t border-gray-200 pt-3">
            <span>Publish: {publishDate ? new Date(publishDate).toLocaleString() : "-"}</span>
            <span>Expiry: {expiryDate ? new Date(expiryDate).toLocaleString() : "-"}</span>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
          {error && (
            <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required
              placeholder="Announcement title"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Message *</label>
            <textarea value={message} onChange={(e) => setMessage(e.target.value)} required rows={5}
              placeholder="Write the announcement message..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category *</label>
              <select value={category} onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                <option value="general">General</option>
                <option value="emergency">Emergency</option>
                <option value="flight">Flight</option>
                <option value="accommodation">Accommodation</option>
                <option value="transport">Transport</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Priority *</label>
              <select value={priority} onChange={(e) => setPriority(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
              <select value={language} onChange={(e) => setLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                <option value="en">English</option>
                <option value="ar">Arabic</option>
                <option value="ha">Hausa</option>
                <option value="fr">French</option>
              </select>
            </div>
            <div></div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Publish Date *</label>
              <input type="datetime-local" value={publishDate} onChange={(e) => setPublishDate(e.target.value)} required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expiry Date *</label>
              <input type="datetime-local" value={expiryDate} onChange={(e) => setExpiryDate(e.target.value)} required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            </div>
          </div>

          <div className="flex items-center gap-3 pt-2">
            <button type="submit" disabled={saving}
              className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
              {saving ? "Publishing..." : "Publish Announcement"}
            </button>
            <button type="button" onClick={() => navigate("/announcements")}
              className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
