// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_notification.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AppNotificationImpl _$$AppNotificationImplFromJson(
        Map<String, dynamic> json) =>
    _$AppNotificationImpl(
      id: (json['id'] as num).toInt(),
      pilgrimId: (json['pilgrim_id'] as num).toInt(),
      title: json['title'] as String,
      message: json['message'] as String,
      notificationType: json['notification_type'] as String,
      status: json['status'] as String,
      scheduledTime: json['scheduled_time'] == null
          ? null
          : DateTime.parse(json['scheduled_time'] as String),
      sentAt: json['sent_at'] == null
          ? null
          : DateTime.parse(json['sent_at'] as String),
      readAt: json['read_at'] == null
          ? null
          : DateTime.parse(json['read_at'] as String),
      deliveryMode: json['delivery_mode'] as String?,
      language: json['language'] as String?,
      audioUrl: json['audio_url'] as String?,
      sourceType: json['source_type'] as String?,
      sourceId: (json['source_id'] as num?)?.toInt(),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$AppNotificationImplToJson(
        _$AppNotificationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'pilgrim_id': instance.pilgrimId,
      'title': instance.title,
      'message': instance.message,
      'notification_type': instance.notificationType,
      'status': instance.status,
      'scheduled_time': instance.scheduledTime?.toIso8601String(),
      'sent_at': instance.sentAt?.toIso8601String(),
      'read_at': instance.readAt?.toIso8601String(),
      'delivery_mode': instance.deliveryMode,
      'language': instance.language,
      'audio_url': instance.audioUrl,
      'source_type': instance.sourceType,
      'source_id': instance.sourceId,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
