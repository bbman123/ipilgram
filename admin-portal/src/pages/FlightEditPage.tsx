import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getFlight, updateFlight, type Flight } from "../api/flights";

export default function FlightEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [flight, setFlight] = useState<Flight | null>(null);

  const [airline, setAirline] = useState("");
  const [flightNumber, setFlightNumber] = useState("");
  const [departureAirport, setDepartureAirport] = useState("");
  const [arrivalAirport, setArrivalAirport] = useState("");
  const [departureDatetime, setDepartureDatetime] = useState("");
  const [arrivalDatetime, setArrivalDatetime] = useState("");
  const [gate, setGate] = useState("");
  const [seatNumber, setSeatNumber] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (!id) return;
    getFlight(Number(id))
      .then((f) => {
        setFlight(f);
        setAirline(f.airline);
        setFlightNumber(f.flight_number);
        setDepartureAirport(f.departure_airport);
        setArrivalAirport(f.arrival_airport);
        setDepartureDatetime(f.departure_datetime.slice(0, 16));
        setArrivalDatetime(f.arrival_datetime.slice(0, 16));
        setGate(f.gate || "");
        setSeatNumber(f.seat_number || "");
        setStatus(f.status);
      })
      .catch(() => setError("Failed to load flight"))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    setError("");
    setSaving(true);
    try {
      await updateFlight(Number(id), {
        airline,
        flight_number: flightNumber,
        departure_airport: departureAirport,
        arrival_airport: arrivalAirport,
        departure_datetime: departureDatetime,
        arrival_datetime: arrivalDatetime,
        gate: gate || undefined,
        seat_number: seatNumber || undefined,
        status: status as Flight["status"],
      });
      navigate(`/flights/${id}`);
    } catch {
      setError("Failed to update flight");
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

  if (!flight) {
    return <div className="text-center py-20 text-gray-500">Flight not found.</div>;
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Edit Flight</h1>
        <p className="text-gray-500 text-sm mt-1">{flight.flight_number} — {flight.airline}</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Airline *</label>
            <input type="text" value={airline} onChange={(e) => setAirline(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Flight Number *</label>
            <input type="text" value={flightNumber} onChange={(e) => setFlightNumber(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Departure Airport *</label>
            <input type="text" value={departureAirport} onChange={(e) => setDepartureAirport(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Arrival Airport *</label>
            <input type="text" value={arrivalAirport} onChange={(e) => setArrivalAirport(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Departure *</label>
            <input type="datetime-local" value={departureDatetime} onChange={(e) => setDepartureDatetime(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Arrival *</label>
            <input type="datetime-local" value={arrivalDatetime} onChange={(e) => setArrivalDatetime(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Gate</label>
            <input type="text" value={gate} onChange={(e) => setGate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Seat Number</label>
            <input type="text" value={seatNumber} onChange={(e) => setSeatNumber(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select value={status} onChange={(e) => setStatus(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="scheduled">Scheduled</option>
              <option value="confirmed">Confirmed</option>
              <option value="boarding">Boarding</option>
              <option value="departed">Departed</option>
              <option value="in_air">In Air</option>
              <option value="landed">Landed</option>
              <option value="cancelled">Cancelled</option>
              <option value="delayed">Delayed</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={saving}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <button type="button" onClick={() => navigate(`/flights/${id}`)}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
