import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createPackage, type PackageCreateData } from "../api/packages";
import { listFlights, type Flight } from "../api/flights";
import { listAccommodations, type Accommodation } from "../api/accommodations";
import { listTransports, type Transport } from "../api/transports";

export default function PackageNewPage() {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [flightId, setFlightId] = useState("");
  const [accommodationId, setAccommodationId] = useState("");
  const [transportId, setTransportId] = useState("");

  const [flights, setFlights] = useState<Flight[]>([]);
  const [accommodations, setAccommodations] = useState<Accommodation[]>([]);
  const [transports, setTransports] = useState<Transport[]>([]);

  useEffect(() => {
    Promise.all([
      listFlights(1, 100).then((d) => setFlights(d.items)),
      listAccommodations(1, 100).then((d) => setAccommodations(d.items)),
      listTransports(1, 100).then((d) => setTransports(d.items)),
    ]).catch(() => {});
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const body: PackageCreateData = {
        name,
        description: description || undefined,
        flight_id: flightId ? Number(flightId) : null,
        accommodation_id: accommodationId ? Number(accommodationId) : null,
        transport_id: transportId ? Number(transportId) : null,
      };
      const pkg = await createPackage(body);
      navigate(`/packages/${pkg.id}`);
    } catch {
      setError("Failed to create package. Check all fields.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Create Package</h1>
        <p className="text-gray-500 text-sm mt-1">Create a new Hajj package</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Package Name *</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required
            placeholder="e.g. Premium Hajj 2026"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3}
            placeholder="Package description..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Flight</label>
            <select value={flightId} onChange={(e) => setFlightId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">No flight</option>
              {flights.map((f) => (
                <option key={f.id} value={f.id}>{f.flight_number} ({f.airline})</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Accommodation</label>
            <select value={accommodationId} onChange={(e) => setAccommodationId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">No accommodation</option>
              {accommodations.map((a) => (
                <option key={a.id} value={a.id}>{a.hotel_name} (Room {a.room_number})</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Transport</label>
            <select value={transportId} onChange={(e) => setTransportId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="">No transport</option>
              {transports.map((t) => (
                <option key={t.id} value={t.id}>{t.bus_number} ({t.driver_name})</option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={saving}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            {saving ? "Creating..." : "Create Package"}
          </button>
          <button type="button" onClick={() => navigate("/packages")}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
