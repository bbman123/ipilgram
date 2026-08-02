// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'transport.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$TransportImpl _$$TransportImplFromJson(Map<String, dynamic> json) =>
    _$TransportImpl(
      id: (json['id'] as num).toInt(),
      busNumber: json['bus_number'] as String,
      pickupLocation: json['pickup_location'] as String,
      destination: json['destination'] as String,
      pickupTime: DateTime.parse(json['pickup_time'] as String),
      driverName: json['driver_name'] as String,
      driverPhone: json['driver_phone'] as String,
      transportType: json['transport_type'] as String,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$TransportImplToJson(_$TransportImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'bus_number': instance.busNumber,
      'pickup_location': instance.pickupLocation,
      'destination': instance.destination,
      'pickup_time': instance.pickupTime.toIso8601String(),
      'driver_name': instance.driverName,
      'driver_phone': instance.driverPhone,
      'transport_type': instance.transportType,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
