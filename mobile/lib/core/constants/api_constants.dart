class ApiConstants {
  ApiConstants._();

  static const String baseUrl = 'https://ipilgram.onrender.com/api/v1';
  static const String loginEndpoint = '/auth/login';
  static const String registerEndpoint = '/auth/register';
  static const String refreshTokenEndpoint = '/auth/refresh';
  static const String logoutEndpoint = '/auth/logout';
  static const String meEndpoint = '/auth/me';
  static const String healthEndpoint = '/health';

  static const String flightsEndpoint = '/flights';
  static const String accommodationsEndpoint = '/accommodations';
  static const String transportsEndpoint = '/transports';
  static const String myNotificationsEndpoint = '/notifications/my';
  static const String myAnnouncementsEndpoint = '/announcements/my';
  static const String myPackageEndpoint = '/packages/my';

  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 15);
}
