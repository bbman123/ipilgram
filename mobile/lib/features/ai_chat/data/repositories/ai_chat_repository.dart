import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import '../../../../core/errors/app_exception.dart';

class AiChatMessage {
  final String id;
  final String text;
  final bool isUser;
  final String? audioUrl;
  final DateTime timestamp;

  const AiChatMessage({
    required this.id,
    required this.text,
    required this.isUser,
    this.audioUrl,
    required this.timestamp,
  });
}

class AiChatRepository {
  final Dio _dio;

  AiChatRepository(this._dio);

  Future<Map<String, dynamic>> ask(String query) async {
    try {
      final response = await _dio.post(
        '/personalize/ask',
        data: {'query': query},
      );
      final data = response.data;
      final Map<String, dynamic> resultData =
          data is Map<String, dynamic> && data.containsKey('data')
              ? data['data'] as Map<String, dynamic>
              : data as Map<String, dynamic>;
      return resultData;
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<String> askAudio(String query) async {
    try {
      final response = await _dio.post(
        '/personalize/ask/audio',
        data: {'query': query},
        options: Options(responseType: ResponseType.bytes),
      );
      final bytes = response.data as List<int>;
      final dir = await getTemporaryDirectory();
      final filename = 'ai_audio_${DateTime.now().millisecondsSinceEpoch}.mp3';
      final file = File('${dir.path}/$filename');
      await file.writeAsBytes(bytes);
      return file.path;
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }
}
