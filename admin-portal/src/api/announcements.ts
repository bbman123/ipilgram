import apiClient from "./client";

export type AnnouncementCategory = "emergency" | "general" | "flight" | "accommodation" | "transport";
export type AnnouncementPriority = "low" | "medium" | "high" | "urgent";

export interface Announcement {
  id: number;
  title: string;
  message: string;
  category: AnnouncementCategory;
  language: string;
  priority: AnnouncementPriority;
  publish_date: string;
  expiry_date: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedAnnouncements {
  items: Announcement[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface AnnouncementCreateData {
  title: string;
  message: string;
  category: AnnouncementCategory;
  language?: string;
  priority?: AnnouncementPriority;
  publish_date: string;
  expiry_date: string;
}

export interface AnnouncementUpdateData {
  title?: string;
  message?: string;
  category?: AnnouncementCategory;
  language?: string;
  priority?: AnnouncementPriority;
  publish_date?: string;
  expiry_date?: string;
}

export async function listAnnouncements(
  page = 1,
  size = 20,
  search = "",
  category?: string,
  priority?: string,
  language?: string
): Promise<PaginatedAnnouncements> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (category) params.category = category;
  if (priority) params.priority = priority;
  if (language) params.language = language;
  const { data } = await apiClient.get<PaginatedAnnouncements>("/announcements", { params });
  return data;
}

export async function getAnnouncement(id: number): Promise<Announcement> {
  const { data } = await apiClient.get<Announcement>(`/announcements/${id}`);
  return data;
}

export async function createAnnouncement(body: AnnouncementCreateData): Promise<Announcement> {
  const { data } = await apiClient.post<Announcement>("/announcements", body);
  return data;
}

export async function updateAnnouncement(id: number, body: AnnouncementUpdateData): Promise<Announcement> {
  const { data } = await apiClient.put<Announcement>(`/announcements/${id}`, body);
  return data;
}

export async function deleteAnnouncement(id: number): Promise<void> {
  await apiClient.delete(`/announcements/${id}`);
}
