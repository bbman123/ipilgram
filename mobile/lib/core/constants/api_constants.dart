class ApiConstants {
  ApiConstants._();

  static const String baseUrl = 'https://ipilgram.onrender.com/api/v1';
  static const String loginEndpoint = '/auth/login';
  static const String registerEndpoint = '/auth/register';
  static const String refreshTokenEndpoint = '/auth/refresh';
  static const String logoutEndpoint = '/auth/logout';
  static const String meEndpoint = '/auth/me';
  static const String healthEndpoint = '/health';

  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 15);
}
