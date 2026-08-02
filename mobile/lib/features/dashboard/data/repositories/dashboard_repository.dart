import 'package:dio/dio.dart';
import '../../../../core/constants/constants.dart';
import '../../../../core/errors/app_exception.dart';
import '../models/models.dart';

class DashboardRepository {
  final Dio _dio;

  DashboardRepository(this._dio);

  Future<List<Flight>> getFlights() async {
    try {
      final response = await _dio.get(ApiConstants.flightsEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as Map<String, dynamic>;
      final items = data['items'] as List;
      return items.map((e) => Flight.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<List<Accommodation>> getAccommodations() async {
    try {
      final response = await _dio.get(ApiConstants.accommodationsEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as Map<String, dynamic>;
      final items = data['items'] as List;
      return items.map((e) => Accommodation.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<List<Transport>> getTransports() async {
    try {
      final response = await _dio.get(ApiConstants.transportsEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as Map<String, dynamic>;
      final items = data['items'] as List;
      return items.map((e) => Transport.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<List<AppNotification>> getMyNotifications() async {
    try {
      final response = await _dio.get(ApiConstants.myNotificationsEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as List;
      return data.map((e) => AppNotification.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<List<Announcement>> getMyAnnouncements() async {
    try {
      final response = await _dio.get(ApiConstants.myAnnouncementsEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as List;
      return data.map((e) => Announcement.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }
}
