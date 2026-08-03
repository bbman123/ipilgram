import 'dart:async';
import 'dart:developer' as developer;
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../data/repositories/audio_center_repository.dart';

final audioCenterRepositoryProvider = Provider<AudioCenterRepository>((ref) {
  final dio = ref.watch(dioClientProvider).dio;
  return AudioCenterRepository(dio);
});

enum AudioCategory { all, announcements }

class AudioCenterState {
  final bool isLoading;
  final List<AudioItem> allAudios;
  final AudioCategory selectedCategory;
  final AudioPlayer? player;
  final AudioItem? currentlyPlaying;
  final bool isPlaying;
  final Duration position;
  final Duration duration;
  final double playbackSpeed;
  final String? error;

  const AudioCenterState({
    this.isLoading = false,
    this.allAudios = const [],
    this.selectedCategory = AudioCategory.all,
    this.player,
    this.currentlyPlaying,
    this.isPlaying = false,
    this.position = Duration.zero,
    this.duration = Duration.zero,
    this.playbackSpeed = 1.0,
    this.error,
  });

  AudioCenterState copyWith({
    bool? isLoading,
    List<AudioItem>? allAudios,
    AudioCategory? selectedCategory,
    AudioPlayer? player,
    AudioItem? currentlyPlaying,
    bool? isPlaying,
    Duration? position,
    Duration? duration,
    double? playbackSpeed,
    String? error,
    bool clearCurrentlyPlaying = false,
  }) {
    return AudioCenterState(
      isLoading: isLoading ?? this.isLoading,
      allAudios: allAudios ?? this.allAudios,
      selectedCategory: selectedCategory ?? this.selectedCategory,
      player: player ?? this.player,
      currentlyPlaying: clearCurrentlyPlaying ? null : (currentlyPlaying ?? this.currentlyPlaying),
      isPlaying: isPlaying ?? this.isPlaying,
      position: position ?? this.position,
      duration: duration ?? this.duration,
      playbackSpeed: playbackSpeed ?? this.playbackSpeed,
      error: error,
    );
  }

  List<AudioItem> get audios {
    if (selectedCategory == AudioCategory.all) return allAudios;
    return allAudios;
  }
}

class AudioCenterNotifier extends StateNotifier<AudioCenterState> {
  final AudioCenterRepository _repo;
  AudioPlayer? _player;
  StreamSubscription? _positionSub;
  StreamSubscription? _durationSub;
  StreamSubscription? _playerStateSub;

  AudioCenterNotifier(this._repo) : super(const AudioCenterState()) {
    debugPrint('[AUDIO_DIAG] Provider: Initializing AudioCenterNotifier');
    _player = AudioPlayer();
    _initPlayer();
    debugPrint('[AUDIO_DIAG] Provider: AudioCenterNotifier initialized successfully');
  }

  void _initPlayer() {
    debugPrint('[AUDIO_DIAG] Provider: Initializing AudioPlayer');
    _player = AudioPlayer();
    _positionSub = _player!.positionStream.listen((pos) {
      if (mounted) state = state.copyWith(position: pos);
    });
    _durationSub = _player!.durationStream.listen((dur) {
      debugPrint('[AUDIO_DIAG] Provider: Duration stream event: duration=${dur?.inMilliseconds}ms');
      if (mounted) state = state.copyWith(duration: dur ?? Duration.zero);
    });
    _playerStateSub = _player!.playerStateStream.listen((playerState) {
      debugPrint('[AUDIO_DIAG] Provider: Player state changed: playing=${playerState.playing}, processingState=${playerState.processingState}');
      if (mounted) {
        state = state.copyWith(
          isPlaying: playerState.playing,
          clearCurrentlyPlaying: playerState.processingState == ProcessingState.completed,
          position: playerState.processingState == ProcessingState.completed ? Duration.zero : state.position,
        );
      }
    });
    debugPrint('[AUDIO_DIAG] Provider: AudioPlayer initialized and streams subscribed');
  }

  Future<void> load() async {
    debugPrint('[AUDIO_DIAG] Provider: Loading audio items');
    state = state.copyWith(isLoading: true, error: null);
    try {
      final items = await _repo.getAnnouncementAudios();
      debugPrint('[AUDIO_DIAG] Provider: Loaded ${items.length} audio items successfully');
      state = state.copyWith(isLoading: false, allAudios: items, error: null);
    } catch (e, stackTrace) {
      debugPrint('[AUDIO_DIAG] Provider: Load FAILED');
      debugPrint('[AUDIO_DIAG] Provider: Error: $e');
      debugPrint('[AUDIO_DIAG] Provider: Stack trace: $stackTrace');
      state = state.copyWith(
        isLoading: false,
        allAudios: [],
        error: e.toString(),
      );
    }
  }

  Future<void> play(AudioItem item) async {
    try {
      debugPrint('[AUDIO_DIAG] Provider: Playing audio item: id=${item.id}, title=${item.title}');
      debugPrint('[AUDIO_DIAG] Provider:   - audioUrl=${item.audioUrl}');
      debugPrint('[AUDIO_DIAG] Provider:   - localPath=${item.localPath}');

      final source = item.localPath != null
          ? AudioSource.file(item.localPath!)
          : AudioSource.uri(Uri.parse(item.audioUrl));

      debugPrint('[AUDIO_DIAG] Provider: Audio source created: ${source.runtimeType}');
      debugPrint('[AUDIO_DIAG] Provider: Initializing player...');
      await _player!.setAudioSource(source);
      debugPrint('[AUDIO_DIAG] Provider: Player initialized, starting playback...');
      await _player!.play();
      debugPrint('[AUDIO_DIAG] Provider: Playback started successfully');
      state = state.copyWith(currentlyPlaying: item, isPlaying: true);
    } catch (e, stackTrace) {
      debugPrint('[AUDIO_DIAG] Provider: Playback FAILED');
      debugPrint('[AUDIO_DIAG] Provider: Error: $e');
      debugPrint('[AUDIO_DIAG] Provider: Stack trace: $stackTrace');
      state = state.copyWith(error: 'Failed to play audio');
    }
  }

  Future<void> togglePlayPause() async {
    if (_player == null) {
      debugPrint('[AUDIO_DIAG] Provider: togglePlayPause called but player is null');
      return;
    }
    if (state.isPlaying) {
      debugPrint('[AUDIO_DIAG] Provider: Pausing playback');
      await _player!.pause();
    } else if (state.currentlyPlaying != null) {
      debugPrint('[AUDIO_DIAG] Provider: Resuming playback');
      await _player!.play();
    }
  }

  Future<void> seek(Duration position) async {
    debugPrint('[AUDIO_DIAG] Provider: Seeking to position=${position.inMilliseconds}ms');
    await _player?.seek(position);
  }

  Future<void> setSpeed(double speed) async {
    await _player?.setSpeed(speed);
    state = state.copyWith(playbackSpeed: speed);
  }

  Future<void> download(AudioItem item) async {
    try {
      final filename = '${item.id}.mp3';
      debugPrint('[AUDIO_DIAG] Provider: Downloading audio: id=${item.id}, filename=$filename');
      debugPrint('[AUDIO_DIAG] Provider:   - audioUrl=${item.audioUrl}');
      final localPath = await _repo.downloadAudio(item.audioUrl, filename);
      debugPrint('[AUDIO_DIAG] Provider: Download complete: localPath=$localPath');
      state = state.copyWith(
        allAudios: state.allAudios.map((a) {
          if (a.id == item.id) {
            return a.copyWith(localPath: localPath, isDownloaded: true);
          }
          return a;
        }).toList(),
      );
    } catch (e, stackTrace) {
      debugPrint('[AUDIO_DIAG] Provider: Download FAILED');
      debugPrint('[AUDIO_DIAG] Provider: Error: $e');
      debugPrint('[AUDIO_DIAG] Provider: Stack trace: $stackTrace');
      state = state.copyWith(error: 'Download failed');
    }
  }

  void setCategory(AudioCategory cat) {
    state = state.copyWith(selectedCategory: cat);
  }

  @override
  void dispose() {
    _positionSub?.cancel();
    _durationSub?.cancel();
    _playerStateSub?.cancel();
    _player?.dispose();
    super.dispose();
  }
}

final audioCenterProvider = StateNotifierProvider<AudioCenterNotifier, AudioCenterState>((ref) {
  final repo = ref.watch(audioCenterRepositoryProvider);
  return AudioCenterNotifier(repo);
});
