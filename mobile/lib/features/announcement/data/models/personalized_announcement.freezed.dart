// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'personalized_announcement.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

PersonalizedAnnouncement _$PersonalizedAnnouncementFromJson(
    Map<String, dynamic> json) {
  return _PersonalizedAnnouncement.fromJson(json);
}

/// @nodoc
mixin _$PersonalizedAnnouncement {
  int get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  String get message => throw _privateConstructorUsedError;
  String get priority => throw _privateConstructorUsedError;
  @JsonKey(name: 'publish_date')
  DateTime? get publishDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'expiry_date')
  DateTime? get expiryDate => throw _privateConstructorUsedError;
  bool get simplified => throw _privateConstructorUsedError;
  bool get translated => throw _privateConstructorUsedError;
  String get language => throw _privateConstructorUsedError;
  @JsonKey(name: 'audio_url')
  String? get audioUrl => throw _privateConstructorUsedError;

  /// Serializes this PersonalizedAnnouncement to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PersonalizedAnnouncement
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PersonalizedAnnouncementCopyWith<PersonalizedAnnouncement> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PersonalizedAnnouncementCopyWith<$Res> {
  factory $PersonalizedAnnouncementCopyWith(PersonalizedAnnouncement value,
          $Res Function(PersonalizedAnnouncement) then) =
      _$PersonalizedAnnouncementCopyWithImpl<$Res, PersonalizedAnnouncement>;
  @useResult
  $Res call(
      {int id,
      String title,
      String message,
      String priority,
      @JsonKey(name: 'publish_date') DateTime? publishDate,
      @JsonKey(name: 'expiry_date') DateTime? expiryDate,
      bool simplified,
      bool translated,
      String language,
      @JsonKey(name: 'audio_url') String? audioUrl});
}

/// @nodoc
class _$PersonalizedAnnouncementCopyWithImpl<$Res,
        $Val extends PersonalizedAnnouncement>
    implements $PersonalizedAnnouncementCopyWith<$Res> {
  _$PersonalizedAnnouncementCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PersonalizedAnnouncement
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? message = null,
    Object? priority = null,
    Object? publishDate = freezed,
    Object? expiryDate = freezed,
    Object? simplified = null,
    Object? translated = null,
    Object? language = null,
    Object? audioUrl = freezed,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as String,
      publishDate: freezed == publishDate
          ? _value.publishDate
          : publishDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      expiryDate: freezed == expiryDate
          ? _value.expiryDate
          : expiryDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      simplified: null == simplified
          ? _value.simplified
          : simplified // ignore: cast_nullable_to_non_nullable
              as bool,
      translated: null == translated
          ? _value.translated
          : translated // ignore: cast_nullable_to_non_nullable
              as bool,
      language: null == language
          ? _value.language
          : language // ignore: cast_nullable_to_non_nullable
              as String,
      audioUrl: freezed == audioUrl
          ? _value.audioUrl
          : audioUrl // ignore: cast_nullable_to_non_nullable
              as String?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PersonalizedAnnouncementImplCopyWith<$Res>
    implements $PersonalizedAnnouncementCopyWith<$Res> {
  factory _$$PersonalizedAnnouncementImplCopyWith(
          _$PersonalizedAnnouncementImpl value,
          $Res Function(_$PersonalizedAnnouncementImpl) then) =
      __$$PersonalizedAnnouncementImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {int id,
      String title,
      String message,
      String priority,
      @JsonKey(name: 'publish_date') DateTime? publishDate,
      @JsonKey(name: 'expiry_date') DateTime? expiryDate,
      bool simplified,
      bool translated,
      String language,
      @JsonKey(name: 'audio_url') String? audioUrl});
}

/// @nodoc
class __$$PersonalizedAnnouncementImplCopyWithImpl<$Res>
    extends _$PersonalizedAnnouncementCopyWithImpl<$Res,
        _$PersonalizedAnnouncementImpl>
    implements _$$PersonalizedAnnouncementImplCopyWith<$Res> {
  __$$PersonalizedAnnouncementImplCopyWithImpl(
      _$PersonalizedAnnouncementImpl _value,
      $Res Function(_$PersonalizedAnnouncementImpl) _then)
      : super(_value, _then);

  /// Create a copy of PersonalizedAnnouncement
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? message = null,
    Object? priority = null,
    Object? publishDate = freezed,
    Object? expiryDate = freezed,
    Object? simplified = null,
    Object? translated = null,
    Object? language = null,
    Object? audioUrl = freezed,
  }) {
    return _then(_$PersonalizedAnnouncementImpl(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as int,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      message: null == message
          ? _value.message
          : message // ignore: cast_nullable_to_non_nullable
              as String,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as String,
      publishDate: freezed == publishDate
          ? _value.publishDate
          : publishDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      expiryDate: freezed == expiryDate
          ? _value.expiryDate
          : expiryDate // ignore: cast_nullable_to_non_nullable
              as DateTime?,
      simplified: null == simplified
          ? _value.simplified
          : simplified // ignore: cast_nullable_to_non_nullable
              as bool,
      translated: null == translated
          ? _value.translated
          : translated // ignore: cast_nullable_to_non_nullable
              as bool,
      language: null == language
          ? _value.language
          : language // ignore: cast_nullable_to_non_nullable
              as String,
      audioUrl: freezed == audioUrl
          ? _value.audioUrl
          : audioUrl // ignore: cast_nullable_to_non_nullable
              as String?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PersonalizedAnnouncementImpl implements _PersonalizedAnnouncement {
  const _$PersonalizedAnnouncementImpl(
      {required this.id,
      required this.title,
      required this.message,
      required this.priority,
      @JsonKey(name: 'publish_date') this.publishDate,
      @JsonKey(name: 'expiry_date') this.expiryDate,
      this.simplified = false,
      this.translated = false,
      this.language = 'English',
      @JsonKey(name: 'audio_url') this.audioUrl});

  factory _$PersonalizedAnnouncementImpl.fromJson(Map<String, dynamic> json) =>
      _$$PersonalizedAnnouncementImplFromJson(json);

  @override
  final int id;
  @override
  final String title;
  @override
  final String message;
  @override
  final String priority;
  @override
  @JsonKey(name: 'publish_date')
  final DateTime? publishDate;
  @override
  @JsonKey(name: 'expiry_date')
  final DateTime? expiryDate;
  @override
  @JsonKey()
  final bool simplified;
  @override
  @JsonKey()
  final bool translated;
  @override
  @JsonKey()
  final String language;
  @override
  @JsonKey(name: 'audio_url')
  final String? audioUrl;

  @override
  String toString() {
    return 'PersonalizedAnnouncement(id: $id, title: $title, message: $message, priority: $priority, publishDate: $publishDate, expiryDate: $expiryDate, simplified: $simplified, translated: $translated, language: $language, audioUrl: $audioUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PersonalizedAnnouncementImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.message, message) || other.message == message) &&
            (identical(other.priority, priority) ||
                other.priority == priority) &&
            (identical(other.publishDate, publishDate) ||
                other.publishDate == publishDate) &&
            (identical(other.expiryDate, expiryDate) ||
                other.expiryDate == expiryDate) &&
            (identical(other.simplified, simplified) ||
                other.simplified == simplified) &&
            (identical(other.translated, translated) ||
                other.translated == translated) &&
            (identical(other.language, language) ||
                other.language == language) &&
            (identical(other.audioUrl, audioUrl) ||
                other.audioUrl == audioUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(runtimeType, id, title, message, priority,
      publishDate, expiryDate, simplified, translated, language, audioUrl);

  /// Create a copy of PersonalizedAnnouncement
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PersonalizedAnnouncementImplCopyWith<_$PersonalizedAnnouncementImpl>
      get copyWith => __$$PersonalizedAnnouncementImplCopyWithImpl<
          _$PersonalizedAnnouncementImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PersonalizedAnnouncementImplToJson(
      this,
    );
  }
}

abstract class _PersonalizedAnnouncement implements PersonalizedAnnouncement {
  const factory _PersonalizedAnnouncement(
          {required final int id,
          required final String title,
          required final String message,
          required final String priority,
          @JsonKey(name: 'publish_date') final DateTime? publishDate,
          @JsonKey(name: 'expiry_date') final DateTime? expiryDate,
          final bool simplified,
          final bool translated,
          final String language,
          @JsonKey(name: 'audio_url') final String? audioUrl}) =
      _$PersonalizedAnnouncementImpl;

  factory _PersonalizedAnnouncement.fromJson(Map<String, dynamic> json) =
      _$PersonalizedAnnouncementImpl.fromJson;

  @override
  int get id;
  @override
  String get title;
  @override
  String get message;
  @override
  String get priority;
  @override
  @JsonKey(name: 'publish_date')
  DateTime? get publishDate;
  @override
  @JsonKey(name: 'expiry_date')
  DateTime? get expiryDate;
  @override
  bool get simplified;
  @override
  bool get translated;
  @override
  String get language;
  @override
  @JsonKey(name: 'audio_url')
  String? get audioUrl;

  /// Create a copy of PersonalizedAnnouncement
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PersonalizedAnnouncementImplCopyWith<_$PersonalizedAnnouncementImpl>
      get copyWith => throw _privateConstructorUsedError;
}
