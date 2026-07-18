import apiClient from "./client";

export type FlightStatus =
  | "scheduled"
  | "confirmed"
  | "boarding"
  | "departed"
  | "in_air"
  | "landed"
  | "cancelled"
  | "delayed";

export type TransportType = "bus" | "van" | "taxi" | "car" | "other";

export interface Flight {
  id: number;
  airline: string;
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_datetime: string;
  arrival_datetime: string;
  gate: string | null;
  seat_number: string | null;
  status: FlightStatus;
  created_at: string;
  updated_at: string;
}

export interface Accommodation {
  id: number;
  hotel_name: string;
  city: string;
  building: string | null;
  floor: string | null;
  room_number: string;
  bed_number: string | null;
  address: string | null;
  check_in: string;
  check_out: string;
  created_at: string;
  updated_at: string;
}

export interface Transport {
  id: number;
  bus_number: string;
  pickup_location: string;
  destination: string;
  pickup_time: string;
  driver_name: string;
  driver_phone: string;
  transport_type: TransportType;
  created_at: string;
  updated_at: string;
}

export interface Package {
  id: number;
  name: string;
  description: string | null;
  flight_id: number | null;
  accommodation_id: number | null;
  transport_id: number | null;
  created_at: string;
  updated_at: string;
  pilgrim_count: number;
}

export interface PackageDetail {
  id: number;
  name: string;
  description: string | null;
  flight: Flight | null;
  accommodation: Accommodation | null;
  transport: Transport | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedPackages {
  items: Package[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PackageCreateData {
  name: string;
  description?: string;
  flight_id?: number | null;
  accommodation_id?: number | null;
  transport_id?: number | null;
}

export interface PackageUpdateData {
  name?: string;
  description?: string;
  flight_id?: number | null;
  accommodation_id?: number | null;
  transport_id?: number | null;
}

export async function listPackages(
  page = 1,
  size = 20,
  search = ""
): Promise<PaginatedPackages> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  const { data } = await apiClient.get<PaginatedPackages>("/packages", { params });
  return data;
}

export async function getPackage(id: number): Promise<PackageDetail> {
  const { data } = await apiClient.get<PackageDetail>(`/packages/${id}`);
  return data;
}

export async function createPackage(body: PackageCreateData): Promise<Package> {
  const { data } = await apiClient.post<Package>("/packages", body);
  return data;
}

export async function updatePackage(id: number, body: PackageUpdateData): Promise<Package> {
  const { data } = await apiClient.put<Package>(`/packages/${id}`, body);
  return data;
}

export async function deletePackage(id: number): Promise<void> {
  await apiClient.delete(`/packages/${id}`);
}

export async function assignPackage(packageId: number, pilgrimId: number): Promise<void> {
  await apiClient.post(`/packages/${packageId}/assign/${pilgrimId}`);
}
