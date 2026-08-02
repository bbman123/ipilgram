// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'package_detail.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

PackageDetail _$PackageDetailFromJson(Map<String, dynamic> json) {
  return _PackageDetail.fromJson(json);
}

/// @nodoc
mixin _$PackageDetail {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  Flight? get flight => throw _privateConstructorUsedError;
  Accommodation? get accommodation => throw _privateConstructorUsedError;
  Transport? get transport => throw _privateConstructorUsedError;
  @JsonKey(name: 'pilgrim_count')
  int get pilgrimCount => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this PackageDetail to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PackageDetailCopyWith<PackageDetail> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PackageDetailCopyWith<$Res> {
  factory $PackageDetailCopyWith(
          PackageDetail value, $Res Function(PackageDetail) then) =
      _$PackageDetailCopyWithImpl<$Res, PackageDetail>;
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      Flight? flight,
      Accommodation? accommodation,
      Transport? transport,
      @JsonKey(name: 'pilgrim_count') int pilgrimCount,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});

  $FlightCopyWith<$Res>? get flight;
  $AccommodationCopyWith<$Res>? get accommodation;
  $TransportCopyWith<$Res>? get transport;
}

/// @nodoc
class _$PackageDetailCopyWithImpl<$Res, $Val extends PackageDetail>
    implements $PackageDetailCopyWith<$Res> {
  _$PackageDetailCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? flight = freezed,
    Object? accommodation = freezed,
    Object? transport = freezed,
    Object? pilgrimCount = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      flight: freezed == flight
          ? _value.flight
          : flight // ignore: cast_nullable_to_non_nullable
              as Flight?,
      accommodation: freezed == accommodation
          ? _value.accommodation
          : accommodation // ignore: cast_nullable_to_non_nullable
              as Accommodation?,
      transport: freezed == transport
          ? _value.transport
          : transport // ignore: cast_nullable_to_non_nullable
              as Transport?,
      pilgrimCount: null == pilgrimCount
          ? _value.pilgrimCount
          : pilgrimCount // ignore: cast_nullable_to_non_nullable
              as int,
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

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $FlightCopyWith<$Res>? get flight {
    if (_value.flight == null) {
      return null;
    }

    return $FlightCopyWith<$Res>(_value.flight!, (value) {
      return _then(_value.copyWith(flight: value) as $Val);
    });
  }

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $AccommodationCopyWith<$Res>? get accommodation {
    if (_value.accommodation == null) {
      return null;
    }

    return $AccommodationCopyWith<$Res>(_value.accommodation!, (value) {
      return _then(_value.copyWith(accommodation: value) as $Val);
    });
  }

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $TransportCopyWith<$Res>? get transport {
    if (_value.transport == null) {
      return null;
    }

    return $TransportCopyWith<$Res>(_value.transport!, (value) {
      return _then(_value.copyWith(transport: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$PackageDetailImplCopyWith<$Res>
    implements $PackageDetailCopyWith<$Res> {
  factory _$$PackageDetailImplCopyWith(
          _$PackageDetailImpl value, $Res Function(_$PackageDetailImpl) then) =
      __$$PackageDetailImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String name,
      String? description,
      Flight? flight,
      Accommodation? accommodation,
      Transport? transport,
      @JsonKey(name: 'pilgrim_count') int pilgrimCount,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});

  @override
  $FlightCopyWith<$Res>? get flight;
  @override
  $AccommodationCopyWith<$Res>? get accommodation;
  @override
  $TransportCopyWith<$Res>? get transport;
}

/// @nodoc
class __$$PackageDetailImplCopyWithImpl<$Res>
    extends _$PackageDetailCopyWithImpl<$Res, _$PackageDetailImpl>
    implements _$$PackageDetailImplCopyWith<$Res> {
  __$$PackageDetailImplCopyWithImpl(
      _$PackageDetailImpl _value, $Res Function(_$PackageDetailImpl) _then)
      : super(_value, _then);

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? flight = freezed,
    Object? accommodation = freezed,
    Object? transport = freezed,
    Object? pilgrimCount = null,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_$PackageDetailImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      description: freezed == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String?,
      flight: freezed == flight
          ? _value.flight
          : flight // ignore: cast_nullable_to_non_nullable
              as Flight?,
      accommodation: freezed == accommodation
          ? _value.accommodation
          : accommodation // ignore: cast_nullable_to_non_nullable
              as Accommodation?,
      transport: freezed == transport
          ? _value.transport
          : transport // ignore: cast_nullable_to_non_nullable
              as Transport?,
      pilgrimCount: null == pilgrimCount
          ? _value.pilgrimCount
          : pilgrimCount // ignore: cast_nullable_to_non_nullable
              as int,
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
class _$PackageDetailImpl implements _PackageDetail {
  const _$PackageDetailImpl(
      {required this.id,
      required this.name,
      this.description,
      this.flight,
      this.accommodation,
      this.transport,
      @JsonKey(name: 'pilgrim_count') this.pilgrimCount = 0,
      @JsonKey(name: 'created_at') this.createdAt,
      @JsonKey(name: 'updated_at') this.updatedAt});

  factory _$PackageDetailImpl.fromJson(Map<String, dynamic> json) =>
      _$$PackageDetailImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final Flight? flight;
  @override
  final Accommodation? accommodation;
  @override
  final Transport? transport;
  @override
  @JsonKey(name: 'pilgrim_count')
  final int pilgrimCount;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'PackageDetail(id: $id, name: $name, description: $description, flight: $flight, accommodation: $accommodation, transport: $transport, pilgrimCount: $pilgrimCount, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PackageDetailImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.flight, flight) || other.flight == flight) &&
            (identical(other.accommodation, accommodation) ||
                other.accommodation == accommodation) &&
            (identical(other.transport, transport) ||
                other.transport == transport) &&
            (identical(other.pilgrimCount, pilgrimCount) ||
                other.pilgrimCount == pilgrimCount) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(runtimeType, id, name, description, flight,
      accommodation, transport, pilgrimCount, createdAt, updatedAt);

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PackageDetailImplCopyWith<_$PackageDetailImpl> get copyWith =>
      __$$PackageDetailImplCopyWithImpl<_$PackageDetailImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PackageDetailImplToJson(
      this,
    );
  }
}

abstract class _PackageDetail implements PackageDetail {
  const factory _PackageDetail(
          {required final int id,
          required final String name,
          final String? description,
          final Flight? flight,
          final Accommodation? accommodation,
          final Transport? transport,
          @JsonKey(name: 'pilgrim_count') final int pilgrimCount,
          @JsonKey(name: 'created_at') final DateTime? createdAt,
          @JsonKey(name: 'updated_at') final DateTime? updatedAt}) =
      _$PackageDetailImpl;

  factory _PackageDetail.fromJson(Map<String, dynamic> json) =
      _$PackageDetailImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  Flight? get flight;
  @override
  Accommodation? get accommodation;
  @override
  Transport? get transport;
  @override
  @JsonKey(name: 'pilgrim_count')
  int get pilgrimCount;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of PackageDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PackageDetailImplCopyWith<_$PackageDetailImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
