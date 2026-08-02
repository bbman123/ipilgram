// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'accommodation.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AccommodationImpl _$$AccommodationImplFromJson(Map<String, dynamic> json) =>
    _$AccommodationImpl(
      id: (json['id'] as num).toInt(),
      hotelName: json['hotel_name'] as String,
      city: json['city'] as String,
      building: json['building'] as String?,
      floor: json['floor'] as String?,
      roomNumber: json['room_number'] as String,
      bedNumber: json['bed_number'] as String?,
      address: json['address'] as String?,
      checkIn: DateTime.parse(json['check_in'] as String),
      checkOut: DateTime.parse(json['check_out'] as String),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$AccommodationImplToJson(_$AccommodationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'hotel_name': instance.hotelName,
      'city': instance.city,
      'building': instance.building,
      'floor': instance.floor,
      'room_number': instance.roomNumber,
      'bed_number': instance.bedNumber,
      'address': instance.address,
      'check_in': instance.checkIn.toIso8601String(),
      'check_out': instance.checkOut.toIso8601String(),
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
