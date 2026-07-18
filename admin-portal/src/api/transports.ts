import apiClient from "./client";

export type TransportType = "bus" | "van" | "taxi" | "car" | "other";

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

export interface PaginatedTransports {
  items: Transport[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface TransportCreateData {
  bus_number: string;
  pickup_location: string;
  destination: string;
  pickup_time: string;
  driver_name: string;
  driver_phone: string;
  transport_type: TransportType;
}

export interface TransportUpdateData {
  bus_number?: string;
  pickup_location?: string;
  destination?: string;
  pickup_time?: string;
  driver_name?: string;
  driver_phone?: string;
  transport_type?: TransportType;
}

export async function listTransports(
  page = 1,
  size = 20,
  search = "",
  type?: string,
): Promise<PaginatedTransports> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (type) params.type = type;
  const { data } = await apiClient.get<PaginatedTransports>("/transports", { params });
  return data;
}

export async function getTransport(id: number): Promise<Transport> {
  const { data } = await apiClient.get<Transport>(`/transports/${id}`);
  return data;
}

export async function createTransport(body: TransportCreateData): Promise<Transport> {
  const { data } = await apiClient.post<Transport>("/transports", body);
  return data;
}

export async function updateTransport(id: number, body: TransportUpdateData): Promise<Transport> {
  const { data } = await apiClient.put<Transport>(`/transports/${id}`, body);
  return data;
}

export async function deleteTransport(id: number): Promise<void> {
  await apiClient.delete(`/transports/${id}`);
}
