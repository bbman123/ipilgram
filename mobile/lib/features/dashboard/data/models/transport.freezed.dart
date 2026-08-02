// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'transport.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

Transport _$TransportFromJson(Map<String, dynamic> json) {
  return _Transport.fromJson(json);
}

/// @nodoc
mixin _$Transport {
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'bus_number')
  String get busNumber => throw _privateConstructorUsedError;
  @JsonKey(name: 'pickup_location')
  String get pickupLocation => throw _privateConstructorUsedError;
  String get destination => throw _privateConstructorUsedError;
  @JsonKey(name: 'pickup_time')
  DateTime get pickupTime => throw _privateConstructorUsedError;
  @JsonKey(name: 'driver_name')
  String get driverName => throw _privateConstructorUsedError;
  @JsonKey(name: 'driver_phone')
  String get driverPhone => throw _privateConstructorUsedError;
  @JsonKey(name: 'transport_type')
  String get transportType => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Transport to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Transport
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $TransportCopyWith<Transport> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TransportCopyWith<$Res> {
  factory $TransportCopyWith(Transport value, $Res Function(Transport) then) =
      _$TransportCopyWithImpl<$Res, Transport>;
  @useResult
  $Res call(
      {int id,
      @JsonKey(name: 'bus_number') String busNumber,
      @JsonKey(name: 'pickup_location') String pickupLocation,
      String destination,
      @JsonKey(name: 'pickup_time') DateTime pickupTime,
      @JsonKey(name: 'driver_name') String driverName,
      @JsonKey(name: 'driver_phone') String driverPhone,
      @JsonKey(name: 'transport_type') String transportType,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class _$TransportCopyWithImpl<$Res, $Val extends Transport>
    implements $TransportCopyWith<$Res> {
  _$TransportCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Transport
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? busNumber = null,
    Object? pickupLocation = null,
    Object? destination = null,
    Object? pickupTime = null,
    Object? driverName = null,
    Object? driverPhone = null,
    Object? transportType = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      busNumber: null == busNumber
          ? _value.busNumber
          : busNumber // ignore: cast_nullable_to_non_nullable
              as String,
      pickupLocation: null == pickupLocation
          ? _value.pickupLocation
          : pickupLocation // ignore: cast_nullable_to_non_nullable
              as String,
      destination: null == destination
          ? _value.destination
          : destination // ignore: cast_nullable_to_non_nullable
              as String,
      pickupTime: null == pickupTime
          ? _value.pickupTime
          : pickupTime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      driverName: null == driverName
          ? _value.driverName
          : driverName // ignore: cast_nullable_to_non_nullable
              as String,
      driverPhone: null == driverPhone
          ? _value.driverPhone
          : driverPhone // ignore: cast_nullable_to_non_nullable
              as String,
      transportType: null == transportType
          ? _value.transportType
          : transportType // ignore: cast_nullable_to_non_nullable
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
abstract class _$$TransportImplCopyWith<$Res>
    implements $TransportCopyWith<$Res> {
  factory _$$TransportImplCopyWith(
          _$TransportImpl value, $Res Function(_$TransportImpl) then) =
      __$$TransportImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      @JsonKey(name: 'bus_number') String busNumber,
      @JsonKey(name: 'pickup_location') String pickupLocation,
      String destination,
      @JsonKey(name: 'pickup_time') DateTime pickupTime,
      @JsonKey(name: 'driver_name') String driverName,
      @JsonKey(name: 'driver_phone') String driverPhone,
      @JsonKey(name: 'transport_type') String transportType,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class __$$TransportImplCopyWithImpl<$Res>
    extends _$TransportCopyWithImpl<$Res, _$TransportImpl>
    implements _$$TransportImplCopyWith<$Res> {
  __$$TransportImplCopyWithImpl(
      _$TransportImpl _value, $Res Function(_$TransportImpl) _then)
      : super(_value, _then);

  /// Create a copy of Transport
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? busNumber = null,
    Object? pickupLocation = null,
    Object? destination = null,
    Object? pickupTime = null,
    Object? driverName = null,
    Object? driverPhone = null,
    Object? transportType = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_$TransportImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      busNumber: null == busNumber
          ? _value.busNumber
          : busNumber // ignore: cast_nullable_to_non_nullable
              as String,
      pickupLocation: null == pickupLocation
          ? _value.pickupLocation
          : pickupLocation // ignore: cast_nullable_to_non_nullable
              as String,
      destination: null == destination
          ? _value.destination
          : destination // ignore: cast_nullable_to_non_nullable
              as String,
      pickupTime: null == pickupTime
          ? _value.pickupTime
          : pickupTime // ignore: cast_nullable_to_non_nullable
              as DateTime,
      driverName: null == driverName
          ? _value.driverName
          : driverName // ignore: cast_nullable_to_non_nullable
              as String,
      driverPhone: null == driverPhone
          ? _value.driverPhone
          : driverPhone // ignore: cast_nullable_to_non_nullable
              as String,
      transportType: null == transportType
          ? _value.transportType
          : transportType // ignore: cast_nullable_to_non_nullable
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
class _$TransportImpl implements _Transport {
  const _$TransportImpl(
      {required this.id,
      @JsonKey(name: 'bus_number') required this.busNumber,
      @JsonKey(name: 'pickup_location') required this.pickupLocation,
      required this.destination,
      @JsonKey(name: 'pickup_time') required this.pickupTime,
      @JsonKey(name: 'driver_name') required this.driverName,
      @JsonKey(name: 'driver_phone') required this.driverPhone,
      @JsonKey(name: 'transport_type') required this.transportType,
      @JsonKey(name: 'created_at') this.createdAt,
      @JsonKey(name: 'updated_at') this.updatedAt});

  factory _$TransportImpl.fromJson(Map<String, dynamic> json) =>
      _$$TransportImplFromJson(json);

  @override
  final int id;
  @override
  @JsonKey(name: 'bus_number')
  final String busNumber;
  @override
  @JsonKey(name: 'pickup_location')
  final String pickupLocation;
  @override
  final String destination;
  @override
  @JsonKey(name: 'pickup_time')
  final DateTime pickupTime;
  @override
  @JsonKey(name: 'driver_name')
  final String driverName;
  @override
  @JsonKey(name: 'driver_phone')
  final String driverPhone;
  @override
  @JsonKey(name: 'transport_type')
  final String transportType;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Transport(id: $id, busNumber: $busNumber, pickupLocation: $pickupLocation, destination: $destination, pickupTime: $pickupTime, driverName: $driverName, driverPhone: $driverPhone, transportType: $transportType, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TransportImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.busNumber, busNumber) ||
                other.busNumber == busNumber) &&
            (identical(other.pickupLocation, pickupLocation) ||
                other.pickupLocation == pickupLocation) &&
            (identical(other.destination, destination) ||
                other.destination == destination) &&
            (identical(other.pickupTime, pickupTime) ||
                other.pickupTime == pickupTime) &&
            (identical(other.driverName, driverName) ||
                other.driverName == driverName) &&
            (identical(other.driverPhone, driverPhone) ||
                other.driverPhone == driverPhone) &&
            (identical(other.transportType, transportType) ||
                other.transportType == transportType) &&
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
      busNumber,
      pickupLocation,
      destination,
      pickupTime,
      driverName,
      driverPhone,
      transportType,
      createdAt,
      updatedAt);

  /// Create a copy of Transport
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$TransportImplCopyWith<_$TransportImpl> get copyWith =>
      __$$TransportImplCopyWithImpl<_$TransportImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$TransportImplToJson(
      this,
    );
  }
}

abstract class _Transport implements Transport {
  const factory _Transport(
      {required final int id,
      @JsonKey(name: 'bus_number') required final String busNumber,
      @JsonKey(name: 'pickup_location') required final String pickupLocation,
      required final String destination,
      @JsonKey(name: 'pickup_time') required final DateTime pickupTime,
      @JsonKey(name: 'driver_name') required final String driverName,
      @JsonKey(name: 'driver_phone') required final String driverPhone,
      @JsonKey(name: 'transport_type') required final String transportType,
      @JsonKey(name: 'created_at') final DateTime? createdAt,
      @JsonKey(name: 'updated_at')
      final DateTime? updatedAt}) = _$TransportImpl;

  factory _Transport.fromJson(Map<String, dynamic> json) =
      _$TransportImpl.fromJson;

  @override
  int get id;
  @override
  @JsonKey(name: 'bus_number')
  String get busNumber;
  @override
  @JsonKey(name: 'pickup_location')
  String get pickupLocation;
  @override
  String get destination;
  @override
  @JsonKey(name: 'pickup_time')
  DateTime get pickupTime;
  @override
  @JsonKey(name: 'driver_name')
  String get driverName;
  @override
  @JsonKey(name: 'driver_phone')
  String get driverPhone;
  @override
  @JsonKey(name: 'transport_type')
  String get transportType;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of Transport
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$TransportImplCopyWith<_$TransportImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
