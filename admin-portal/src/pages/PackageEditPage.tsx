import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getPackage, updatePackage, type PackageDetail, type PackageUpdateData } from "../api/packages";
import { listFlights, type Flight } from "../api/flights";
import { listAccommodations, type Accommodation } from "../api/accommodations";
import { listTransports, type Transport } from "../api/transports";

export default function PackageEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [pkg, setPkg] = useState<PackageDetail | null>(null);

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
      id ? getPackage(Number(id)) : Promise.reject(),
      listFlights(1, 100).then((d) => setFlights(d.items)),
      listAccommodations(1, 100).then((d) => setAccommodations(d.items)),
      listTransports(1, 100).then((d) => setTransports(d.items)),
    ])
      .then(([p]) => {
        setPkg(p);
        setName(p.name);
        setDescription(p.description || "");
        setFlightId(p.flight?.id ? String(p.flight.id) : "");
        setAccommodationId(p.accommodation?.id ? String(p.accommodation.id) : "");
        setTransportId(p.transport?.id ? String(p.transport.id) : "");
      })
      .catch(() => setError("Failed to load package"))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    setError("");
    setSaving(true);
    try {
      const body: PackageUpdateData = {
        name,
        description: description || undefined,
        flight_id: flightId ? Number(flightId) : null,
        accommodation_id: accommodationId ? Number(accommodationId) : null,
        transport_id: transportId ? Number(transportId) : null,
      };
      await updatePackage(Number(id), body);
      navigate(`/packages/${id}`);
    } catch {
      setError("Failed to update package");
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

  if (!pkg) {
    return <div className="text-center py-20 text-gray-500">Package not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Edit Package</h1>
        <p className="text-gray-500 text-sm mt-1">{pkg.name}</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Package Name *</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3}
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
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <button type="button" onClick={() => navigate(`/packages/${id}`)}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
