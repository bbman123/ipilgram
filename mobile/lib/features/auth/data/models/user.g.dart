// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$UserImpl _$$UserImplFromJson(Map<String, dynamic> json) => _$UserImpl(
      id: (json['id'] as num).toInt(),
      email: json['email'] as String,
      fullName: json['full_name'] as String,
      role: json['role'] as String? ?? 'pilgrim',
      isActive: json['is_active'] as bool? ?? true,
      phone: json['phone'] as String?,
      nationality: json['nationality'] as String?,
      passportNumber: json['passport_number'] as String?,
      emergencyContact: json['emergency_contact'] as String?,
      packageId: (json['package_id'] as num?)?.toInt(),
      packageName: json['packageName'] as String?,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$UserImplToJson(_$UserImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'email': instance.email,
      'full_name': instance.fullName,
      'role': instance.role,
      'is_active': instance.isActive,
      'phone': instance.phone,
      'nationality': instance.nationality,
      'passport_number': instance.passportNumber,
      'emergency_contact': instance.emergencyContact,
      'package_id': instance.packageId,
      'packageName': instance.packageName,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
