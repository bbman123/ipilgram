import 'package:freezed_annotation/freezed_annotation.dart';
import '../../../dashboard/data/models/models.dart';

part 'package_detail.freezed.dart';
part 'package_detail.g.dart';

@freezed
class PackageDetail with _$PackageDetail {
  const factory PackageDetail({
    required int id,
    required String name,
    String? description,
    Flight? flight,
    Accommodation? accommodation,
    Transport? transport,
    @JsonKey(name: 'pilgrim_count') @Default(0) int pilgrimCount,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _PackageDetail;

  factory PackageDetail.fromJson(Map<String, dynamic> json) =>
      _$PackageDetailFromJson(json);
}
