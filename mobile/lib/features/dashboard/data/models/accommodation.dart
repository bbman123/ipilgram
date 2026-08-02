import 'package:freezed_annotation/freezed_annotation.dart';

part 'accommodation.freezed.dart';
part 'accommodation.g.dart';

@freezed
class Accommodation with _$Accommodation {
  const factory Accommodation({
    required int id,
    @JsonKey(name: 'hotel_name') required String hotelName,
    required String city,
    String? building,
    String? floor,
    @JsonKey(name: 'room_number') required String roomNumber,
    @JsonKey(name: 'bed_number') String? bedNumber,
    String? address,
    @JsonKey(name: 'check_in') required DateTime checkIn,
    @JsonKey(name: 'check_out') required DateTime checkOut,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _Accommodation;

  factory Accommodation.fromJson(Map<String, dynamic> json) =>
      _$AccommodationFromJson(json);
}
