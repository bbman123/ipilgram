import 'package:freezed_annotation/freezed_annotation.dart';

part 'flight.freezed.dart';
part 'flight.g.dart';

@freezed
class Flight with _$Flight {
  const factory Flight({
    required int id,
    required String airline,
    @JsonKey(name: 'flight_number') required String flightNumber,
    @JsonKey(name: 'departure_airport') required String departureAirport,
    @JsonKey(name: 'arrival_airport') required String arrivalAirport,
    @JsonKey(name: 'departure_datetime') required DateTime departureDatetime,
    @JsonKey(name: 'arrival_datetime') required DateTime arrivalDatetime,
    String? gate,
    @JsonKey(name: 'seat_number') String? seatNumber,
    required String status,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _Flight;

  factory Flight.fromJson(Map<String, dynamic> json) => _$FlightFromJson(json);
}
