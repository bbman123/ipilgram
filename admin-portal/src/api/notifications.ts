import apiClient from "./client";

export type NotificationType =
  | "flight_reminder"
  | "accommodation_checkin"
  | "accommodation_checkout"
  | "transport_reminder"
  | "return_flight"
  | "emergency"
  | "broadcast"
  | "announcement";

export type NotificationStatus = "pending" | "scheduled" | "sent" | "failed" | "read";

export interface Notification {
  id: number;
  pilgrim_id: number;
  title: string;
  message: string;
  notification_type: NotificationType;
  status: NotificationStatus;
  scheduled_time: string | null;
  sent_at: string | null;
  read_at: string | null;
  delivery_mode: string | null;
  language: string | null;
  audio_url: string | null;
  source_type: string | null;
  source_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedNotifications {
  items: Notification[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export async function listNotifications(
  page = 1,
  size = 20,
  type?: string,
  status?: string,
): Promise<PaginatedNotifications> {
  const params: Record<string, string | number> = { page, size };
  if (type) params.type = type;
  if (status) params.status = status;
  const { data } = await apiClient.get<PaginatedNotifications>("/notifications", { params });
  return data;
}

export async function getMyNotifications(): Promise<Notification[]> {
  const { data } = await apiClient.get<Notification[]>("/notifications/my");
  return data;
}

export async function markNotificationRead(id: number): Promise<Notification> {
  const { data } = await apiClient.patch<Notification>(`/notifications/${id}/read`);
  return data;
}
