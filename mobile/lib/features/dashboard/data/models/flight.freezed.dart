// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'flight.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

Flight _$FlightFromJson(Map<String, dynamic> json) {
  return _Flight.fromJson(json);
}

/// @nodoc
mixin _$Flight {
  int get id => throw _privateConstructorUsedError;
  String get airline => throw _privateConstructorUsedError;
  @JsonKey(name: 'flight_number')
  String get flightNumber => throw _privateConstructorUsedError;
  @JsonKey(name: 'departure_airport')
  String get departureAirport => throw _privateConstructorUsedError;
  @JsonKey(name: 'arrival_airport')
  String get arrivalAirport => throw _privateConstructorUsedError;
  @JsonKey(name: 'departure_datetime')
  DateTime get departureDatetime => throw _privateConstructorUsedError;
  @JsonKey(name: 'arrival_datetime')
  DateTime get arrivalDatetime => throw _privateConstructorUsedError;
  String? get gate => throw _privateConstructorUsedError;
  @JsonKey(name: 'seat_number')
  String? get seatNumber => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Flight to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Flight
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $FlightCopyWith<Flight> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $FlightCopyWith<$Res> {
  factory $FlightCopyWith(Flight value, $Res Function(Flight) then) =
      _$FlightCopyWithImpl<$Res, Flight>;
  @useResult
  $Res call(
      {int id,
      String airline,
      @JsonKey(name: 'flight_number') String flightNumber,
      @JsonKey(name: 'departure_airport') String departureAirport,
      @JsonKey(name: 'arrival_airport') String arrivalAirport,
      @JsonKey(name: 'departure_datetime') DateTime departureDatetime,
      @JsonKey(name: 'arrival_datetime') DateTime arrivalDatetime,
      String? gate,
      @JsonKey(name: 'seat_number') String? seatNumber,
      String status,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class _$FlightCopyWithImpl<$Res, $Val extends Flight>
    implements $FlightCopyWith<$Res> {
  _$FlightCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Flight
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? airline = null,
    Object? flightNumber = null,
    Object? departureAirport = null,
    Object? arrivalAirport = null,
    Object? departureDatetime = null,
    Object? arrivalDatetime = null,
    Object? gate = freezed,
    Object? seatNumber = freezed,
    Object? status = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      airline: null == airline
          ? _value.airline
          : airline // ignore: cast_nullable_to_non_nullable
              as String,
      flightNumber: null == flightNumber
          ? _value.flightNumber
          : flightNumber // ignore: cast_nullable_to_non_nullable
              as String,
      departureAirport: null == departureAirport
          ? _value.departureAirport
          : departureAirport // ignore: cast_nullable_to_non_nullable
              as String,
      arrivalAirport: null == arrivalAirport
          ? _value.arrivalAirport
          : arrivalAirport // ignore: cast_nullable_to_non_nullable
              as String,
      departureDatetime: null == departureDatetime
          ? _value.departureDatetime
          : departureDatetime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      arrivalDatetime: null == arrivalDatetime
          ? _value.arrivalDatetime
          : arrivalDatetime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      gate: freezed == gate
          ? _value.gate
          : gate // ignore: cast_nullable_to_non_nullable
              as String?,
      seatNumber: freezed == seatNumber
          ? _value.seatNumber
          : seatNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
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
abstract class _$$FlightImplCopyWith<$Res> implements $FlightCopyWith<$Res> {
  factory _$$FlightImplCopyWith(
          _$FlightImpl value, $Res Function(_$FlightImpl) then) =
      __$$FlightImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String airline,
      @JsonKey(name: 'flight_number') String flightNumber,
      @JsonKey(name: 'departure_airport') String departureAirport,
      @JsonKey(name: 'arrival_airport') String arrivalAirport,
      @JsonKey(name: 'departure_datetime') DateTime departureDatetime,
      @JsonKey(name: 'arrival_datetime') DateTime arrivalDatetime,
      String? gate,
      @JsonKey(name: 'seat_number') String? seatNumber,
      String status,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class __$$FlightImplCopyWithImpl<$Res>
    extends _$FlightCopyWithImpl<$Res, _$FlightImpl>
    implements _$$FlightImplCopyWith<$Res> {
  __$$FlightImplCopyWithImpl(
      _$FlightImpl _value, $Res Function(_$FlightImpl) _then)
      : super(_value, _then);

  /// Create a copy of Flight
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? airline = null,
    Object? flightNumber = null,
    Object? departureAirport = null,
    Object? arrivalAirport = null,
    Object? departureDatetime = null,
    Object? arrivalDatetime = null,
    Object? gate = freezed,
    Object? seatNumber = freezed,
    Object? status = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_$FlightImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      airline: null == airline
          ? _value.airline
          : airline // ignore: cast_nullable_to_non_nullable
              as String,
      flightNumber: null == flightNumber
          ? _value.flightNumber
          : flightNumber // ignore: cast_nullable_to_non_nullable
              as String,
      departureAirport: null == departureAirport
          ? _value.departureAirport
          : departureAirport // ignore: cast_nullable_to_non_nullable
              as String,
      arrivalAirport: null == arrivalAirport
          ? _value.arrivalAirport
          : arrivalAirport // ignore: cast_nullable_to_non_nullable
              as String,
      departureDatetime: null == departureDatetime
          ? _value.departureDatetime
          : departureDatetime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      arrivalDatetime: null == arrivalDatetime
          ? _value.arrivalDatetime
          : arrivalDatetime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      gate: freezed == gate
          ? _value.gate
          : gate // ignore: cast_nullable_to_non_nullable
              as String?,
      seatNumber: freezed == seatNumber
          ? _value.seatNumber
          : seatNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
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
class _$FlightImpl implements _Flight {
  const _$FlightImpl(
      {required this.id,
      required this.airline,
      @JsonKey(name: 'flight_number') required this.flightNumber,
      @JsonKey(name: 'departure_airport') required this.departureAirport,
      @JsonKey(name: 'arrival_airport') required this.arrivalAirport,
      @JsonKey(name: 'departure_datetime') required this.departureDatetime,
      @JsonKey(name: 'arrival_datetime') required this.arrivalDatetime,
      this.gate,
      @JsonKey(name: 'seat_number') this.seatNumber,
      required this.status,
      @JsonKey(name: 'created_at') this.createdAt,
      @JsonKey(name: 'updated_at') this.updatedAt});

  factory _$FlightImpl.fromJson(Map<String, dynamic> json) =>
      _$$FlightImplFromJson(json);

  @override
  final int id;
  @override
  final String airline;
  @override
  @JsonKey(name: 'flight_number')
  final String flightNumber;
  @override
  @JsonKey(name: 'departure_airport')
  final String departureAirport;
  @override
  @JsonKey(name: 'arrival_airport')
  final String arrivalAirport;
  @override
  @JsonKey(name: 'departure_datetime')
  final DateTime departureDatetime;
  @override
  @JsonKey(name: 'arrival_datetime')
  final DateTime arrivalDatetime;
  @override
  final String? gate;
  @override
  @JsonKey(name: 'seat_number')
  final String? seatNumber;
  @override
  final String status;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Flight(id: $id, airline: $airline, flightNumber: $flightNumber, departureAirport: $departureAirport, arrivalAirport: $arrivalAirport, departureDatetime: $departureDatetime, arrivalDatetime: $arrivalDatetime, gate: $gate, seatNumber: $seatNumber, status: $status, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$FlightImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.airline, airline) || other.airline == airline) &&
            (identical(other.flightNumber, flightNumber) ||
                other.flightNumber == flightNumber) &&
            (identical(other.departureAirport, departureAirport) ||
                other.departureAirport == departureAirport) &&
            (identical(other.arrivalAirport, arrivalAirport) ||
                other.arrivalAirport == arrivalAirport) &&
            (identical(other.departureDatetime, departureDatetime) ||
                other.departureDatetime == departureDatetime) &&
            (identical(other.arrivalDatetime, arrivalDatetime) ||
                other.arrivalDatetime == arrivalDatetime) &&
            (identical(other.gate, gate) || other.gate == gate) &&
            (identical(other.seatNumber, seatNumber) ||
                other.seatNumber == seatNumber) &&
            (identical(other.status, status) || other.status == status) &&
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
      airline,
      flightNumber,
      departureAirport,
      arrivalAirport,
      departureDatetime,
      arrivalDatetime,
      gate,
      seatNumber,
      status,
      createdAt,
      updatedAt);

  /// Create a copy of Flight
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$FlightImplCopyWith<_$FlightImpl> get copyWith =>
      __$$FlightImplCopyWithImpl<_$FlightImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$FlightImplToJson(
      this,
    );
  }
}

abstract class _Flight implements Flight {
  const factory _Flight(
      {required final int id,
      required final String airline,
      @JsonKey(name: 'flight_number') required final String flightNumber,
      @JsonKey(name: 'departure_airport')
      required final String departureAirport,
      @JsonKey(name: 'arrival_airport') required final String arrivalAirport,
      @JsonKey(name: 'departure_datetime')
      required final DateTime departureDatetime,
      @JsonKey(name: 'arrival_datetime')
      required final DateTime arrivalDatetime,
      final String? gate,
      @JsonKey(name: 'seat_number') final String? seatNumber,
      required final String status,
      @JsonKey(name: 'created_at') final DateTime? createdAt,
      @JsonKey(name: 'updated_at') final DateTime? updatedAt}) = _$FlightImpl;

  factory _Flight.fromJson(Map<String, dynamic> json) = _$FlightImpl.fromJson;

  @override
  int get id;
  @override
  String get airline;
  @override
  @JsonKey(name: 'flight_number')
  String get flightNumber;
  @override
  @JsonKey(name: 'departure_airport')
  String get departureAirport;
  @override
  @JsonKey(name: 'arrival_airport')
  String get arrivalAirport;
  @override
  @JsonKey(name: 'departure_datetime')
  DateTime get departureDatetime;
  @override
  @JsonKey(name: 'arrival_datetime')
  DateTime get arrivalDatetime;
  @override
  String? get gate;
  @override
  @JsonKey(name: 'seat_number')
  String? get seatNumber;
  @override
  String get status;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of Flight
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$FlightImplCopyWith<_$FlightImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
