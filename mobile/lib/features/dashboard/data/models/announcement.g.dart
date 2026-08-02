// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'announcement.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AnnouncementImpl _$$AnnouncementImplFromJson(Map<String, dynamic> json) =>
    _$AnnouncementImpl(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      message: json['message'] as String?,
      messageTemplate: json['message_template'] as String?,
      priority: json['priority'] as String,
      publishDate: json['publish_date'] == null
          ? null
          : DateTime.parse(json['publish_date'] as String),
      expiryDate: json['expiry_date'] == null
          ? null
          : DateTime.parse(json['expiry_date'] as String),
      simplified: json['simplified'] as bool?,
      translated: json['translated'] as bool?,
      language: json['language'] as String?,
      audioUrl: json['audio_url'] as String?,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$AnnouncementImplToJson(_$AnnouncementImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'message': instance.message,
      'message_template': instance.messageTemplate,
      'priority': instance.priority,
      'publish_date': instance.publishDate?.toIso8601String(),
      'expiry_date': instance.expiryDate?.toIso8601String(),
      'simplified': instance.simplified,
      'translated': instance.translated,
      'language': instance.language,
      'audio_url': instance.audioUrl,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
