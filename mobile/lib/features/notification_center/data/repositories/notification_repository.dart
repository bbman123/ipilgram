import 'package:dio/dio.dart';
import '../../../../core/constants/api_constants.dart';
import '../../../dashboard/data/models/app_notification.dart';

class NotificationRepository {
  final Dio _dio;

  NotificationRepository(this._dio);

  Future<List<AppNotification>> getMyNotifications() async {
    final response = await _dio.get(ApiConstants.myNotificationsEndpoint);
    final data = response.data;
    final List items = data is Map<String, dynamic> && data.containsKey('data')
        ? data['data'] as List
        : data as List;
    return items
        .map((e) => AppNotification.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<void> markAsRead(int notificationId) async {
    await _dio.patch('/notifications/$notificationId/read');
  }
}
