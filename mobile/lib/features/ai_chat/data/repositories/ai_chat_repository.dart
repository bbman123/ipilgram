import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import '../../../../core/constants/api_constants.dart';

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
    final response = await _dio.post(
      '${ApiConstants.baseUrl}/personalize/ask',
      data: {'query': query},
    );
    final data = response.data;
    final Map<String, dynamic> resultData =
        data is Map<String, dynamic> && data.containsKey('data')
            ? data['data'] as Map<String, dynamic>
            : data as Map<String, dynamic>;
    return resultData;
  }

  Future<String> askAudio(String query) async {
    final response = await _dio.post(
      '${ApiConstants.baseUrl}/personalize/ask/audio',
      data: {'query': query},
      options: Options(responseType: ResponseType.bytes),
    );
    final bytes = response.data as List<int>;
    final dir = await getTemporaryDirectory();
    final filename = 'ai_audio_${DateTime.now().millisecondsSinceEpoch}.mp3';
    final file = File('${dir.path}/$filename');
    await file.writeAsBytes(bytes);
    return file.path;
  }
}
