import 'package:freezed_annotation/freezed_annotation.dart';

part 'app_notification.freezed.dart';
part 'app_notification.g.dart';

@freezed
class AppNotification with _$AppNotification {
  const factory AppNotification({
    required int id,
    @JsonKey(name: 'pilgrim_id') required int pilgrimId,
    required String title,
    required String message,
    @JsonKey(name: 'notification_type') required String notificationType,
    required String status,
    @JsonKey(name: 'scheduled_time') DateTime? scheduledTime,
    @JsonKey(name: 'sent_at') DateTime? sentAt,
    @JsonKey(name: 'read_at') DateTime? readAt,
    @JsonKey(name: 'delivery_mode') String? deliveryMode,
    String? language,
    @JsonKey(name: 'audio_url') String? audioUrl,
    @JsonKey(name: 'source_type') String? sourceType,
    @JsonKey(name: 'source_id') int? sourceId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _AppNotification;

  factory AppNotification.fromJson(Map<String, dynamic> json) =>
      _$AppNotificationFromJson(json);
}
