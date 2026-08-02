import 'package:dio/dio.dart';
import '../../../../core/constants/constants.dart';
import '../../../../core/errors/app_exception.dart';
import '../models/models.dart';

class DashboardRepository {
  final Dio _dio;

  DashboardRepository(this._dio);

  Future<DashboardData> getDashboardData() async {
    try {
      final results = await Future.wait([
        _dio.get(ApiConstants.myPackageEndpoint),
        _dio.get(ApiConstants.myNotificationsEndpoint),
        _dio.get(ApiConstants.myAnnouncementsEndpoint),
      ]);

      final packageBody = results[0].data as Map<String, dynamic>;
      final packageData = packageBody['data'] as Map<String, dynamic>;

      Flight? flight;
      if (packageData['flight'] != null) {
        flight = Flight.fromJson(packageData['flight'] as Map<String, dynamic>);
      }

      Accommodation? accommodation;
      if (packageData['accommodation'] != null) {
        accommodation = Accommodation.fromJson(packageData['accommodation'] as Map<String, dynamic>);
      }

      Transport? transport;
      if (packageData['transport'] != null) {
        transport = Transport.fromJson(packageData['transport'] as Map<String, dynamic>);
      }

      final notifBody = results[1].data as Map<String, dynamic>;
      final notifData = notifBody['data'] as List;
      final notifications = notifData
          .map((e) => AppNotification.fromJson(e as Map<String, dynamic>))
          .toList();

      final annBody = results[2].data as Map<String, dynamic>;
      final annData = annBody['data'] as List;
      final announcements = annData
          .map((e) => Announcement.fromJson(e as Map<String, dynamic>))
          .toList();

      return DashboardData(
        flight: flight,
        accommodation: accommodation,
        transport: transport,
        notifications: notifications,
        announcements: announcements,
      );
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }
}

class DashboardData {
  final Flight? flight;
  final Accommodation? accommodation;
  final Transport? transport;
  final List<AppNotification> notifications;
  final List<Announcement> announcements;

  const DashboardData({
    this.flight,
    this.accommodation,
    this.transport,
    this.notifications = const [],
    this.announcements = const [],
  });
}
