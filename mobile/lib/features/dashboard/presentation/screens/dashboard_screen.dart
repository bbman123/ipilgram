import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../../accommodation/presentation/providers/accommodation_provider.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../flight/presentation/providers/flight_provider.dart';
import '../../../transport/presentation/providers/transport_provider.dart';
import '../providers/dashboard_provider.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen>
    with TickerProviderStateMixin {
  late final AnimationController _staggerController;
  late final List<Animation<double>> _fadeAnimations;
  late final List<Animation<Offset>> _slideAnimations;

  @override
  void initState() {
    super.initState();
    _staggerController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    );

    _fadeAnimations = List.generate(8, (i) {
      final start = (i * 0.1).clamp(0.0, 0.7);
      final end = (start + 0.3).clamp(0.0, 1.0);
      return Tween<double>(begin: 0, end: 1).animate(
        CurvedAnimation(parent: _staggerController, curve: Interval(start, end, curve: Curves.easeOut)),
      );
    });

    _slideAnimations = List.generate(8, (i) {
      final start = (i * 0.1).clamp(0.0, 0.7);
      final end = (start + 0.3).clamp(0.0, 1.0);
      return Tween<Offset>(begin: const Offset(0, 0.15), end: Offset.zero).animate(
        CurvedAnimation(parent: _staggerController, curve: Interval(start, end, curve: Curves.easeOutCubic)),
      );
    });

    _staggerController.forward();
  }

  @override
  void dispose() {
    _staggerController.dispose();
    super.dispose();
  }

  Widget _buildAnimated(int index, Widget child) {
    return FadeTransition(
      opacity: _fadeAnimations[index],
      child: SlideTransition(
        position: _slideAnimations[index],
        child: child,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final dashState = ref.watch(dashboardProvider);
    final user = authState.user;
    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () => ref.read(dashboardProvider.notifier).loadDashboard(),
        child: CustomScrollView(
          slivers: [
            SliverAppBar(
              expandedHeight: 220,
              pinned: true,
              automaticallyImplyLeading: false,
              flexibleSpace: FlexibleSpaceBar(
                background: _WelcomeHeader(user: user, dashState: dashState),
              ),
              actions: [
                IconButton(
                  icon: const Icon(Icons.settings),
                  onPressed: () => context.push('/settings'),
                  tooltip: 'Settings',
                ),
                IconButton(
                  icon: const Icon(Icons.logout),
                  onPressed: () async {
                    await ref.read(authProvider.notifier).logout();
                    if (context.mounted) context.go('/login');
                  },
                ),
              ],
            ),
            SliverPadding(
              padding: EdgeInsets.symmetric(
                horizontal: isWide ? size.width * 0.15 : 16,
                vertical: 8,
              ),
              sliver: SliverList.list(
                children: [
                  _buildAnimated(0, _InfoCardsRow(dashState: dashState)),
                  const SizedBox(height: 16),
                  _buildAnimated(1, _NextFlightCard(dashState: dashState)),
                  const SizedBox(height: 12),
                  _buildAnimated(2, _AccommodationCard(dashState: dashState)),
                  const SizedBox(height: 12),
                  _buildAnimated(3, _TransportCard(dashState: dashState)),
                  const SizedBox(height: 16),
                  _buildAnimated(4, _SectionHeader(title: 'Quick Actions')),
                  const SizedBox(height: 8),
                  _buildAnimated(5, _QuickActionsGrid()),
                  const SizedBox(height: 16),
                  _buildAnimated(6, _SectionHeader(title: 'Recent Notifications')),
                  const SizedBox(height: 8),
                  _buildAnimated(7, _RecentNotifications(dashState: dashState)),
                  const SizedBox(height: 80),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _WelcomeHeader extends StatelessWidget {
  final dynamic user;
  final DashboardState dashState;

  const _WelcomeHeader({required this.user, required this.dashState});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            theme.colorScheme.primary,
            theme.colorScheme.primary.withValues(alpha: 0.7),
            theme.colorScheme.tertiary,
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 16, 20, 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    radius: 28,
                    backgroundColor: Colors.white.withValues(alpha: 0.2),
                    child: Text(
                      (user?.fullName ?? 'P')[0].toUpperCase(),
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Assalamu Alaikum,',
                          style: theme.textTheme.bodyMedium?.copyWith(
                            color: Colors.white.withValues(alpha: 0.85),
                          ),
                        ),
                        Text(
                          user?.fullName ?? 'Pilgrim',
                          style: theme.textTheme.titleLarge?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              if (user?.packageName != null)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    user!.packageName!,
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InfoCardsRow extends StatelessWidget {
  final DashboardState dashState;

  const _InfoCardsRow({required this.dashState});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _InfoCard(
            icon: Icons.notifications_active_outlined,
            label: 'Notifications',
            count: dashState.unreadNotifications,
            color: Colors.orange,
            onTap: () => context.push('/notifications'),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _InfoCard(
            icon: Icons.campaign_outlined,
            label: 'Announcements',
            count: dashState.unreadAnnouncements,
            color: Colors.blue,
            onTap: () => context.push('/announcements'),
          ),
        ),
      ],
    );
  }
}

class _InfoCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final int count;
  final Color color;
  final VoidCallback? onTap;

  const _InfoCard({
    required this.icon,
    required this.label,
    required this.count,
    required this.color,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              Container(
                width: 42,
                height: 42,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(icon, color: color, size: 22),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$count',
                      style: theme.textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: color,
                      ),
                    ),
                    Text(
                      label,
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _NextFlightCard extends ConsumerWidget {
  final DashboardState dashState;

  const _NextFlightCard({required this.dashState});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final flight = dashState.nextFlight;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: flight != null
            ? () {
                ref.read(selectedFlightProvider.notifier).state = flight;
                context.push('/flight');
              }
            : null,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(color: theme.colorScheme.primary, width: 4),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: flight == null
                ? Row(
                    children: [
                      Icon(Icons.flight_outlined, size: 36, color: theme.colorScheme.primary.withValues(alpha: 0.4)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Next Flight', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                            const SizedBox(height: 2),
                            Text(
                              'No upcoming flights',
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: theme.colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  )
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.flight, color: theme.colorScheme.primary, size: 20),
                          const SizedBox(width: 6),
                          Text('Next Flight', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                          const Spacer(),
                          _StatusBadge(status: flight.status),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  flight.departureAirport,
                                  style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
                                ),
                                Text(
                                  DateFormat('MMM d, HH:mm').format(flight.departureDatetime),
                                  style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                                ),
                              ],
                            ),
                          ),
                          Icon(Icons.flight_takeoff, color: theme.colorScheme.primary),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.end,
                              children: [
                                Text(
                                  flight.arrivalAirport,
                                  style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
                                ),
                                Text(
                                  DateFormat('MMM d, HH:mm').format(flight.arrivalDatetime),
                                  style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          _Chip(label: flight.airline),
                          const SizedBox(width: 6),
                          _Chip(label: flight.flightNumber),
                          if (flight.gate != null) ...[
                            const SizedBox(width: 6),
                            _Chip(label: 'Gate ${flight.gate}'),
                          ],
                          if (flight.seatNumber != null) ...[
                            const SizedBox(width: 6),
                            _Chip(label: 'Seat ${flight.seatNumber}'),
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
}

class _AccommodationCard extends ConsumerWidget {
  final DashboardState dashState;

  const _AccommodationCard({required this.dashState});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final acc = dashState.accommodation;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: acc != null
            ? () {
                ref.read(selectedAccommodationProvider.notifier).state = acc;
                context.push('/accommodation');
              }
            : null,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(color: Colors.teal, width: 4),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: acc == null
                ? Row(
                    children: [
                      Icon(Icons.hotel_outlined, size: 36, color: Colors.teal.withValues(alpha: 0.4)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Accommodation', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                            const SizedBox(height: 2),
                            Text('No accommodation assigned', style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                          ],
                        ),
                      ),
                    ],
                  )
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.hotel, color: Colors.teal, size: 20),
                          const SizedBox(width: 6),
                          Text('Accommodation', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Text(
                        acc.hotelName,
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Icon(Icons.location_on_outlined, size: 16, color: theme.colorScheme.onSurfaceVariant),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              [acc.roomNumber, acc.city].where((e) => e.isNotEmpty).join(', '),
                              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          _Chip(label: 'In: ${DateFormat('MMM d').format(acc.checkIn)}'),
                          const SizedBox(width: 6),
                          _Chip(label: 'Out: ${DateFormat('MMM d').format(acc.checkOut)}'),
                        ],
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}

class _TransportCard extends ConsumerWidget {
  final DashboardState dashState;

  const _TransportCard({required this.dashState});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final t = dashState.transport;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: t != null
            ? () {
                ref.read(selectedTransportProvider.notifier).state = t;
                context.push('/transport');
              }
            : null,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              left: BorderSide(color: Colors.purple, width: 4),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: t == null
                ? Row(
                    children: [
                      Icon(Icons.directions_bus_outlined, size: 36, color: Colors.purple.withValues(alpha: 0.4)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Transport', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                            const SizedBox(height: 2),
                            Text('No transport assigned', style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                          ],
                        ),
                      ),
                    ],
                  )
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.directions_bus, color: Colors.purple, size: 20),
                          const SizedBox(width: 6),
                          Text('Transport', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Text(
                        '${t.pickupLocation} → ${t.destination}',
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Icon(Icons.schedule, size: 16, color: theme.colorScheme.onSurfaceVariant),
                          const SizedBox(width: 4),
                          Text(
                            DateFormat('MMM d, HH:mm').format(t.pickupTime),
                            style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          _Chip(label: t.transportType),
                          const SizedBox(width: 6),
                          _Chip(label: t.busNumber),
                        ],
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;

  const _SectionHeader({required this.title});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Text(
      title,
      style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
    );
  }
}

class _QuickActionsGrid extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return GridView.count(
      crossAxisCount: 4,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 10,
      crossAxisSpacing: 10,
      childAspectRatio: 0.85,
      children: [
        _ActionTile(icon: Icons.inventory_2_outlined, label: 'My Package', color: Colors.teal, onTap: () => context.push('/package')),
        _ActionTile(icon: Icons.flight_outlined, label: 'Flights', color: Colors.blue, onTap: () {
          final flight = ref.read(dashboardProvider).nextFlight;
          if (flight != null) {
            ref.read(selectedFlightProvider.notifier).state = flight;
            context.push('/flight');
          }
        }),
        _ActionTile(icon: Icons.hotel_outlined, label: 'Hotels', color: Colors.teal, onTap: () {
          final acc = ref.read(dashboardProvider).accommodation;
          if (acc != null) {
            ref.read(selectedAccommodationProvider.notifier).state = acc;
            context.push('/accommodation');
          }
        }),
        _ActionTile(icon: Icons.directions_bus_outlined, label: 'Transport', color: Colors.purple, onTap: () {
          final t = ref.read(dashboardProvider).transport;
          if (t != null) {
            ref.read(selectedTransportProvider.notifier).state = t;
            context.push('/transport');
          }
        }),
        _ActionTile(icon: Icons.chat_bubble_outline, label: 'AI Chat', color: Colors.green, onTap: () => context.push('/ai-chat')),
        _ActionTile(icon: Icons.volume_up_outlined, label: 'Audio', color: Colors.orange, onTap: () => context.push('/audio')),
        _ActionTile(icon: Icons.campaign_outlined, label: 'Alerts', color: Colors.red, onTap: () => context.push('/announcements')),
        _ActionTile(icon: Icons.info_outline, label: 'Settings', color: Colors.indigo, onTap: () => context.push('/settings')),
      ],
    );
  }
}

class _ActionTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _ActionTile({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            const SizedBox(height: 6),
            Text(
              label,
              style: theme.textTheme.labelSmall?.copyWith(
                fontWeight: FontWeight.w500,
              ),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}

class _RecentNotifications extends StatelessWidget {
  final DashboardState dashState;

  const _RecentNotifications({required this.dashState});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final notifications = dashState.recentNotifications;

    if (notifications.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Center(
            child: Column(
              children: [
                Icon(Icons.notifications_none, size: 32, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
                const SizedBox(height: 8),
                Text(
                  'No notifications yet',
                  style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Column(
      children: notifications.map((n) {
        final isUnread = n.readAt == null;
        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: isUnread
                    ? theme.colorScheme.primary.withValues(alpha: 0.12)
                    : theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                _notifIcon(n.notificationType),
                color: isUnread ? theme.colorScheme.primary : theme.colorScheme.onSurfaceVariant,
                size: 20,
              ),
            ),
            title: Text(
              n.title,
              style: TextStyle(fontWeight: isUnread ? FontWeight.w600 : FontWeight.normal),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            subtitle: Text(
              n.message,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
            trailing: isUnread
                ? Container(
                    width: 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: theme.colorScheme.primary,
                      shape: BoxShape.circle,
                    ),
                  )
                : null,
          ),
        );
      }).toList(),
    );
  }

  IconData _notifIcon(String type) {
    if (type.contains('flight')) return Icons.flight_outlined;
    if (type.contains('accommodation') || type.contains('hotel')) return Icons.hotel_outlined;
    if (type.contains('transport') || type.contains('bus')) return Icons.directions_bus_outlined;
    if (type.contains('announcement')) return Icons.campaign_outlined;
    return Icons.notifications_outlined;
  }
}

class _StatusBadge extends StatelessWidget {
  final String status;

  const _StatusBadge({required this.status});

  @override
  Widget build(BuildContext context) {
    final color = switch (status.toLowerCase()) {
      'scheduled' => Colors.blue,
      'boarding' => Colors.orange,
      'departed' || 'in_flight' => Colors.green,
      'arrived' => Colors.teal,
      'cancelled' => Colors.red,
      'delayed' => Colors.amber,
      _ => Colors.grey,
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status.replaceAll('_', ' ').toUpperCase(),
        style: TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.w600,
          color: color,
        ),
      ),
    );
  }
}

class _Chip extends StatelessWidget {
  final String label;

  const _Chip({required this.label});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        label,
        style: theme.textTheme.labelSmall?.copyWith(
          color: theme.colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }
}
