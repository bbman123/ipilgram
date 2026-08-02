// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'package_detail.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PackageDetailImpl _$$PackageDetailImplFromJson(Map<String, dynamic> json) =>
    _$PackageDetailImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      flight: json['flight'] == null
          ? null
          : Flight.fromJson(json['flight'] as Map<String, dynamic>),
      accommodation: json['accommodation'] == null
          ? null
          : Accommodation.fromJson(
              json['accommodation'] as Map<String, dynamic>),
      transport: json['transport'] == null
          ? null
          : Transport.fromJson(json['transport'] as Map<String, dynamic>),
      pilgrimCount: (json['pilgrim_count'] as num?)?.toInt() ?? 0,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$PackageDetailImplToJson(_$PackageDetailImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'flight': instance.flight,
      'accommodation': instance.accommodation,
      'transport': instance.transport,
      'pilgrim_count': instance.pilgrimCount,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
