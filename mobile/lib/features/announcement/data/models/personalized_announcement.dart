import 'package:freezed_annotation/freezed_annotation.dart';

part 'personalized_announcement.freezed.dart';
part 'personalized_announcement.g.dart';

@freezed
class PersonalizedAnnouncement with _$PersonalizedAnnouncement {
  const factory PersonalizedAnnouncement({
    required int id,
    required String title,
    required String message,
    required String priority,
    @JsonKey(name: 'publish_date') DateTime? publishDate,
    @JsonKey(name: 'expiry_date') DateTime? expiryDate,
    @Default(false) bool simplified,
    @Default(false) bool translated,
    @Default('English') String language,
    @JsonKey(name: 'audio_url') String? audioUrl,
  }) = _PersonalizedAnnouncement;

  factory PersonalizedAnnouncement.fromJson(Map<String, dynamic> json) =>
      _$PersonalizedAnnouncementFromJson(json);
}
