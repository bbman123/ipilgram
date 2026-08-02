import 'package:dio/dio.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/personalized_announcement.dart';

class AnnouncementRepository {
  final Dio _dio;

  AnnouncementRepository(this._dio);

  Future<List<PersonalizedAnnouncement>> getMyAnnouncements() async {
    final response = await _dio.get(ApiConstants.myAnnouncementsEndpoint);
    final data = response.data;
    final List items = data is Map<String, dynamic> && data.containsKey('data')
        ? data['data'] as List
        : data as List;
    return items
        .map((e) => PersonalizedAnnouncement.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
