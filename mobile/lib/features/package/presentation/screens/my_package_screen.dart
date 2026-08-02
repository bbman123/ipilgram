import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/package_provider.dart';
import '../../data/models/models.dart';
import '../../../dashboard/data/models/models.dart';

class MyPackageScreen extends ConsumerWidget {
  const MyPackageScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(packageProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Package'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.read(packageProvider.notifier).loadPackage(),
          ),
        ],
      ),
      body: _buildBody(state, theme, ref),
    );
  }

  Widget _buildBody(PackageState state, ThemeData theme, WidgetRef ref) {
    switch (state.status) {
      case PackageStatus.initial:
      case PackageStatus.loading:
        return _LoadingState();
      case PackageStatus.empty:
        return _EmptyState(theme: theme);
      case PackageStatus.error:
        return _ErrorState(
          message: state.error ?? 'Unknown error',
          onRetry: () => ref.read(packageProvider.notifier).loadPackage(),
        );
      case PackageStatus.loaded:
        return _PackageContent(package: state.package!);
    }
  }
}

class _LoadingState extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(color: Theme.of(context).colorScheme.primary),
          const SizedBox(height: 16),
          Text(
            'Loading your package...',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
          ),
        ],
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  final ThemeData theme;

  const _EmptyState({required this.theme});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.inventory_2_outlined,
                size: 48,
                color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.5),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'No Package Assigned',
              style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(
              'You haven\'t been assigned a Hajj package yet. Please contact your administrator.',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

class _ErrorState extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const _ErrorState({required this.message, this.onRetry});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                color: theme.colorScheme.errorContainer,
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.error_outline,
                size: 48,
                color: theme.colorScheme.error,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Something went wrong',
              style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

class _PackageContent extends StatelessWidget {
  final PackageDetail package;

  const _PackageContent({required this.package});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return RefreshIndicator(
      onRefresh: () async {
        // Trigger rebuild
      },
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: EdgeInsets.symmetric(
          horizontal: isWide ? size.width * 0.15 : 16,
          vertical: 16,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _PackageHeader(package: package),
            const SizedBox(height: 20),
            _SummarySection(package: package),
            const SizedBox(height: 16),
            Text('Trip Details', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            _ExpandableFlightCard(flight: package.flight),
            const SizedBox(height: 12),
            _ExpandableAccommodationCard(accommodation: package.accommodation),
            const SizedBox(height: 12),
            _ExpandableTransportCard(transport: package.transport),
            const SizedBox(height: 16),
            _ImportantDatesCard(package: package),
            const SizedBox(height: 80),
          ],
        ),
      ),
    );
  }
}

class _PackageHeader extends StatelessWidget {
  final PackageDetail package;

  const _PackageHeader({required this.package});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              theme.colorScheme.primary,
              theme.colorScheme.primary.withValues(alpha: 0.7),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.inventory_2, color: Colors.white, size: 28),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          package.name,
                          style: theme.textTheme.headlineSmall?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Package #${package.id}',
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: Colors.white.withValues(alpha: 0.8),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              if (package.description != null && package.description!.isNotEmpty) ...[
                const SizedBox(height: 14),
                Text(
                  package.description!,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: Colors.white.withValues(alpha: 0.9),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _SummarySection extends StatelessWidget {
  final PackageDetail package;

  const _SummarySection({required this.package});

  @override
  Widget build(BuildContext context) {
    final items = [
      _SummaryItem(
        icon: Icons.flight,
        label: 'Flight',
        value: package.flight != null ? '${package.flight!.departureAirport} → ${package.flight!.arrivalAirport}' : 'Not assigned',
        color: Colors.blue,
      ),
      _SummaryItem(
        icon: Icons.hotel,
        label: 'Hotel',
        value: package.accommodation != null ? package.accommodation!.hotelName : 'Not assigned',
        color: Colors.teal,
      ),
      _SummaryItem(
        icon: Icons.directions_bus,
        label: 'Transport',
        value: package.transport != null ? package.transport!.transportType.toUpperCase() : 'Not assigned',
        color: Colors.purple,
      ),
      _SummaryItem(
        icon: Icons.people,
        label: 'Fellow Pilgrims',
        value: '${package.pilgrimCount}',
        color: Colors.orange,
      ),
    ];

    return Row(
      children: items.map((item) => Expanded(child: item)).toList(),
    );
  }
}

class _SummaryItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _SummaryItem({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
        child: Column(
          children: [
            Container(
              width: 36,
              height: 36,
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 20),
            ),
            const SizedBox(height: 6),
            Text(
              value,
              style: theme.textTheme.labelMedium?.copyWith(fontWeight: FontWeight.w600),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 2),
            Text(
              label,
              style: theme.textTheme.labelSmall?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ExpandableFlightCard extends StatefulWidget {
  final Flight? flight;

  const _ExpandableFlightCard({required this.flight});

  @override
  State<_ExpandableFlightCard> createState() => _ExpandableFlightCardState();
}

class _ExpandableFlightCardState extends State<_ExpandableFlightCard> {
  bool _expanded = true;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final flight = widget.flight;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.blue.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.flight, color: Colors.blue, size: 22),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Flight', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        Text(
                          flight != null ? '${flight.airline} ${flight.flightNumber}' : 'Not assigned',
                          style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                        ),
                      ],
                    ),
                  ),
                  AnimatedRotation(
                    turns: _expanded ? 0.5 : 0,
                    duration: const Duration(milliseconds: 200),
                    child: Icon(Icons.expand_more, color: theme.colorScheme.onSurfaceVariant),
                  ),
                ],
              ),
            ),
          ),
          AnimatedCrossFade(
            firstChild: const SizedBox.shrink(),
            secondChild: flight == null
                ? _EmptyDetail(message: 'No flight assigned to this package', theme: theme)
                : _FlightDetail(flight: flight, theme: theme),
            crossFadeState: _expanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
            duration: const Duration(milliseconds: 250),
          ),
        ],
      ),
    );
  }
}

class _FlightDetail extends StatelessWidget {
  final Flight flight;
  final ThemeData theme;

  const _FlightDetail({required this.flight, required this.theme});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Divider(height: 1),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('FROM', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                    Text(flight.departureAirport, style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
              Icon(Icons.flight_takeoff, color: theme.colorScheme.primary, size: 28),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text('TO', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                    Text(flight.arrivalAirport, style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _DetailRow(icon: Icons.calendar_today, label: 'Departure', value: DateFormat('MMM d, yyyy • HH:mm').format(flight.departureDatetime)),
          _DetailRow(icon: Icons.calendar_today, label: 'Arrival', value: DateFormat('MMM d, yyyy • HH:mm').format(flight.arrivalDatetime)),
          _DetailRow(icon: Icons.business, label: 'Airline', value: flight.airline),
          if (flight.gate != null) _DetailRow(icon: Icons.door_front_door, label: 'Gate', value: flight.gate!),
          if (flight.seatNumber != null) _DetailRow(icon: Icons.event_seat, label: 'Seat', value: flight.seatNumber!),
          const SizedBox(height: 8),
          _StatusChip(status: flight.status),
        ],
      ),
    );
  }
}

class _ExpandableAccommodationCard extends StatefulWidget {
  final Accommodation? accommodation;

  const _ExpandableAccommodationCard({required this.accommodation});

  @override
  State<_ExpandableAccommodationCard> createState() => _ExpandableAccommodationCardState();
}

class _ExpandableAccommodationCardState extends State<_ExpandableAccommodationCard> {
  bool _expanded = true;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final acc = widget.accommodation;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.teal.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.hotel, color: Colors.teal, size: 22),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Accommodation', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        Text(
                          acc != null ? '${acc.hotelName} • Room ${acc.roomNumber}' : 'Not assigned',
                          style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                        ),
                      ],
                    ),
                  ),
                  AnimatedRotation(
                    turns: _expanded ? 0.5 : 0,
                    duration: const Duration(milliseconds: 200),
                    child: Icon(Icons.expand_more, color: theme.colorScheme.onSurfaceVariant),
                  ),
                ],
              ),
            ),
          ),
          AnimatedCrossFade(
            firstChild: const SizedBox.shrink(),
            secondChild: acc == null
                ? _EmptyDetail(message: 'No accommodation assigned to this package', theme: theme)
                : _AccommodationDetail(accommodation: acc, theme: theme),
            crossFadeState: _expanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
            duration: const Duration(milliseconds: 250),
          ),
        ],
      ),
    );
  }
}

class _AccommodationDetail extends StatelessWidget {
  final Accommodation accommodation;
  final ThemeData theme;

  const _AccommodationDetail({required this.accommodation, required this.theme});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Divider(height: 1),
          const SizedBox(height: 16),
          Text(
            accommodation.hotelName,
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 12),
          _DetailRow(icon: Icons.location_on, label: 'City', value: accommodation.city),
          _DetailRow(icon: Icons.meeting_room, label: 'Room', value: accommodation.roomNumber),
          if (accommodation.building != null) _DetailRow(icon: Icons.apartment, label: 'Building', value: accommodation.building!),
          if (accommodation.floor != null) _DetailRow(icon: Icons.layers, label: 'Floor', value: accommodation.floor!),
          if (accommodation.bedNumber != null) _DetailRow(icon: Icons.king_bed, label: 'Bed', value: accommodation.bedNumber!),
          if (accommodation.address != null) _DetailRow(icon: Icons.map, label: 'Address', value: accommodation.address!),
          const SizedBox(height: 8),
          Row(
            children: [
              _DateChip(label: 'Check-in', date: accommodation.checkIn),
              const SizedBox(width: 8),
              _DateChip(label: 'Check-out', date: accommodation.checkOut),
            ],
          ),
        ],
      ),
    );
  }
}

class _ExpandableTransportCard extends StatefulWidget {
  final Transport? transport;

  const _ExpandableTransportCard({required this.transport});

  @override
  State<_ExpandableTransportCard> createState() => _ExpandableTransportCardState();
}

class _ExpandableTransportCardState extends State<_ExpandableTransportCard> {
  bool _expanded = true;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final t = widget.transport;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.purple.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.directions_bus, color: Colors.purple, size: 22),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Transport', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        Text(
                          t != null ? '${t.transportType.toUpperCase()} • ${t.busNumber}' : 'Not assigned',
                          style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                        ),
                      ],
                    ),
                  ),
                  AnimatedRotation(
                    turns: _expanded ? 0.5 : 0,
                    duration: const Duration(milliseconds: 200),
                    child: Icon(Icons.expand_more, color: theme.colorScheme.onSurfaceVariant),
                  ),
                ],
              ),
            ),
          ),
          AnimatedCrossFade(
            firstChild: const SizedBox.shrink(),
            secondChild: t == null
                ? _EmptyDetail(message: 'No transport assigned to this package', theme: theme)
                : _TransportDetail(transport: t, theme: theme),
            crossFadeState: _expanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
            duration: const Duration(milliseconds: 250),
          ),
        ],
      ),
    );
  }
}

class _TransportDetail extends StatelessWidget {
  final Transport transport;
  final ThemeData theme;

  const _TransportDetail({required this.transport, required this.theme});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Divider(height: 1),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('FROM', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                    Text(transport.pickupLocation, style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600), maxLines: 2, overflow: TextOverflow.ellipsis),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                child: Icon(Icons.arrow_forward, color: theme.colorScheme.primary),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text('TO', style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                    Text(transport.destination, style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600), maxLines: 2, overflow: TextOverflow.ellipsis),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _DetailRow(icon: Icons.schedule, label: 'Pickup Time', value: DateFormat('MMM d, yyyy • HH:mm').format(transport.pickupTime)),
          _DetailRow(icon: Icons.person, label: 'Driver', value: transport.driverName),
          _DetailRow(icon: Icons.phone, label: 'Driver Phone', value: transport.driverPhone),
          _DetailRow(icon: Icons.directions_bus, label: 'Vehicle', value: '${transport.transportType.toUpperCase()} • ${transport.busNumber}'),
        ],
      ),
    );
  }
}

class _ImportantDatesCard extends StatelessWidget {
  final PackageDetail package;

  const _ImportantDatesCard({required this.package});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final dates = <_DateEntry>[];

    if (package.flight != null) {
      dates.add(_DateEntry('Flight Departure', package.flight!.departureDatetime, Icons.flight_takeoff, Colors.blue));
      dates.add(_DateEntry('Flight Arrival', package.flight!.arrivalDatetime, Icons.flight_land, Colors.blue));
    }
    if (package.accommodation != null) {
      dates.add(_DateEntry('Hotel Check-in', package.accommodation!.checkIn, Icons.hotel, Colors.teal));
      dates.add(_DateEntry('Hotel Check-out', package.accommodation!.checkOut, Icons.hotel, Colors.teal));
    }
    if (package.transport != null) {
      dates.add(_DateEntry('Transport Pickup', package.transport!.pickupTime, Icons.directions_bus, Colors.purple));
    }

    if (dates.isEmpty) return const SizedBox.shrink();

    dates.sort((a, b) => a.date.compareTo(b.date));

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.event, color: theme.colorScheme.primary, size: 20),
                const SizedBox(width: 8),
                Text('Important Dates', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
              ],
            ),
            const SizedBox(height: 12),
            ...dates.map((entry) => Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Row(
                    children: [
                      Container(
                        width: 32,
                        height: 32,
                        decoration: BoxDecoration(
                          color: entry.color.withValues(alpha: 0.12),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(entry.icon, color: entry.color, size: 16),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(entry.label, style: theme.textTheme.bodyMedium),
                      ),
                      Text(
                        DateFormat('MMM d, yyyy').format(entry.date),
                        style: theme.textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w500,
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }
}

class _DateEntry {
  final String label;
  final DateTime date;
  final IconData icon;
  final Color color;

  _DateEntry(this.label, this.date, this.icon, this.color);
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
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Icon(icon, size: 16, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6)),
          const SizedBox(width: 8),
          Text('$label: ', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          Expanded(
            child: Text(value, style: theme.textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w500)),
          ),
        ],
      ),
    );
  }
}

class _StatusChip extends StatelessWidget {
  final String status;

  const _StatusChip({required this.status});

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
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status.replaceAll('_', ' ').toUpperCase(),
        style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: color),
      ),
    );
  }
}

class _DateChip extends StatelessWidget {
  final String label;
  final DateTime date;

  const _DateChip({required this.label, required this.date});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          Text(DateFormat('MMM d').format(date), style: theme.textTheme.labelMedium?.copyWith(fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}

class _EmptyDetail extends StatelessWidget {
  final String message;
  final ThemeData theme;

  const _EmptyDetail({required this.message, required this.theme});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Icon(Icons.info_outline, size: 18, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.5)),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              message,
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
          ),
        ],
      ),
    );
  }
}
