import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../data/repositories/audio_center_repository.dart';
import '../providers/audio_center_provider.dart';

class AudioCenterScreen extends ConsumerStatefulWidget {
  const AudioCenterScreen({super.key});

  @override
  ConsumerState<AudioCenterScreen> createState() => _AudioCenterScreenState();
}

class _AudioCenterScreenState extends ConsumerState<AudioCenterScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(audioCenterProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(audioCenterProvider);
    final theme = Theme.of(context);
    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return Scaffold(
      body: Column(
        children: [
          Expanded(
            child: RefreshIndicator(
              onRefresh: () => ref.read(audioCenterProvider.notifier).load(),
              child: CustomScrollView(
                slivers: [
                  SliverAppBar(
                    expandedHeight: 160,
                    pinned: true,
                    flexibleSpace: FlexibleSpaceBar(
                      title: const Text('Audio Center'),
                      background: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Colors.deepPurple.shade700,
                              Colors.deepPurple.shade500,
                              Colors.purple.shade300,
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: Stack(
                          children: [
                            Positioned(
                              right: -30,
                              bottom: -30,
                              child: Icon(Icons.headphones, size: 140, color: Colors.white.withValues(alpha: 0.08)),
                            ),
                            Center(
                              child: Icon(Icons.headphones, size: 70, color: Colors.white.withValues(alpha: 0.12)),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  SliverPadding(
                    padding: EdgeInsets.symmetric(
                      horizontal: isWide ? size.width * 0.15 : 12,
                      vertical: 8,
                    ),
                    sliver: state.isLoading
                        ? const SliverFillRemaining(
                            child: Center(child: CircularProgressIndicator()),
                          )
                        : state.error != null
                            ? SliverFillRemaining(
                                child: Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(Icons.error_outline, size: 56, color: theme.colorScheme.error),
                                      const SizedBox(height: 12),
                                      Text('Failed to load audio', style: theme.textTheme.titleMedium),
                                      const SizedBox(height: 8),
                                      FilledButton.icon(
                                        onPressed: () => ref.read(audioCenterProvider.notifier).load(),
                                        icon: const Icon(Icons.refresh),
                                        label: const Text('Retry'),
                                      ),
                                    ],
                                  ),
                                ),
                              )
                            : state.audios.isEmpty
                                ? SliverFillRemaining(
                                    child: Center(
                                      child: Column(
                                        mainAxisAlignment: MainAxisAlignment.center,
                                        children: [
                                          Icon(Icons.headset_off, size: 64, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
                                          const SizedBox(height: 12),
                                          Text('No audio available', style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                                          const SizedBox(height: 4),
                                          Text(
                                            'Audio will appear when announcements have audio files',
                                            style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                                            textAlign: TextAlign.center,
                                          ),
                                        ],
                                      ),
                                    ),
                                  )
                                : SliverList.separated(
                                    itemCount: state.audios.length,
                                    separatorBuilder: (_, __) => const SizedBox(height: 8),
                                    itemBuilder: (context, index) {
                                      final audio = state.audios[index];
                                      final isPlaying = state.currentlyPlaying?.id == audio.id;
                                      return _AudioCard(
                                        audio: audio,
                                        isPlaying: isPlaying,
                                        onTap: () => ref.read(audioCenterProvider.notifier).play(audio),
                                        onDownload: () => ref.read(audioCenterProvider.notifier).download(audio),
                                      );
                                    },
                                  ),
                  ),
                  const SliverToBoxAdapter(child: SizedBox(height: 160)),
                ],
              ),
            ),
          ),
          if (state.currentlyPlaying != null)
            _NowPlayingBar(state: state),
        ],
      ),
    );
  }
}

class _AudioCard extends StatelessWidget {
  final AudioItem audio;
  final bool isPlaying;
  final VoidCallback onTap;
  final VoidCallback onDownload;

  const _AudioCard({
    required this.audio,
    required this.isPlaying,
    required this.onTap,
    required this.onDownload,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(
                color: isPlaying ? Colors.deepPurple : Colors.transparent,
                width: 4,
              ),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: isPlaying
                          ? [Colors.deepPurple, Colors.purple]
                          : [Colors.grey.shade300, Colors.grey.shade200],
                    ),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    isPlaying ? Icons.pause : Icons.play_arrow,
                    color: isPlaying ? Colors.white : Colors.grey.shade600,
                    size: 28,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        audio.title,
                        style: TextStyle(
                          fontWeight: isPlaying ? FontWeight.bold : FontWeight.w600,
                          color: isPlaying ? Colors.deepPurple : null,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 2),
                      Text(
                        audio.subtitle,
                        style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Icon(Icons.access_time, size: 12, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                          const SizedBox(width: 3),
                          Text(
                            audio.createdAt != null ? DateFormat('MMM d, HH:mm').format(audio.createdAt!) : '',
                            style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                if (audio.isDownloaded)
                  Icon(Icons.download_done, color: Colors.green, size: 20)
                else
                  IconButton(
                    icon: Icon(Icons.download, color: theme.colorScheme.primary, size: 22),
                    onPressed: onDownload,
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _NowPlayingBar extends ConsumerWidget {
  final AudioCenterState state;

  const _NowPlayingBar({required this.state});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifier = ref.read(audioCenterProvider.notifier);
    final progress = state.duration.inMilliseconds > 0
        ? state.position.inMilliseconds / state.duration.inMilliseconds
        : 0.0;

    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.deepPurple.shade800, Colors.deepPurple.shade600],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 12, offset: const Offset(0, -4)),
        ],
      ),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 10, 16, 0),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.music_note, color: Colors.white, size: 22),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          state.currentlyPlaying?.title ?? '',
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 13),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        Text(
                          state.currentlyPlaying?.subtitle ?? '',
                          style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 11),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                  _SpeedButton(
                    speed: state.playbackSpeed,
                    onSpeedChange: (s) => notifier.setSpeed(s),
                  ),
                ],
              ),
            ),
            SliderTheme(
              data: SliderTheme.of(context).copyWith(
                activeTrackColor: Colors.white,
                inactiveTrackColor: Colors.white.withValues(alpha: 0.2),
                thumbColor: Colors.white,
                thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                trackHeight: 3,
                overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
              ),
              child: Slider(
                value: progress.clamp(0.0, 1.0),
                onChanged: (v) {
                  final pos = Duration(milliseconds: (v * state.duration.inMilliseconds).round());
                  notifier.seek(pos);
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 6),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    _formatDuration(state.position),
                    style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 11),
                  ),
                  Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.replay_10, color: Colors.white, size: 26),
                        onPressed: () => notifier.seek(Duration(seconds: (state.position.inSeconds - 10).clamp(0, state.duration.inSeconds))),
                      ),
                      Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                        ),
                        child: IconButton(
                          icon: Icon(
                            state.isPlaying ? Icons.pause : Icons.play_arrow,
                            color: Colors.deepPurple,
                            size: 28,
                          ),
                          onPressed: () => notifier.togglePlayPause(),
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.forward_10, color: Colors.white, size: 26),
                        onPressed: () => notifier.seek(Duration(seconds: (state.position.inSeconds + 10).clamp(0, state.duration.inSeconds))),
                      ),
                    ],
                  ),
                  Text(
                    _formatDuration(state.duration),
                    style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 11),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration d) {
    final min = d.inMinutes.remainder(60).toString().padLeft(2, '0');
    final sec = d.inSeconds.remainder(60).toString().padLeft(2, '0');
    return '$min:$sec';
  }
}

class _SpeedButton extends StatelessWidget {
  final double speed;
  final ValueChanged<double> onSpeedChange;

  const _SpeedButton({required this.speed, required this.onSpeedChange});

  @override
  Widget build(BuildContext context) {
    final speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];
    return GestureDetector(
      onTap: () {
        showModalBottomSheet(
          context: context,
          builder: (ctx) => Container(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('Playback Speed', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                ...speeds.map((s) => ListTile(
                      title: Text('${s}x'),
                      trailing: s == speed ? Icon(Icons.check, color: Colors.deepPurple) : null,
                      onTap: () {
                        onSpeedChange(s);
                        Navigator.pop(ctx);
                      },
                    )),
              ],
            ),
          ),
        );
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.15),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          '${speed}x',
          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }
}
