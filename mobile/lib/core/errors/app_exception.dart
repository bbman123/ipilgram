import 'package:dio/dio.dart';

class AppException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic data;

  AppException({
    required this.message,
    this.statusCode,
    this.data,
  });

  @override
  String toString() => message;

  factory AppException.fromDioError(DioException dioError) {
    switch (dioError.type) {
      case DioExceptionType.connectionTimeout:
        return AppException(message: 'Connection timed out. Please try again.');
      case DioExceptionType.sendTimeout:
        return AppException(message: 'Send timeout. Please try again.');
      case DioExceptionType.receiveTimeout:
        return AppException(message: 'Receive timeout. Please try again.');
      case DioExceptionType.badResponse:
        return _handleBadResponse(dioError.response);
      case DioExceptionType.cancel:
        return AppException(message: 'Request was cancelled.');
      case DioExceptionType.connectionError:
        return AppException(message: 'No internet connection.');
      case DioExceptionType.unknown:
        return AppException(message: 'An unexpected error occurred.');
      case DioExceptionType.badCertificate:
        return AppException(message: 'Certificate verification failed.');
      case DioExceptionType.transformTimeout:
        return AppException(message: 'Request timeout. Please try again.');
    }
  }

  static AppException _handleBadResponse(Response? response) {
    if (response == null) {
      return AppException(message: 'No response from server.');
    }

    final statusCode = response.statusCode;
    final data = response.data;

    String message;
    switch (statusCode) {
      case 400:
        message = data is Map ? (data['detail'] ?? data['message'] ?? 'Bad request') : 'Bad request';
        break;
      case 401:
        message = 'Invalid email or password';
        break;
      case 403:
        message = 'Access denied';
        break;
      case 404:
        message = 'Resource not found';
        break;
      case 422:
        message = data is Map ? (data['detail'] ?? 'Validation error') : 'Validation error';
        break;
      case 429:
        message = 'Too many requests. Please try again later.';
        break;
      case 500:
        message = 'Internal server error';
        break;
      default:
        message = data is Map ? (data['detail'] ?? 'Server error') : 'Server error';
    }

    return AppException(message: message, statusCode: statusCode, data: data);
  }
}
