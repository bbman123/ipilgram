import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../dashboard/data/models/models.dart';
import '../providers/flight_provider.dart';

class MyFlightScreen extends ConsumerStatefulWidget {
  const MyFlightScreen({super.key});

  @override
  ConsumerState<MyFlightScreen> createState() => _MyFlightScreenState();
}

class _MyFlightScreenState extends ConsumerState<MyFlightScreen>
    with SingleTickerProviderStateMixin {
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnimation;
  Timer? _countdownTimer;
  Duration _timeUntilDeparture = Duration.zero;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 0.8, end: 1.0).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
    _startCountdown();
  }

  void _startCountdown() {
    _updateCountdown();
    _countdownTimer = Timer.periodic(const Duration(seconds: 1), (_) => _updateCountdown());
  }

  void _updateCountdown() {
    final flight = ref.read(selectedFlightProvider);
    if (flight == null) return;
    final now = DateTime.now().toUtc();
    final departure = flight.departureDatetime.toUtc();
    setState(() {
      _timeUntilDeparture = departure.isAfter(now) ? departure.difference(now) : Duration.zero;
    });
  }

  @override
  void dispose() {
    _countdownTimer?.cancel();
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final flight = ref.watch(selectedFlightProvider);
    final theme = Theme.of(context);

    if (flight == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('My Flight')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.flight, size: 64, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
              const SizedBox(height: 16),
              Text('No flight information available', style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
            ],
          ),
        ),
      );
    }

    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          _FlightAppBar(flight: flight),
          SliverPadding(
            padding: EdgeInsets.symmetric(
              horizontal: isWide ? size.width * 0.15 : 16,
              vertical: 12,
            ),
            sliver: SliverList.list(
              children: [
                _CountdownSection(
                  timeUntilDeparture: _timeUntilDeparture,
                  pulseAnimation: _pulseAnimation,
                  status: flight.status,
                ),
                const SizedBox(height: 16),
                _FlightRouteCard(flight: flight),
                const SizedBox(height: 12),
                _FlightDetailsCard(flight: flight),
                const SizedBox(height: 12),
                _QRCodePlaceholder(flight: flight),
                const SizedBox(height: 80),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _FlightAppBar extends StatelessWidget {
  final Flight flight;

  const _FlightAppBar({required this.flight});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SliverAppBar(
      expandedHeight: 200,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: Text(
          '${flight.airline} ${flight.flightNumber}',
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        background: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                theme.colorScheme.primary,
                theme.colorScheme.primary.withValues(alpha: 0.6),
                theme.colorScheme.tertiary,
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Center(
            child: Icon(
              Icons.flight,
              size: 80,
              color: Colors.white.withValues(alpha: 0.15),
            ),
          ),
        ),
      ),
    );
  }
}

class _CountdownSection extends StatelessWidget {
  final Duration timeUntilDeparture;
  final Animation<double> pulseAnimation;
  final String status;

  const _CountdownSection({
    required this.timeUntilDeparture,
    required this.pulseAnimation,
    required this.status,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDeparted = status.toLowerCase() == 'departed' || status.toLowerCase() == 'in_flight';
    final isArrived = status.toLowerCase() == 'arrived';
    final isCancelled = status.toLowerCase() == 'cancelled';

    return Card(
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: isCancelled
                ? [Colors.red.shade50, Colors.red.shade100]
                : isArrived
                    ? [Colors.teal.shade50, Colors.teal.shade100]
                    : [Colors.blue.shade50, Colors.indigo.shade50],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Text(
                isDeparted
                    ? 'In Flight'
                    : isArrived
                        ? 'Arrived'
                        : isCancelled
                            ? 'Cancelled'
                            : 'Time Until Departure',
                style: theme.textTheme.titleSmall?.copyWith(
                  fontWeight: FontWeight.w600,
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: 12),
              if (isDeparted || isArrived || isCancelled)
                _StatusPill(status: status)
              else
                AnimatedBuilder(
                  animation: pulseAnimation,
                  builder: (context, child) {
                    return Transform.scale(
                      scale: pulseAnimation.value,
                      child: child,
                    );
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      _CountdownUnit(value: timeUntilDeparture.inDays, label: 'Days'),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 4),
                        child: Text(':', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      ),
                      _CountdownUnit(value: timeUntilDeparture.inHours % 24, label: 'Hrs'),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 4),
                        child: Text(':', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      ),
                      _CountdownUnit(value: timeUntilDeparture.inMinutes % 60, label: 'Min'),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 4),
                        child: Text(':', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      ),
                      _CountdownUnit(value: timeUntilDeparture.inSeconds % 60, label: 'Sec'),
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

class _CountdownUnit extends StatelessWidget {
  final int value;
  final String label;

  const _CountdownUnit({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      children: [
        Container(
          width: 56,
          height: 56,
          decoration: BoxDecoration(
            color: theme.colorScheme.primary,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: theme.colorScheme.primary.withValues(alpha: 0.3),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Center(
            child: Text(
              value.toString().padLeft(2, '0'),
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: theme.textTheme.labelSmall?.copyWith(
            color: theme.colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }
}

class _StatusPill extends StatelessWidget {
  final String status;

  const _StatusPill({required this.status});

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
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          const SizedBox(width: 8),
          Text(
            status.replaceAll('_', ' ').toUpperCase(),
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w700,
              color: color,
              letterSpacing: 1,
            ),
          ),
        ],
      ),
    );
  }
}

class _FlightRouteCard extends StatelessWidget {
  final Flight flight;

  const _FlightRouteCard({required this.flight});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('DEPARTURE', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant, letterSpacing: 1)),
                      const SizedBox(height: 4),
                      Text(
                        flight.departureAirport,
                        style: theme.textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        DateFormat('EEE, MMM d').format(flight.departureDatetime),
                        style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                      ),
                      Text(
                        DateFormat('HH:mm').format(flight.departureDatetime),
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
                Column(
                  children: [
                    Icon(Icons.flight, color: theme.colorScheme.primary, size: 32),
                    Container(
                      width: 80,
                      height: 2,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [theme.colorScheme.primary.withValues(alpha: 0.3), theme.colorScheme.primary],
                        ),
                      ),
                    ),
                  ],
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('ARRIVAL', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant, letterSpacing: 1)),
                      const SizedBox(height: 4),
                      Text(
                        flight.arrivalAirport,
                        style: theme.textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        DateFormat('EEE, MMM d').format(flight.arrivalDatetime),
                        style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                      ),
                      Text(
                        DateFormat('HH:mm').format(flight.arrivalDatetime),
                        style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _FlightDetailsCard extends StatelessWidget {
  final Flight flight;

  const _FlightDetailsCard({required this.flight});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final duration = flight.arrivalDatetime.difference(flight.departureDatetime);
    final hours = duration.inHours;
    final minutes = duration.inMinutes % 60;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Flight Details', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            _DetailRow(icon: Icons.business, label: 'Airline', value: flight.airline),
            _DetailRow(icon: Icons.confirmation_number, label: 'Flight Number', value: flight.flightNumber),
            _DetailRow(icon: Icons.door_front_door, label: 'Gate', value: flight.gate ?? 'TBA'),
            _DetailRow(icon: Icons.event_seat, label: 'Seat', value: flight.seatNumber ?? 'Not assigned'),
            _DetailRow(icon: Icons.schedule, label: 'Duration', value: '${hours}h ${minutes}m'),
            _DetailRow(
              icon: Icons.calendar_today,
              label: 'Departure',
              value: DateFormat('MMM d, yyyy • HH:mm').format(flight.departureDatetime),
            ),
            _DetailRow(
              icon: Icons.calendar_today,
              label: 'Arrival',
              value: DateFormat('MMM d, yyyy • HH:mm').format(flight.arrivalDatetime),
            ),
          ],
        ),
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _DetailRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: [
          Icon(icon, size: 18, color: theme.colorScheme.primary.withValues(alpha: 0.7)),
          const SizedBox(width: 10),
          Text('$label ', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          const Spacer(),
          Text(value, style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}

class _QRCodePlaceholder extends StatelessWidget {
  final Flight flight;

  const _QRCodePlaceholder({required this.flight});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Text('Boarding Pass', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
            const SizedBox(height: 16),
            Container(
              width: 180,
              height: 180,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: theme.colorScheme.outlineVariant),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.qr_code_2,
                    size: 100,
                    color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.3),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'QR Code',
                    style: theme.textTheme.labelMedium?.copyWith(
                      color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.5),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Text(
              '${flight.airline} • ${flight.flightNumber}',
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
            Text(
              '${flight.departureAirport} → ${flight.arrivalAirport}',
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
            if (flight.seatNumber != null) ...[
              const SizedBox(height: 4),
              Text(
                'Seat ${flight.seatNumber}',
                style: theme.textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w600),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
