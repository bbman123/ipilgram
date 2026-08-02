import 'package:dio/dio.dart';
import '../../../../core/constants/constants.dart';
import '../../../../core/errors/app_exception.dart';
import '../models/models.dart';

class PackageRepository {
  final Dio _dio;

  PackageRepository(this._dio);

  Future<PackageDetail> getMyPackage() async {
    try {
      final response = await _dio.get(ApiConstants.myPackageEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as Map<String, dynamic>;
      return PackageDetail.fromJson(data);
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }
}
