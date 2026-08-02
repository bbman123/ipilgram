import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../dashboard/data/models/app_notification.dart';
import '../providers/notification_center_provider.dart';

class NotificationCenterScreen extends ConsumerStatefulWidget {
  const NotificationCenterScreen({super.key});

  @override
  ConsumerState<NotificationCenterScreen> createState() => _NotificationCenterScreenState();
}

class _NotificationCenterScreenState extends ConsumerState<NotificationCenterScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(notificationCenterProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(notificationCenterProvider);
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
              if (state.unreadCount > 0)
                Center(
                  child: Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: Text(
                      '${state.unreadCount} unread',
                      style: theme.textTheme.labelMedium?.copyWith(color: Colors.white70),
                    ),
                  ),
                ),
            ],
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('Notifications'),
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.indigo.shade700,
                      Colors.indigo.shade500,
                      Colors.indigo.shade300,
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
                        Icons.notifications,
                        size: 140,
                        color: Colors.white.withValues(alpha: 0.08),
                      ),
                    ),
                    Center(
                      child: Icon(
                        Icons.notifications,
                        size: 70,
                        color: Colors.white.withValues(alpha: 0.12),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: _CategoryTabs(
              selected: state.selectedCategory,
              unreadCounts: {
                for (final cat in NotificationCategory.values)
                  cat: state.unreadCountFor(cat),
              },
              onSelect: (cat) => ref.read(notificationCenterProvider.notifier).setCategory(cat),
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
                              Text('Failed to load notifications', style: theme.textTheme.titleMedium),
                              const SizedBox(height: 8),
                              FilledButton.icon(
                                onPressed: () => ref.read(notificationCenterProvider.notifier).load(),
                                icon: const Icon(Icons.refresh),
                                label: const Text('Retry'),
                              ),
                            ],
                          ),
                        ),
                      )
                    : state.notifications.isEmpty
                        ? SliverFillRemaining(
                            child: Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.notifications_none, size: 64, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
                                  const SizedBox(height: 12),
                                  Text(
                                    'No notifications',
                                    style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                                  ),
                                ],
                              ),
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: () => ref.read(notificationCenterProvider.notifier).load(),
                            child: SliverList.separated(
                              itemCount: state.notifications.length,
                              separatorBuilder: (_, __) => const SizedBox(height: 8),
                              itemBuilder: (context, index) {
                                final n = state.notifications[index];
                                return _NotificationTile(
                                  notification: n,
                                  onRead: () => ref.read(notificationCenterProvider.notifier).markAsRead(n.id),
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

class _CategoryTabs extends StatelessWidget {
  final NotificationCategory selected;
  final Map<NotificationCategory, int> unreadCounts;
  final ValueChanged<NotificationCategory> onSelect;

  const _CategoryTabs({
    required this.selected,
    required this.unreadCounts,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final categories = NotificationCategory.values;

    return SizedBox(
      height: 56,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        itemCount: categories.length,
        separatorBuilder: (_, __) => const SizedBox(width: 8),
        itemBuilder: (context, index) {
          final cat = categories[index];
          final isSelected = cat == selected;
          final unread = unreadCounts[cat] ?? 0;

          return GestureDetector(
            onTap: () => onSelect(cat),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: const EdgeInsets.symmetric(horizontal: 14),
              decoration: BoxDecoration(
                color: isSelected
                    ? theme.colorScheme.primary
                    : theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: isSelected
                      ? theme.colorScheme.primary
                      : theme.colorScheme.outline.withValues(alpha: 0.2),
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    _categoryIcon(cat),
                    size: 16,
                    color: isSelected ? Colors.white : theme.colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    _categoryLabel(cat),
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                      color: isSelected ? Colors.white : theme.colorScheme.onSurfaceVariant,
                    ),
                  ),
                  if (unread > 0) ...[
                    const SizedBox(width: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? Colors.white.withValues(alpha: 0.25)
                            : theme.colorScheme.error,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        '$unread',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: isSelected ? Colors.white : Colors.white,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  String _categoryLabel(NotificationCategory cat) {
    switch (cat) {
      case NotificationCategory.all:
        return 'All';
      case NotificationCategory.flight:
        return 'Flight';
      case NotificationCategory.accommodation:
        return 'Hotel';
      case NotificationCategory.transport:
        return 'Transport';
      case NotificationCategory.general:
        return 'General';
    }
  }

  IconData _categoryIcon(NotificationCategory cat) {
    switch (cat) {
      case NotificationCategory.all:
        return Icons.all_inclusive;
      case NotificationCategory.flight:
        return Icons.flight;
      case NotificationCategory.accommodation:
        return Icons.hotel;
      case NotificationCategory.transport:
        return Icons.directions_bus;
      case NotificationCategory.general:
        return Icons.info_outline;
    }
  }
}

class _NotificationTile extends StatelessWidget {
  final AppNotification notification;
  final VoidCallback onRead;

  const _NotificationTile({required this.notification, required this.onRead});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isRead = notification.readAt != null;
    final color = _typeColor(notification.notificationType);
    final icon = _typeIcon(notification.notificationType);

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: isRead ? null : onRead,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(
                color: isRead ? Colors.grey.shade200 : color,
                width: 4,
              ),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: isRead
                        ? Colors.grey.withValues(alpha: 0.08)
                        : color.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(
                    icon,
                    color: isRead ? Colors.grey : color,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              notification.title,
                              style: TextStyle(
                                fontWeight: isRead ? FontWeight.normal : FontWeight.w600,
                                fontSize: 14,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (!isRead)
                            Container(
                              width: 8,
                              height: 8,
                              decoration: BoxDecoration(
                                color: theme.colorScheme.primary,
                                shape: BoxShape.circle,
                              ),
                            ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        notification.message,
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          _TypeChip(label: _typeLabel(notification.notificationType), color: color),
                          const Spacer(),
                          Text(
                            _formatTime(notification.createdAt),
                            style: theme.textTheme.labelSmall?.copyWith(
                              color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6),
                            ),
                          ),
                        ],
                      ),
                      if (notification.audioUrl != null) ...[
                        const SizedBox(height: 6),
                        Row(
                          children: [
                            Icon(Icons.headset, size: 14, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
                            const SizedBox(width: 4),
                            Text(
                              'Audio available',
                              style: theme.textTheme.labelSmall?.copyWith(
                                color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  String _typeLabel(String type) {
    switch (type) {
      case 'flight':
        return 'Flight';
      case 'accommodation':
        return 'Hotel';
      case 'transport':
        return 'Transport';
      default:
        return 'General';
    }
  }

  Color _typeColor(String type) {
    switch (type) {
      case 'flight':
        return Colors.blue;
      case 'accommodation':
        return Colors.teal;
      case 'transport':
        return Colors.purple;
      default:
        return Colors.orange;
    }
  }

  IconData _typeIcon(String type) {
    switch (type) {
      case 'flight':
        return Icons.flight;
      case 'accommodation':
        return Icons.hotel;
      case 'transport':
        return Icons.directions_bus;
      default:
        return Icons.notifications;
    }
  }

  String _formatTime(DateTime? date) {
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

class _TypeChip extends StatelessWidget {
  final String label;
  final Color color;

  const _TypeChip({required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.w600,
          color: color,
        ),
      ),
    );
  }
}
