import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required int id,
    required String email,
    @JsonKey(name: 'full_name') required String fullName,
    @Default('pilgrim') String role,
    @JsonKey(name: 'is_active') @Default(true) bool isActive,
    String? phone,
    String? nationality,
    @JsonKey(name: 'passport_number') String? passportNumber,
    @JsonKey(name: 'emergency_contact') String? emergencyContact,
    @JsonKey(name: 'package_id') int? packageId,
    String? packageName,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
