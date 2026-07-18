import apiClient from "./client";

export type TargetType = "all" | "pilgrim" | "package" | "flight" | "accommodation" | "transport";
export type AnnouncementPriority = "low" | "medium" | "high" | "urgent";

export interface Announcement {
  id: number;
  title: string;
  message: string;
  priority: AnnouncementPriority;
  target_type: TargetType;
  target_id: number | null;
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
  priority?: AnnouncementPriority;
  target_type: TargetType;
  target_id?: number | null;
  publish_date: string;
  expiry_date: string;
}

export interface AnnouncementUpdateData {
  title?: string;
  message?: string;
  priority?: AnnouncementPriority;
  target_type?: TargetType;
  target_id?: number | null;
  publish_date?: string;
  expiry_date?: string;
}

export async function listAnnouncements(
  page = 1,
  size = 20,
  search = "",
  priority?: string,
  targetType?: string,
): Promise<PaginatedAnnouncements> {
  const params: Record<string, string | number> = { page, size };
  if (search) params.search = search;
  if (priority) params.priority = priority;
  if (targetType) params.target_type = targetType;
  const { data } = await apiClient.get<PaginatedAnnouncements>("/announcements", { params });
  return data;
}

export async function getActiveAnnouncements(): Promise<Announcement[]> {
  const { data } = await apiClient.get<Announcement[]>("/announcements/active");
  return data;
}

export async function getMyAnnouncements(): Promise<Announcement[]> {
  const { data } = await apiClient.get<Announcement[]>("/announcements/my");
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
