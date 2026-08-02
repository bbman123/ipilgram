import 'package:freezed_annotation/freezed_annotation.dart';

part 'transport.freezed.dart';
part 'transport.g.dart';

@freezed
class Transport with _$Transport {
  const factory Transport({
    required int id,
    @JsonKey(name: 'bus_number') required String busNumber,
    @JsonKey(name: 'pickup_location') required String pickupLocation,
    required String destination,
    @JsonKey(name: 'pickup_time') required DateTime pickupTime,
    @JsonKey(name: 'driver_name') required String driverName,
    @JsonKey(name: 'driver_phone') required String driverPhone,
    @JsonKey(name: 'transport_type') required String transportType,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _Transport;

  factory Transport.fromJson(Map<String, dynamic> json) =>
      _$TransportFromJson(json);
}
