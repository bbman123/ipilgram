import apiClient from "./client";

export type PreferredLanguage = "English" | "Hausa" | "Yoruba" | "Igbo" | "Arabic";
export type DeliveryMode = "Text" | "Audio" | "Text + Audio";

export interface Preference {
  id: number;
  pilgrim_id: number;
  preferred_language: PreferredLanguage;
  delivery_mode: DeliveryMode;
  font_size: number;
  notifications_enabled: boolean;
  created_at: string;
  updated_at: string;
  pilgrim_name: string | null;
  pilgrim_email: string | null;
}

export interface PaginatedPreferences {
  items: Preference[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PreferenceCreateData {
  pilgrim_id: number;
  preferred_language?: PreferredLanguage;
  delivery_mode?: DeliveryMode;
  font_size?: number;
  notifications_enabled?: boolean;
}

export interface PreferenceUpdateData {
  preferred_language?: PreferredLanguage;
  delivery_mode?: DeliveryMode;
  font_size?: number;
  notifications_enabled?: boolean;
}

export async function listPreferences(
  page = 1,
  size = 20,
  search = "",
  language?: string,
  deliveryMode?: string
): Promise<PaginatedPreferences> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (language) params.language = language;
  if (deliveryMode) params.delivery_mode = deliveryMode;
  const { data } = await apiClient.get<PaginatedPreferences>("/preferences", { params });
  return data;
}

export async function getPreference(id: number): Promise<Preference> {
  const { data } = await apiClient.get<Preference>(`/preferences/${id}`);
  return data;
}

export async function getPreferenceByPilgrim(pilgrimId: number): Promise<Preference> {
  const { data } = await apiClient.get<Preference>(`/preferences/by-pilgrim/${pilgrimId}`);
  return data;
}

export async function createPreference(body: PreferenceCreateData): Promise<Preference> {
  const { data } = await apiClient.post<Preference>("/preferences", body);
  return data;
}

export async function updatePreference(id: number, body: PreferenceUpdateData): Promise<Preference> {
  const { data } = await apiClient.put<Preference>(`/preferences/${id}`, body);
  return data;
}

export async function deletePreference(id: number): Promise<void> {
  await apiClient.delete(`/preferences/${id}`);
}
