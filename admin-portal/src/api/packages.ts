import apiClient from "./client";
import type { Flight } from "./flights";
import type { Accommodation } from "./accommodations";
import type { Transport } from "./transports";
import type { PaginatedPilgrims } from "./pilgrims";

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

export async function assignPackage(packageId: number, pilgrimId: number): Promise<Package> {
  const { data } = await apiClient.post<Package>(`/packages/${packageId}/assign/${pilgrimId}`);
  return data;
}

export async function getPackagePilgrims(
  packageId: number,
  page = 1,
  size = 20,
  search = ""
): Promise<PaginatedPilgrims> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  const { data } = await apiClient.get<PaginatedPilgrims>(`/packages/${packageId}/pilgrims`, { params });
  return data;
}
