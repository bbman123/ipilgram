import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../data/models/personalized_announcement.dart';
import '../providers/announcement_provider.dart';

class AnnouncementsScreen extends ConsumerStatefulWidget {
  const AnnouncementsScreen({super.key});

  @override
  ConsumerState<AnnouncementsScreen> createState() => _AnnouncementsScreenState();
}

class _AnnouncementsScreenState extends ConsumerState<AnnouncementsScreen> {
  final _searchController = TextEditingController();
  final _searchFocus = FocusNode();
  bool _showSearch = false;
  final Set<int> _readIds = {};

  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(announcementProvider.notifier).load());
  }

  @override
  void dispose() {
    _searchController.dispose();
    _searchFocus.dispose();
    super.dispose();
  }

  void _toggleSearch() {
    setState(() {
      _showSearch = !_showSearch;
      if (!_showSearch) {
        _searchController.clear();
        ref.read(announcementProvider.notifier).setSearch('');
        _searchFocus.unfocus();
      } else {
        _searchFocus.requestFocus();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(announcementProvider);
    final theme = Theme.of(context);
    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 160,
            pinned: true,
            actions: [
              IconButton(
                icon: Icon(_showSearch ? Icons.close : Icons.search),
                onPressed: _toggleSearch,
              ),
              PopupMenuButton<AnnouncementSort>(
                icon: const Icon(Icons.sort),
                onSelected: (sort) => ref.read(announcementProvider.notifier).setSort(sort),
                itemBuilder: (context) => [
                  PopupMenuItem(
                    value: AnnouncementSort.newest,
                    child: Row(
                      children: [
                        Icon(Icons.access_time, size: 18, color: state.sort == AnnouncementSort.newest ? theme.colorScheme.primary : null),
                        const SizedBox(width: 8),
                        Text('Newest First', style: TextStyle(color: state.sort == AnnouncementSort.newest ? theme.colorScheme.primary : null)),
                      ],
                    ),
                  ),
                  PopupMenuItem(
                    value: AnnouncementSort.priority,
                    child: Row(
                      children: [
                        Icon(Icons.priority_high, size: 18, color: state.sort == AnnouncementSort.priority ? theme.colorScheme.primary : null),
                        const SizedBox(width: 8),
                        Text('By Priority', style: TextStyle(color: state.sort == AnnouncementSort.priority ? theme.colorScheme.primary : null)),
                      ],
                    ),
                  ),
                ],
              ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('Announcements'),
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.blue.shade700,
                      Colors.blue.shade500,
                      Colors.blue.shade300,
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
                      child: Icon(
                        Icons.campaign,
                        size: 140,
                        color: Colors.white.withValues(alpha: 0.08),
                      ),
                    ),
                    Center(
                      child: Icon(
                        Icons.campaign,
                        size: 70,
                        color: Colors.white.withValues(alpha: 0.12),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          if (_showSearch)
            SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.symmetric(
                  horizontal: isWide ? size.width * 0.15 : 16,
                  vertical: 12,
                ),
                child: TextField(
                  controller: _searchController,
                  focusNode: _searchFocus,
                  decoration: InputDecoration(
                    hintText: 'Search announcements...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              ref.read(announcementProvider.notifier).setSearch('');
                            },
                          )
                        : null,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
                  ),
                  onChanged: (v) => ref.read(announcementProvider.notifier).setSearch(v),
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
                              Text('Failed to load announcements', style: theme.textTheme.titleMedium),
                              const SizedBox(height: 8),
                              FilledButton.icon(
                                onPressed: () => ref.read(announcementProvider.notifier).load(),
                                icon: const Icon(Icons.refresh),
                                label: const Text('Retry'),
                              ),
                            ],
                          ),
                        ),
                      )
                    : state.announcements.isEmpty
                        ? SliverFillRemaining(
                            child: Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.campaign_outlined, size: 64, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
                                  const SizedBox(height: 12),
                                  Text(
                                    _searchController.text.isNotEmpty
                                        ? 'No announcements match your search'
                                        : 'No announcements yet',
                                    style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                                  ),
                                ],
                              ),
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: () => ref.read(announcementProvider.notifier).load(),
                            child: SliverList.separated(
                              itemCount: state.announcements.length,
                              separatorBuilder: (_, __) => const SizedBox(height: 8),
                              itemBuilder: (context, index) {
                                final a = state.announcements[index];
                                final isRead = _readIds.contains(a.id);
                                return _AnnouncementCard(
                                  announcement: a,
                                  isRead: isRead,
                                  onTap: () => setState(() => _readIds.add(a.id)),
                                );
                              },
                            ),
                          ),
          ),
          const SliverToBoxAdapter(child: SizedBox(height: 80)),
        ],
      ),
    );
  }
}

class _AnnouncementCard extends StatelessWidget {
  final PersonalizedAnnouncement announcement;
  final bool isRead;
  final VoidCallback onTap;

  const _AnnouncementCard({
    required this.announcement,
    required this.isRead,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final priorityColor = _priorityColor(announcement.priority);
    final priorityIcon = _priorityIcon(announcement.priority);
    final isExpired = announcement.expiryDate != null &&
        announcement.expiryDate!.isBefore(DateTime.now().toUtc());
    final isUpcoming = announcement.publishDate != null &&
        announcement.publishDate!.isAfter(DateTime.now().toUtc());

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(
                color: isRead ? Colors.grey.shade300 : priorityColor,
                width: 4,
              ),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(6),
                      decoration: BoxDecoration(
                        color: priorityColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(priorityIcon, size: 18, color: priorityColor),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            announcement.title,
                            style: theme.textTheme.titleSmall?.copyWith(
                              fontWeight: isRead ? FontWeight.normal : FontWeight.bold,
                            ),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 2),
                          Row(
                            children: [
                              _StatusChip(
                                label: announcement.priority.toUpperCase(),
                                color: priorityColor,
                              ),
                              if (isExpired) ...[
                                const SizedBox(width: 6),
                                _StatusChip(label: 'EXPIRED', color: Colors.red),
                              ],
                              if (isUpcoming) ...[
                                const SizedBox(width: 6),
                                _StatusChip(label: 'UPCOMING', color: Colors.orange),
                              ],
                              if (announcement.simplified) ...[
                                const SizedBox(width: 6),
                                _StatusChip(label: 'AI', color: Colors.teal),
                              ],
                            ],
                          ),
                        ],
                      ),
                    ),
                    if (!isRead)
                      Container(
                        width: 10,
                        height: 10,
                        decoration: BoxDecoration(
                          color: priorityColor,
                          shape: BoxShape.circle,
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  announcement.message,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                  maxLines: 4,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    Icon(Icons.access_time, size: 14, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                    const SizedBox(width: 4),
                    Text(
                      _formatDate(announcement.publishDate),
                      style: theme.textTheme.labelSmall?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6),
                      ),
                    ),
                    const Spacer(),
                    if (announcement.language != 'English')
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.indigo.withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          announcement.language,
                          style: theme.textTheme.labelSmall?.copyWith(color: Colors.indigo),
                        ),
                      ),
                    if (announcement.audioUrl != null) ...[
                      const SizedBox(width: 6),
                      Icon(Icons.headset, size: 14, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                    ],
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Color _priorityColor(String priority) {
    switch (priority.toLowerCase()) {
      case 'critical': return Colors.red;
      case 'high': return Colors.orange;
      case 'medium': return Colors.blue;
      case 'low': return Colors.green;
      default: return Colors.grey;
    }
  }

  IconData _priorityIcon(String priority) {
    switch (priority.toLowerCase()) {
      case 'critical': return Icons.error;
      case 'high': return Icons.warning;
      case 'medium': return Icons.info;
      case 'low': return Icons.notifications;
      default: return Icons.campaign;
    }
  }

  String _formatDate(DateTime? date) {
    if (date == null) return '';
    final now = DateTime.now().toUtc();
    final diff = now.difference(date.toUtc());
    if (diff.inMinutes < 1) return 'Just now';
    if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
    if (diff.inHours < 24) return '${diff.inHours}h ago';
    if (diff.inDays < 7) return '${diff.inDays}d ago';
    return DateFormat('MMM d, yyyy').format(date.toUtc());
  }
}

class _StatusChip extends StatelessWidget {
  final String label;
  final Color color;

  const _StatusChip({required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 9,
          fontWeight: FontWeight.w700,
          color: color,
          letterSpacing: 0.5,
        ),
      ),
    );
  }
}
