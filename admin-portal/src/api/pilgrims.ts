import apiClient from "./client";

export interface Pilgrim {
  id: number;
  email: string;
  full_name: string;
  role: "pilgrim";
  is_active: boolean;
  phone: string | null;
  nationality: string | null;
  passport_number: string | null;
  emergency_contact: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedPilgrims {
  items: Pilgrim[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PilgrimCreateData {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  nationality?: string;
  passport_number?: string;
  emergency_contact?: string;
}

export interface PilgrimUpdateData {
  email?: string;
  full_name?: string;
  phone?: string;
  nationality?: string;
  passport_number?: string;
  emergency_contact?: string;
  is_active?: boolean;
}

export async function listPilgrims(
  page = 1,
  size = 20,
  search = ""
): Promise<PaginatedPilgrims> {
  const { data } = await apiClient.get<PaginatedPilgrims>("/pilgrims", {
    params: { page, size, search },
  });
  return data;
}

export async function getPilgrim(id: number): Promise<Pilgrim> {
  const { data } = await apiClient.get<Pilgrim>(`/pilgrims/${id}`);
  return data;
}

export async function createPilgrim(body: PilgrimCreateData): Promise<Pilgrim> {
  const { data } = await apiClient.post<Pilgrim>("/pilgrims", body);
  return data;
}

export async function updatePilgrim(
  id: number,
  body: PilgrimUpdateData
): Promise<Pilgrim> {
  const { data } = await apiClient.put<Pilgrim>(`/pilgrims/${id}`, body);
  return data;
}

export async function deletePilgrim(id: number): Promise<void> {
  await apiClient.delete(`/pilgrims/${id}`);
}
