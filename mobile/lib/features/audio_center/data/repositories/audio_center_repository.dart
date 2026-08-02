import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import '../../../../core/constants/api_constants.dart';

class AudioItem {
  final String id;
  final String title;
  final String subtitle;
  final String audioUrl;
  final String? localPath;
  final bool isDownloaded;
  final DateTime? createdAt;

  const AudioItem({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.audioUrl,
    this.localPath,
    this.isDownloaded = false,
    this.createdAt,
  });

  AudioItem copyWith({String? localPath, bool? isDownloaded}) {
    return AudioItem(
      id: id,
      title: title,
      subtitle: subtitle,
      audioUrl: audioUrl,
      localPath: localPath ?? this.localPath,
      isDownloaded: isDownloaded ?? this.isDownloaded,
      createdAt: createdAt,
    );
  }
}

class AudioCenterRepository {
  final Dio _dio;

  AudioCenterRepository(this._dio);

  Future<List<AudioItem>> getAnnouncementAudios() async {
    final response = await _dio.get(ApiConstants.myAnnouncementsEndpoint);
    final data = response.data;
    final List items = data is Map<String, dynamic> && data.containsKey('data')
        ? data['data'] as List
        : data as List;

    final dir = await getApplicationDocumentsDirectory();
    final audioDir = Directory('${dir.path}/audio');
    if (!await audioDir.exists()) {
      await audioDir.create(recursive: true);
    }

    return items
        .where((e) => e['audio_url'] != null && (e['audio_url'] as String).isNotEmpty)
        .map((e) {
      final audioUrl = e['audio_url'] as String;
      final filename = audioUrl.split('/').last;
      final localFile = File('${audioDir.path}/$filename');
      return AudioItem(
        id: 'ann_${e['id']}',
        title: e['title'] ?? 'Announcement',
        subtitle: e['message'] ?? '',
        audioUrl: audioUrl.startsWith('http') ? audioUrl : '${ApiConstants.baseUrl}$audioUrl',
        localPath: localFile.existsSync() ? localFile.path : null,
        isDownloaded: localFile.existsSync(),
        createdAt: e['publish_date'] != null ? DateTime.tryParse(e['publish_date']) : null,
      );
    }).toList();
  }

  Future<String> downloadAudio(String url, String filename) async {
    final dir = await getApplicationDocumentsDirectory();
    final audioDir = Directory('${dir.path}/audio');
    if (!await audioDir.exists()) {
      await audioDir.create(recursive: true);
    }
    final filepath = '${audioDir.path}/$filename';
    await _dio.download(url, filepath);
    return filepath;
  }
}
