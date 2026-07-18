import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getTransport, updateTransport, type Transport } from "../api/transports";

export default function TransportEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [transport, setTransport] = useState<Transport | null>(null);

  const [busNumber, setBusNumber] = useState("");
  const [pickupLocation, setPickupLocation] = useState("");
  const [destination, setDestination] = useState("");
  const [pickupTime, setPickupTime] = useState("");
  const [driverName, setDriverName] = useState("");
  const [driverPhone, setDriverPhone] = useState("");
  const [transportType, setTransportType] = useState("");

  useEffect(() => {
    if (!id) return;
    getTransport(Number(id))
      .then((t) => {
        setTransport(t);
        setBusNumber(t.bus_number);
        setPickupLocation(t.pickup_location);
        setDestination(t.destination);
        setPickupTime(t.pickup_time.slice(0, 16));
        setDriverName(t.driver_name);
        setDriverPhone(t.driver_phone);
        setTransportType(t.transport_type);
      })
      .catch(() => setError("Failed to load transport"))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    setError("");
    setSaving(true);
    try {
      await updateTransport(Number(id), {
        bus_number: busNumber,
        pickup_location: pickupLocation,
        destination,
        pickup_time: pickupTime,
        driver_name: driverName,
        driver_phone: driverPhone,
        transport_type: transportType as Transport["transport_type"],
      });
      navigate(`/transports/${id}`);
    } catch {
      setError("Failed to update transport");
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

  if (!transport) {
    return <div className="text-center py-20 text-gray-500">Transport not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Edit Transport</h1>
        <p className="text-gray-500 text-sm mt-1">{transport.bus_number} — {transport.driver_name}</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bus/Vehicle Number *</label>
            <input type="text" value={busNumber} onChange={(e) => setBusNumber(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Transport Type *</label>
            <select value={transportType} onChange={(e) => setTransportType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="bus">Bus</option>
              <option value="van">Van</option>
              <option value="taxi">Taxi</option>
              <option value="car">Car</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Pickup Location *</label>
            <input type="text" value={pickupLocation} onChange={(e) => setPickupLocation(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Destination *</label>
            <input type="text" value={destination} onChange={(e) => setDestination(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Pickup Time *</label>
            <input type="datetime-local" value={pickupTime} onChange={(e) => setPickupTime(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Driver Name *</label>
            <input type="text" value={driverName} onChange={(e) => setDriverName(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Driver Phone *</label>
            <input type="text" value={driverPhone} onChange={(e) => setDriverPhone(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={saving}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <button type="button" onClick={() => navigate(`/transports/${id}`)}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
