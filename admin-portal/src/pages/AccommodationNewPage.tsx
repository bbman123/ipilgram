import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createAccommodation } from "../api/accommodations";
import { listPilgrims, type Pilgrim } from "../api/pilgrims";

export default function AccommodationNewPage() {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [pilgrims, setPilgrims] = useState<Pilgrim[]>([]);

  const [pilgrimId, setPilgrimId] = useState("");
  const [hotelName, setHotelName] = useState("");
  const [city, setCity] = useState("");
  const [building, setBuilding] = useState("");
  const [floor, setFloor] = useState("");
  const [roomNumber, setRoomNumber] = useState("");
  const [bedNumber, setBedNumber] = useState("");
  const [address, setAddress] = useState("");
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");

  useEffect(() => {
    listPilgrims(1, 100).then((d) => setPilgrims(d.items)).catch(() => {});
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const acc = await createAccommodation({
        pilgrim_id: Number(pilgrimId),
        hotel_name: hotelName,
        city,
        building: building || undefined,
        floor: floor || undefined,
        room_number: roomNumber,
        bed_number: bedNumber || undefined,
        address: address || undefined,
        check_in: checkIn,
        check_out: checkOut,
      });
      navigate(`/accommodations/${acc.id}`);
    } catch {
      setError("Failed to create accommodation. Check all fields.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Add Accommodation</h1>
        <p className="text-gray-500 text-sm mt-1">Assign hotel lodging to a pilgrim</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        {error && (
          <div className="bg-red-50 text-red-700 text-sm px-4 py-3 rounded-lg border border-red-200">{error}</div>
        )}

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

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Hotel Name *</label>
            <input type="text" value={hotelName} onChange={(e) => setHotelName(e.target.value)} required
              placeholder="e.g. Madinah Hilton"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">City *</label>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} required
              placeholder="e.g. Madinah"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Building</label>
            <input type="text" value={building} onChange={(e) => setBuilding(e.target.value)}
              placeholder="e.g. Tower A"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Floor</label>
            <input type="text" value={floor} onChange={(e) => setFloor(e.target.value)}
              placeholder="e.g. 3"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Room Number *</label>
            <input type="text" value={roomNumber} onChange={(e) => setRoomNumber(e.target.value)} required
              placeholder="e.g. 301"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bed Number</label>
            <input type="text" value={bedNumber} onChange={(e) => setBedNumber(e.target.value)}
              placeholder="e.g. B2"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Check-in *</label>
            <input type="datetime-local" value={checkIn} onChange={(e) => setCheckIn(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Check-out *</label>
            <input type="datetime-local" value={checkOut} onChange={(e) => setCheckOut(e.target.value)} required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
          <input type="text" value={address} onChange={(e) => setAddress(e.target.value)}
            placeholder="Full hotel address"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button type="submit" disabled={saving}
            className="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 transition-colors">
            {saving ? "Creating..." : "Create Accommodation"}
          </button>
          <button type="button" onClick={() => navigate("/accommodations")}
            className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
