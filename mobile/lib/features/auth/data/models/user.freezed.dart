// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'user.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

User _$UserFromJson(Map<String, dynamic> json) {
  return _User.fromJson(json);
}

/// @nodoc
mixin _$User {
  int get id => throw _privateConstructorUsedError;
  String get email => throw _privateConstructorUsedError;
  @JsonKey(name: 'full_name')
  String get fullName => throw _privateConstructorUsedError;
  String get role => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_active')
  bool get isActive => throw _privateConstructorUsedError;
  String? get phone => throw _privateConstructorUsedError;
  String? get nationality => throw _privateConstructorUsedError;
  @JsonKey(name: 'passport_number')
  String? get passportNumber => throw _privateConstructorUsedError;
  @JsonKey(name: 'emergency_contact')
  String? get emergencyContact => throw _privateConstructorUsedError;
  @JsonKey(name: 'package_id')
  int? get packageId => throw _privateConstructorUsedError;
  String? get packageName => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this User to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of User
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $UserCopyWith<User> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $UserCopyWith<$Res> {
  factory $UserCopyWith(User value, $Res Function(User) then) =
      _$UserCopyWithImpl<$Res, User>;
  @useResult
  $Res call(
      {int id,
      String email,
      @JsonKey(name: 'full_name') String fullName,
      String role,
      @JsonKey(name: 'is_active') bool isActive,
      String? phone,
      String? nationality,
      @JsonKey(name: 'passport_number') String? passportNumber,
      @JsonKey(name: 'emergency_contact') String? emergencyContact,
      @JsonKey(name: 'package_id') int? packageId,
      String? packageName,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class _$UserCopyWithImpl<$Res, $Val extends User>
    implements $UserCopyWith<$Res> {
  _$UserCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of User
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? email = null,
    Object? fullName = null,
    Object? role = null,
    Object? isActive = null,
    Object? phone = freezed,
    Object? nationality = freezed,
    Object? passportNumber = freezed,
    Object? emergencyContact = freezed,
    Object? packageId = freezed,
    Object? packageName = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      email: null == email
          ? _value.email
          : email // ignore: cast_nullable_to_non_nullable
              as String,
      fullName: null == fullName
          ? _value.fullName
          : fullName // ignore: cast_nullable_to_non_nullable
              as String,
      role: null == role
          ? _value.role
          : role // ignore: cast_nullable_to_non_nullable
              as String,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      phone: freezed == phone
          ? _value.phone
          : phone // ignore: cast_nullable_to_non_nullable
              as String?,
      nationality: freezed == nationality
          ? _value.nationality
          : nationality // ignore: cast_nullable_to_non_nullable
              as String?,
      passportNumber: freezed == passportNumber
          ? _value.passportNumber
          : passportNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      emergencyContact: freezed == emergencyContact
          ? _value.emergencyContact
          : emergencyContact // ignore: cast_nullable_to_non_nullable
              as String?,
      packageId: freezed == packageId
          ? _value.packageId
          : packageId // ignore: cast_nullable_to_non_nullable
              as int?,
      packageName: freezed == packageName
          ? _value.packageName
          : packageName // ignore: cast_nullable_to_non_nullable
              as String?,
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
abstract class _$$UserImplCopyWith<$Res> implements $UserCopyWith<$Res> {
  factory _$$UserImplCopyWith(
          _$UserImpl value, $Res Function(_$UserImpl) then) =
      __$$UserImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String email,
      @JsonKey(name: 'full_name') String fullName,
      String role,
      @JsonKey(name: 'is_active') bool isActive,
      String? phone,
      String? nationality,
      @JsonKey(name: 'passport_number') String? passportNumber,
      @JsonKey(name: 'emergency_contact') String? emergencyContact,
      @JsonKey(name: 'package_id') int? packageId,
      String? packageName,
      @JsonKey(name: 'created_at') DateTime? createdAt,
      @JsonKey(name: 'updated_at') DateTime? updatedAt});
}

/// @nodoc
class __$$UserImplCopyWithImpl<$Res>
    extends _$UserCopyWithImpl<$Res, _$UserImpl>
    implements _$$UserImplCopyWith<$Res> {
  __$$UserImplCopyWithImpl(_$UserImpl _value, $Res Function(_$UserImpl) _then)
      : super(_value, _then);

  /// Create a copy of User
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? email = null,
    Object? fullName = null,
    Object? role = null,
    Object? isActive = null,
    Object? phone = freezed,
    Object? nationality = freezed,
    Object? passportNumber = freezed,
    Object? emergencyContact = freezed,
    Object? packageId = freezed,
    Object? packageName = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(_$UserImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      email: null == email
          ? _value.email
          : email // ignore: cast_nullable_to_non_nullable
              as String,
      fullName: null == fullName
          ? _value.fullName
          : fullName // ignore: cast_nullable_to_non_nullable
              as String,
      role: null == role
          ? _value.role
          : role // ignore: cast_nullable_to_non_nullable
              as String,
      isActive: null == isActive
          ? _value.isActive
          : isActive // ignore: cast_nullable_to_non_nullable
              as bool,
      phone: freezed == phone
          ? _value.phone
          : phone // ignore: cast_nullable_to_non_nullable
              as String?,
      nationality: freezed == nationality
          ? _value.nationality
          : nationality // ignore: cast_nullable_to_non_nullable
              as String?,
      passportNumber: freezed == passportNumber
          ? _value.passportNumber
          : passportNumber // ignore: cast_nullable_to_non_nullable
              as String?,
      emergencyContact: freezed == emergencyContact
          ? _value.emergencyContact
          : emergencyContact // ignore: cast_nullable_to_non_nullable
              as String?,
      packageId: freezed == packageId
          ? _value.packageId
          : packageId // ignore: cast_nullable_to_non_nullable
              as int?,
      packageName: freezed == packageName
          ? _value.packageName
          : packageName // ignore: cast_nullable_to_non_nullable
              as String?,
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
class _$UserImpl implements _User {
  const _$UserImpl(
      {required this.id,
      required this.email,
      @JsonKey(name: 'full_name') required this.fullName,
      this.role = 'pilgrim',
      @JsonKey(name: 'is_active') this.isActive = true,
      this.phone,
      this.nationality,
      @JsonKey(name: 'passport_number') this.passportNumber,
      @JsonKey(name: 'emergency_contact') this.emergencyContact,
      @JsonKey(name: 'package_id') this.packageId,
      this.packageName,
      @JsonKey(name: 'created_at') this.createdAt,
      @JsonKey(name: 'updated_at') this.updatedAt});

  factory _$UserImpl.fromJson(Map<String, dynamic> json) =>
      _$$UserImplFromJson(json);

  @override
  final int id;
  @override
  final String email;
  @override
  @JsonKey(name: 'full_name')
  final String fullName;
  @override
  @JsonKey()
  final String role;
  @override
  @JsonKey(name: 'is_active')
  final bool isActive;
  @override
  final String? phone;
  @override
  final String? nationality;
  @override
  @JsonKey(name: 'passport_number')
  final String? passportNumber;
  @override
  @JsonKey(name: 'emergency_contact')
  final String? emergencyContact;
  @override
  @JsonKey(name: 'package_id')
  final int? packageId;
  @override
  final String? packageName;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'User(id: $id, email: $email, fullName: $fullName, role: $role, isActive: $isActive, phone: $phone, nationality: $nationality, passportNumber: $passportNumber, emergencyContact: $emergencyContact, packageId: $packageId, packageName: $packageName, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$UserImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.fullName, fullName) ||
                other.fullName == fullName) &&
            (identical(other.role, role) || other.role == role) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.nationality, nationality) ||
                other.nationality == nationality) &&
            (identical(other.passportNumber, passportNumber) ||
                other.passportNumber == passportNumber) &&
            (identical(other.emergencyContact, emergencyContact) ||
                other.emergencyContact == emergencyContact) &&
            (identical(other.packageId, packageId) ||
                other.packageId == packageId) &&
            (identical(other.packageName, packageName) ||
                other.packageName == packageName) &&
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
      email,
      fullName,
      role,
      isActive,
      phone,
      nationality,
      passportNumber,
      emergencyContact,
      packageId,
      packageName,
      createdAt,
      updatedAt);

  /// Create a copy of User
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$UserImplCopyWith<_$UserImpl> get copyWith =>
      __$$UserImplCopyWithImpl<_$UserImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$UserImplToJson(
      this,
    );
  }
}

abstract class _User implements User {
  const factory _User(
      {required final int id,
      required final String email,
      @JsonKey(name: 'full_name') required final String fullName,
      final String role,
      @JsonKey(name: 'is_active') final bool isActive,
      final String? phone,
      final String? nationality,
      @JsonKey(name: 'passport_number') final String? passportNumber,
      @JsonKey(name: 'emergency_contact') final String? emergencyContact,
      @JsonKey(name: 'package_id') final int? packageId,
      final String? packageName,
      @JsonKey(name: 'created_at') final DateTime? createdAt,
      @JsonKey(name: 'updated_at') final DateTime? updatedAt}) = _$UserImpl;

  factory _User.fromJson(Map<String, dynamic> json) = _$UserImpl.fromJson;

  @override
  int get id;
  @override
  String get email;
  @override
  @JsonKey(name: 'full_name')
  String get fullName;
  @override
  String get role;
  @override
  @JsonKey(name: 'is_active')
  bool get isActive;
  @override
  String? get phone;
  @override
  String? get nationality;
  @override
  @JsonKey(name: 'passport_number')
  String? get passportNumber;
  @override
  @JsonKey(name: 'emergency_contact')
  String? get emergencyContact;
  @override
  @JsonKey(name: 'package_id')
  int? get packageId;
  @override
  String? get packageName;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt;

  /// Create a copy of User
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$UserImplCopyWith<_$UserImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
