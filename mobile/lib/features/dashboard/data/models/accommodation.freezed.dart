// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'accommodation.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

Accommodation _$AccommodationFromJson(Map<String, dynamic> json) {
  return _Accommodation.fromJson(json);
}

/// @nodoc
mixin _$Accommodation {
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'hotel_name')
  String get hotelName => throw _privateConstructorUsedError;
  String get city => throw _privateConstructorUsedError;
  String? get building => throw _privateConstructorUsedError;
  String? get floor => throw _privateConstructorUsedError;
  @JsonKey(name: 'room_number')
  String get roomNumber => throw _privateConstructorUsedError;
  @JsonKey(name: 'bed_number')
  String? get bedNumber => throw _privateConstructorUsedError;
  String? get address => throw _privateConstructorUsedError;
  @JsonKey(name: 'check_in')
  DateTime get checkIn => throw _privateConstructorUsedError;
  @JsonKey(name: 'check_out')
  DateTime get checkOut => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Accommodation to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Accommodation
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AccommodationCopyWith<Accommodation> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AccommodationCopyWith<$Res> {
  factory $AccommodationCopyWith(
          Accommodation value, $Res Function(Accommodation) then) =
      _$AccommodationCopyWithImpl<$Res, Accommodation>;
  @useResult
  $Res call(
      {int id,
      @JsonKey(name: 'hotel_name') String hotelName,
      String city,
      String? building,
      String? floor,
      @JsonKey(name: 'room_number') String roomNumber,
      @JsonKey(name: 'bed_number') String? bedNumber,
      String? address,
      @JsonKey(name: 'check_in') DateTime checkIn,
      @JsonKey(name: 'check_out') DateTime checkOut,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class _$AccommodationCopyWithImpl<$Res, $Val extends Accommodation>
    implements $AccommodationCopyWith<$Res> {
  _$AccommodationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Accommodation
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? hotelName = null,
    Object? city = null,
    Object? building = freezed,
    Object? floor = freezed,
    Object? roomNumber = null,
    Object? bedNumber = freezed,
    Object? address = freezed,
    Object? checkIn = null,
    Object? checkOut = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      hotelName: null == hotelName
          ? _value.hotelName
          : hotelName // ignore: cast_nullable_to_non_nullable
              as String,
      city: null == city
          ? _value.city
          : city // ignore: cast_nullable_to_non_nullable
              as String,
      building: freezed == building
          ? _value.building
          : building // ignore: cast_nullable_to_non_nullable
              as String?,
      floor: freezed == floor
          ? _value.floor
          : floor // ignore: cast_nullable_to_non_nullable
              as String?,
      roomNumber: null == roomNumber
          ? _value.roomNumber
          : roomNumber // ignore: cast_nullable_to_non_nullable
              as String,
      bedNumber: freezed == bedNumber
          ? _value.bedNumber
          : bedNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      address: freezed == address
          ? _value.address
          : address // ignore: cast_nullable_to_non_nullable
              as String?,
      checkIn: null == checkIn
          ? _value.checkIn
          : checkIn // ignore: cast_nullable_to_non_nullable
              as DateTime,
      checkOut: null == checkOut
          ? _value.checkOut
          : checkOut // ignore: cast_nullable_to_non_nullable
              as DateTime,
      createdAt: freezed == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      updatedAt: freezed == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$AccommodationImplCopyWith<$Res>
    implements $AccommodationCopyWith<$Res> {
  factory _$$AccommodationImplCopyWith(
          _$AccommodationImpl value, $Res Function(_$AccommodationImpl) then) =
      __$$AccommodationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      @JsonKey(name: 'hotel_name') String hotelName,
      String city,
      String? building,
      String? floor,
      @JsonKey(name: 'room_number') String roomNumber,
      @JsonKey(name: 'bed_number') String? bedNumber,
      String? address,
      @JsonKey(name: 'check_in') DateTime checkIn,
      @JsonKey(name: 'check_out') DateTime checkOut,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class __$$AccommodationImplCopyWithImpl<$Res>
    extends _$AccommodationCopyWithImpl<$Res, _$AccommodationImpl>
    implements _$$AccommodationImplCopyWith<$Res> {
  __$$AccommodationImplCopyWithImpl(
      _$AccommodationImpl _value, $Res Function(_$AccommodationImpl) _then)
      : super(_value, _then);

  /// Create a copy of Accommodation
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? hotelName = null,
    Object? city = null,
    Object? building = freezed,
    Object? floor = freezed,
    Object? roomNumber = null,
    Object? bedNumber = freezed,
    Object? address = freezed,
    Object? checkIn = null,
    Object? checkOut = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_$AccommodationImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      hotelName: null == hotelName
          ? _value.hotelName
          : hotelName // ignore: cast_nullable_to_non_nullable
              as String,
      city: null == city
          ? _value.city
          : city // ignore: cast_nullable_to_non_nullable
              as String,
      building: freezed == building
          ? _value.building
          : building // ignore: cast_nullable_to_non_nullable
              as String?,
      floor: freezed == floor
          ? _value.floor
          : floor // ignore: cast_nullable_to_non_nullable
              as String?,
      roomNumber: null == roomNumber
          ? _value.roomNumber
          : roomNumber // ignore: cast_nullable_to_non_nullable
              as String,
      bedNumber: freezed == bedNumber
          ? _value.bedNumber
          : bedNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      address: freezed == address
          ? _value.address
          : address // ignore: cast_nullable_to_non_nullable
              as String?,
      checkIn: null == checkIn
          ? _value.checkIn
          : checkIn // ignore: cast_nullable_to_non_nullable
              as DateTime,
      checkOut: null == checkOut
          ? _value.checkOut
          : checkOut // ignore: cast_nullable_to_non_nullable
              as DateTime,
      createdAt: freezed == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      updatedAt: freezed == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$AccommodationImpl implements _Accommodation {
  const _$AccommodationImpl(
      {required this.id,
      @JsonKey(name: 'hotel_name') required this.hotelName,
      required this.city,
      this.building,
      this.floor,
      @JsonKey(name: 'room_number') required this.roomNumber,
      @JsonKey(name: 'bed_number') this.bedNumber,
      this.address,
      @JsonKey(name: 'check_in') required this.checkIn,
      @JsonKey(name: 'check_out') required this.checkOut,
      @JsonKey(name: 'created_at') this.createdAt,
      @JsonKey(name: 'updated_at') this.updatedAt});

  factory _$AccommodationImpl.fromJson(Map<String, dynamic> json) =>
      _$$AccommodationImplFromJson(json);

  @override
  final int id;
  @override
  @JsonKey(name: 'hotel_name')
  final String hotelName;
  @override
  final String city;
  @override
  final String? building;
  @override
  final String? floor;
  @override
  @JsonKey(name: 'room_number')
  final String roomNumber;
  @override
  @JsonKey(name: 'bed_number')
  final String? bedNumber;
  @override
  final String? address;
  @override
  @JsonKey(name: 'check_in')
  final DateTime checkIn;
  @override
  @JsonKey(name: 'check_out')
  final DateTime checkOut;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Accommodation(id: $id, hotelName: $hotelName, city: $city, building: $building, floor: $floor, roomNumber: $roomNumber, bedNumber: $bedNumber, address: $address, checkIn: $checkIn, checkOut: $checkOut, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AccommodationImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.hotelName, hotelName) ||
                other.hotelName == hotelName) &&
            (identical(other.city, city) || other.city == city) &&
            (identical(other.building, building) ||
                other.building == building) &&
            (identical(other.floor, floor) || other.floor == floor) &&
            (identical(other.roomNumber, roomNumber) ||
                other.roomNumber == roomNumber) &&
            (identical(other.bedNumber, bedNumber) ||
                other.bedNumber == bedNumber) &&
            (identical(other.address, address) || other.address == address) &&
            (identical(other.checkIn, checkIn) || other.checkIn == checkIn) &&
            (identical(other.checkOut, checkOut) ||
                other.checkOut == checkOut) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      id,
      hotelName,
      city,
      building,
      floor,
      roomNumber,
      bedNumber,
      address,
      checkIn,
      checkOut,
      createdAt,
      updatedAt);

  /// Create a copy of Accommodation
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AccommodationImplCopyWith<_$AccommodationImpl> get copyWith =>
      __$$AccommodationImplCopyWithImpl<_$AccommodationImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AccommodationImplToJson(
      this,
    );
  }
}

abstract class _Accommodation implements Accommodation {
  const factory _Accommodation(
          {required final int id,
          @JsonKey(name: 'hotel_name') required final String hotelName,
          required final String city,
          final String? building,
          final String? floor,
          @JsonKey(name: 'room_number') required final String roomNumber,
          @JsonKey(name: 'bed_number') final String? bedNumber,
          final String? address,
          @JsonKey(name: 'check_in') required final DateTime checkIn,
          @JsonKey(name: 'check_out') required final DateTime checkOut,
          @JsonKey(name: 'created_at') final DateTime? createdAt,
          @JsonKey(name: 'updated_at') final DateTime? updatedAt}) =
      _$AccommodationImpl;

  factory _Accommodation.fromJson(Map<String, dynamic> json) =
      _$AccommodationImpl.fromJson;

  @override
  int get id;
  @override
  @JsonKey(name: 'hotel_name')
  String get hotelName;
  @override
  String get city;
  @override
  String? get building;
  @override
  String? get floor;
  @override
  @JsonKey(name: 'room_number')
  String get roomNumber;
  @override
  @JsonKey(name: 'bed_number')
  String? get bedNumber;
  @override
  String? get address;
  @override
  @JsonKey(name: 'check_in')
  DateTime get checkIn;
  @override
  @JsonKey(name: 'check_out')
  DateTime get checkOut;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of Accommodation
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AccommodationImplCopyWith<_$AccommodationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
