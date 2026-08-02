// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'flight.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$FlightImpl _$$FlightImplFromJson(Map<String, dynamic> json) => _$FlightImpl(
      id: (json['id'] as num).toInt(),
      airline: json['airline'] as String,
      flightNumber: json['flight_number'] as String,
      departureAirport: json['departure_airport'] as String,
      arrivalAirport: json['arrival_airport'] as String,
      departureDatetime: DateTime.parse(json['departure_datetime'] as String),
      arrivalDatetime: DateTime.parse(json['arrival_datetime'] as String),
      gate: json['gate'] as String?,
      seatNumber: json['seat_number'] as String?,
      status: json['status'] as String,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] == null
          ? null
          : DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$FlightImplToJson(_$FlightImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'airline': instance.airline,
      'flight_number': instance.flightNumber,
      'departure_airport': instance.departureAirport,
      'arrival_airport': instance.arrivalAirport,
      'departure_datetime': instance.departureDatetime.toIso8601String(),
      'arrival_datetime': instance.arrivalDatetime.toIso8601String(),
      'gate': instance.gate,
      'seat_number': instance.seatNumber,
      'status': instance.status,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
    };
