// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'personalized_announcement.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PersonalizedAnnouncementImpl _$$PersonalizedAnnouncementImplFromJson(
        Map<String, dynamic> json) =>
    _$PersonalizedAnnouncementImpl(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      message: json['message'] as String,
      priority: json['priority'] as String,
      publishDate: json['publish_date'] == null
          ? null
          : DateTime.parse(json['publish_date'] as String),
      expiryDate: json['expiry_date'] == null
          ? null
          : DateTime.parse(json['expiry_date'] as String),
      simplified: json['simplified'] as bool? ?? false,
      translated: json['translated'] as bool? ?? false,
      language: json['language'] as String? ?? 'English',
      audioUrl: json['audio_url'] as String?,
    );

Map<String, dynamic> _$$PersonalizedAnnouncementImplToJson(
        _$PersonalizedAnnouncementImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'message': instance.message,
      'priority': instance.priority,
      'publish_date': instance.publishDate?.toIso8601String(),
      'expiry_date': instance.expiryDate?.toIso8601String(),
      'simplified': instance.simplified,
      'translated': instance.translated,
      'language': instance.language,
      'audio_url': instance.audioUrl,
    };
