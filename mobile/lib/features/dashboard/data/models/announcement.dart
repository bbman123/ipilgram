import 'package:freezed_annotation/freezed_annotation.dart';

part 'announcement.freezed.dart';
part 'announcement.g.dart';

@freezed
class Announcement with _$Announcement {
  const factory Announcement({
    required int id,
    required String title,
    @JsonKey(name: 'message') String? message,
    @JsonKey(name: 'message_template') String? messageTemplate,
    required String priority,
    @JsonKey(name: 'publish_date') DateTime? publishDate,
    @JsonKey(name: 'expiry_date') DateTime? expiryDate,
    bool? simplified,
    bool? translated,
    String? language,
    @JsonKey(name: 'audio_url') String? audioUrl,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _Announcement;

  factory Announcement.fromJson(Map<String, dynamic> json) =>
      _$AnnouncementFromJson(json);
}
