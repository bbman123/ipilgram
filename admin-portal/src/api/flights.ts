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

export interface PaginatedFlights {
  items: Flight[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface FlightCreateData {
  airline: string;
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_datetime: string;
  arrival_datetime: string;
  gate?: string;
  seat_number?: string;
  status?: FlightStatus;
}

export interface FlightUpdateData {
  airline?: string;
  flight_number?: string;
  departure_airport?: string;
  arrival_airport?: string;
  departure_datetime?: string;
  arrival_datetime?: string;
  gate?: string;
  seat_number?: string;
  status?: FlightStatus;
}

export async function listFlights(
  page = 1,
  size = 20,
  search = "",
  status?: string,
): Promise<PaginatedFlights> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (status) params.status = status;
  const { data } = await apiClient.get<PaginatedFlights>("/flights", { params });
  return data;
}

export async function getFlight(id: number): Promise<Flight> {
  const { data } = await apiClient.get<Flight>(`/flights/${id}`);
  return data;
}

export async function createFlight(body: FlightCreateData): Promise<Flight> {
  const { data } = await apiClient.post<Flight>("/flights", body);
  return data;
}

export async function updateFlight(id: number, body: FlightUpdateData): Promise<Flight> {
  const { data } = await apiClient.put<Flight>(`/flights/${id}`, body);
  return data;
}

export async function deleteFlight(id: number): Promise<void> {
  await apiClient.delete(`/flights/${id}`);
}
