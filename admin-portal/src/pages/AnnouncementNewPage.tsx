import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createAnnouncement, type TargetType } from "../api/announcements";
import { listFlights } from "../api/flights";
import { listAccommodations } from "../api/accommodations";
import { listTransports } from "../api/transports";
import { listPackages } from "../api/packages";
import { listPilgrims } from "../api/pilgrims";

interface EntityOption { id: number; label: string; }

const targetTypeOptions: { value: TargetType; label: string; color: string }[] = [
  { value: "all", label: "All Pilgrims", color: "bg-indigo-100 text-indigo-700" },
  { value: "pilgrim", label: "Individual Pilgrim", color: "bg-emerald-100 text-emerald-700" },
  { value: "package", label: "Package", color: "bg-amber-100 text-amber-700" },
  { value: "flight", label: "Flight", color: "bg-blue-100 text-blue-700" },
  { value: "accommodation", label: "Accommodation", color: "bg-teal-100 text-teal-700" },
  { value: "transport", label: "Transport", color: "bg-orange-100 text-orange-700" },
];

const priorityOptions = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
  { value: "urgent", label: "Urgent" },
];

const placeholderOptions = [
  { tag: "{{pilgrim_name}}", desc: "Pilgrim's full name" },
  { tag: "{{package_name}}", desc: "Package name" },
  { tag: "{{flight_number}}", desc: "Flight number" },
  { tag: "{{airline}}", desc: "Airline name" },
  { tag: "{{departure_airport}}", desc: "Departure airport" },
  { tag: "{{arrival_airport}}", desc: "Arrival airport" },
  { tag: "{{departure_time}}", desc: "Departure time" },
  { tag: "{{arrival_time}}", desc: "Arrival time" },
  { tag: "{{gate}}", desc: "Gate number" },
  { tag: "{{seat}}", desc: "Seat number" },
  { tag: "{{hotel_name}}", desc: "Hotel name" },
  { tag: "{{city}}", desc: "City" },
  { tag: "{{room_number}}", desc: "Room number" },
  { tag: "{{check_in_time}}", desc: "Check-in time" },
  { tag: "{{check_out_time}}", desc: "Check-out time" },
  { tag: "{{pickup_location}}", desc: "Pickup location" },
  { tag: "{{destination}}", desc: "Destination" },
  { tag: "{{pickup_time}}", desc: "Pickup time" },
  { tag: "{{driver_name}}", desc: "Driver name" },
  { tag: "{{driver_phone}}", desc: "Driver phone" },
];

export default function AnnouncementNewPage() {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [showPreview, setShowPreview] = useState(false);

  const [title, setTitle] = useState("");
  const [messageTemplate, setMessageTemplate] = useState("");
  const [priority, setPriority] = useState("medium");
  const [targetType, setTargetType] = useState<TargetType>("all");
  const [targetId, setTargetId] = useState<number | "">("");
  const [publishDate, setPublishDate] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [includePackage, setIncludePackage] = useState(false);
  const [includeFlight, setIncludeFlight] = useState(false);
  const [includeTransport, setIncludeTransport] = useState(false);
  const [includeAccommodation, setIncludeAccommodation] = useState(false);
  const [sendAsNotification, setSendAsNotification] = useState(false);

  const [entityOptions, setEntityOptions] = useState<EntityOption[]>([]);
  const [loadingEntities, setLoadingEntities] = useState(false);

  useEffect(() => {
    if (targetType === "all") {
      setTargetId("");
      setEntityOptions([]);
      return;
    }
    setLoadingEntities(true);
    const loaders: Record<string, () => Promise<EntityOption[]>> = {
      pilgrim: async () => {
        const d = await listPilgrims(1, 500);
        return d.items.map((p) => ({ id: p.id, label: `${p.full_name} (${p.email})` }));
      },
      package: async () => {
        const d = await listPackages(1, 500);
        return d.items.map((p) => ({ id: p.id, label: p.name }));
      },
      flight: async () => {
        const d = await listFlights(1, 500);
        return d.items.map((f) => ({ id: f.id, label: `${f.flight_number} — ${f.airline}` }));
      },
      accommodation: async () => {
        const d = await listAccommodations(1, 500);
        return d.items.map((a) => ({ id: a.id, label: `${a.hotel_name} — Rm ${a.room_number}, ${a.city}` }));
      },
      transport: async () => {
        const d = await listTransports(1, 500);
        return d.items.map((t) => ({ id: t.id, label: `${t.bus_number} — ${t.pickup_location} to ${t.destination}` }));
      },
    };
    loaders[targetType]()
      .then(setEntityOptions)
      .catch(() => setEntityOptions([]))
      .finally(() => setLoadingEntities(false));
  }, [targetType]);

  function insertPlaceholder(tag: string) {
    setMessageTemplate((prev) => prev + (prev && !prev.endsWith(" ") ? " " : "") + tag);
  }

  function renderPreviewMessage(): string {
    let msg = messageTemplate;
    const sample: Record<string, string> = {
      pilgrim_name: "Ahmed Mohammed",
      package_name: "Premium Hajj 2026",
      flight_number: "NA-101",
      airline: "Air Nigeria",
      departure_airport: "Abuja (ABV)",
      arrival_airport: "Jeddah (JED)",
      departure_time: "08:00 AM",
      arrival_time: "04:00 PM",
      gate: "B12",
      seat: "14A",
      hotel_name: "Hilton Makkah",
      city: "Makkah",
      room_number: "705",
      check_in_time: "02:00 PM",
      check_out_time: "11:00 AM",
      pickup_location: "Airport Terminal",
      destination: "Hilton Makkah",
      pickup_time: "05:00 PM",
      driver_name: "Ibrahim",
      driver_phone: "+966501234567",
    };
    for (const [key, val] of Object.entries(sample)) {
      msg = msg.replace(new RegExp(`\\{\\{${key}\\}\\}`, "g"), val);
    }
    return msg;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const a = await createAnnouncement({
        title,
        message_template: messageTemplate,
        priority: priority as any,
        target_type: targetType,
        target_id: targetType === "all" ? null : (targetId as number),
        publish_date: publishDate,
        expiry_date: expiryDate,
        include_package_details: includePackage,
        include_flight_details: includeFlight,
        include_transport_details: includeTransport,
        include_accommodation_details: includeAccommodation,
        send_as_notification: sendAsNotification,
      });
      navigate(`/announcements/${a.id}`);
    } catch {
      setError("Failed to create announcement. Check all fields.");
    } finally {
      setSaving(false);
    }
  }

  const targetInfo = targetTypeOptions.find((t) => t.value === targetType);
  const selectedEntity = entityOptions.find((e) => e.id === targetId);

  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">New Announcement</h1>
          <p className="text-gray-500 text-sm mt-1">Create an announcement template with placeholders</p>
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
            <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${targetInfo?.color}`}>{targetInfo?.label}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${
              priority === "urgent" ? "bg-red-100 text-red-700" :
              priority === "high" ? "bg-amber-100 text-amber-700" :
              priority === "medium" ? "bg-blue-100 text-blue-600" :
              "bg-gray-100 text-gray-600"
            }`}>{priority}</span>
          </div>
          {targetType !== "all" && selectedEntity && (
            <p className="text-xs text-gray-500 mb-2">Target: {selectedEntity.label}</p>
          )}
          <h2 className="text-xl font-bold text-gray-900 mb-3">{title || "Untitled"}</h2>
          <div className="text-sm text-gray-700 whitespace-pre-wrap mb-4 bg-gray-50 p-4 rounded-lg border border-gray-100">
            <div className="text-xs text-gray-400 mb-2 uppercase tracking-wide">Preview (sample data)</div>
            {renderPreviewMessage() || "No message content."}
          </div>
          <div className="flex flex-wrap gap-2 text-xs text-gray-500 border-t border-gray-200 pt-3">
            {includePackage && <span className="bg-amber-50 text-amber-700 px-2 py-0.5 rounded">Package Details</span>}
            {includeFlight && <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded">Flight Details</span>}
            {includeTransport && <span className="bg-orange-50 text-orange-700 px-2 py-0.5 rounded">Transport Details</span>}
            {includeAccommodation && <span className="bg-teal-50 text-teal-700 px-2 py-0.5 rounded">Accommodation Details</span>}
            {sendAsNotification && <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded">Send as Push Notification</span>}
          </div>
          <div className="flex gap-4 text-xs text-gray-500 border-t border-gray-200 pt-3 mt-3">
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Message Template *</label>
            <textarea value={messageTemplate} onChange={(e) => setMessageTemplate(e.target.value)} required rows={5}
              placeholder="Hello {{pilgrim_name}}, your flight {{flight_number}} departs from {{departure_airport}} at {{departure_time}}."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 font-mono" />
            <div className="mt-2">
              <div className="text-xs font-medium text-gray-500 mb-1">Insert Placeholder:</div>
              <div className="flex flex-wrap gap-1">
                {placeholderOptions.map((p) => (
                  <button key={p.tag} type="button" onClick={() => insertPlaceholder(p.tag)}
                    title={p.desc}
                    className="px-2 py-0.5 text-xs bg-gray-100 hover:bg-emerald-100 text-gray-600 hover:text-emerald-700 rounded border border-gray-200 hover:border-emerald-300 transition-colors">
                    {p.tag}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Priority *</label>
              <select value={priority} onChange={(e) => setPriority(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                {priorityOptions.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Target Audience *</label>
              <select value={targetType} onChange={(e) => setTargetType(e.target.value as TargetType)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                {targetTypeOptions.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>
            {targetType !== "all" && (
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target {targetType.charAt(0).toUpperCase() + targetType.slice(1)} *
                </label>
                {loadingEntities ? (
                  <div className="text-sm text-gray-500 py-2">Loading entities...</div>
                ) : (
                  <select value={targetId} onChange={(e) => setTargetId(Number(e.target.value))}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="">Select {targetType}...</option>
                    {entityOptions.map((e) => (
                      <option key={e.id} value={e.id}>{e.label}</option>
                    ))}
                  </select>
                )}
              </div>
            )}
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

          <div className="border-t border-gray-200 pt-4">
            <div className="text-sm font-medium text-gray-700 mb-2">Include Details</div>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: "Package Details", checked: includePackage, onChange: setIncludePackage },
                { label: "Flight Details", checked: includeFlight, onChange: setIncludeFlight },
                { label: "Transport Details", checked: includeTransport, onChange: setIncludeTransport },
                { label: "Accommodation Details", checked: includeAccommodation, onChange: setIncludeAccommodation },
              ].map((opt) => (
                <label key={opt.label} className="flex items-center gap-2 text-sm text-gray-600">
                  <input type="checkbox" checked={opt.checked} onChange={(e) => opt.onChange(e.target.checked)}
                    className="rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
                  {opt.label}
                </label>
              ))}
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <label className="flex items-center gap-2 text-sm text-gray-600">
              <input type="checkbox" checked={sendAsNotification} onChange={(e) => setSendAsNotification(e.target.checked)}
                className="rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" />
              Send as push notification to targeted pilgrims
            </label>
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
