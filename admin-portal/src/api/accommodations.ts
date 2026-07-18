import apiClient from "./client";

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

export interface PaginatedAccommodations {
  items: Accommodation[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface AccommodationCreateData {
  hotel_name: string;
  city: string;
  building?: string;
  floor?: string;
  room_number: string;
  bed_number?: string;
  address?: string;
  check_in: string;
  check_out: string;
}

export interface AccommodationUpdateData {
  hotel_name?: string;
  city?: string;
  building?: string;
  floor?: string;
  room_number?: string;
  bed_number?: string;
  address?: string;
  check_in?: string;
  check_out?: string;
}

export async function listAccommodations(
  page = 1,
  size = 20,
  search = "",
  city?: string
): Promise<PaginatedAccommodations> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (city) params.city = city;
  const { data } = await apiClient.get<PaginatedAccommodations>("/accommodations", { params });
  return data;
}

export async function getAccommodation(id: number): Promise<Accommodation> {
  const { data } = await apiClient.get<Accommodation>(`/accommodations/${id}`);
  return data;
}

export async function createAccommodation(body: AccommodationCreateData): Promise<Accommodation> {
  const { data } = await apiClient.post<Accommodation>("/accommodations", body);
  return data;
}

export async function updateAccommodation(id: number, body: AccommodationUpdateData): Promise<Accommodation> {
  const { data } = await apiClient.put<Accommodation>(`/accommodations/${id}`, body);
  return data;
}

export async function deleteAccommodation(id: number): Promise<void> {
  await apiClient.delete(`/accommodations/${id}`);
}
