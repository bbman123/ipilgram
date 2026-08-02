import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../dashboard/data/models/models.dart';
import '../providers/accommodation_provider.dart';

class MyAccommodationScreen extends ConsumerWidget {
  const MyAccommodationScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final accommodation = ref.watch(selectedAccommodationProvider);
    final theme = Theme.of(context);

    if (accommodation == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('My Accommodation')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.hotel, size: 64, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.4)),
              const SizedBox(height: 16),
              Text('No accommodation information available', style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
            ],
          ),
        ),
      );
    }

    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;
    final now = DateTime.now().toUtc();
    final checkIn = accommodation.checkIn.toUtc();
    final checkOut = accommodation.checkOut.toUtc();
    final isCheckedIn = now.isAfter(checkIn);
    final isCheckedOut = now.isAfter(checkOut);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          _HotelAppBar(accommodation: accommodation),
          SliverPadding(
            padding: EdgeInsets.symmetric(
              horizontal: isWide ? size.width * 0.15 : 16,
              vertical: 12,
            ),
            sliver: SliverList.list(
              children: [
                _StatusBanner(isCheckedIn: isCheckedIn, isCheckedOut: isCheckedOut),
                const SizedBox(height: 16),
                _HotelInfoCard(accommodation: accommodation),
                const SizedBox(height: 12),
                _RoomDetailsCard(accommodation: accommodation),
                const SizedBox(height: 12),
                _CheckDatesCard(accommodation: accommodation),
                const SizedBox(height: 12),
                _MapButton(address: accommodation.address, city: accommodation.city),
                const SizedBox(height: 12),
                _ImagePlaceholder(accommodation: accommodation),
                const SizedBox(height: 80),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _HotelAppBar extends StatelessWidget {
  final Accommodation accommodation;

  const _HotelAppBar({required this.accommodation});

  @override
  Widget build(BuildContext context) {
    return SliverAppBar(
      expandedHeight: 220,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: Text(
          accommodation.hotelName,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        background: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                Colors.teal.shade600,
                Colors.teal.shade400,
                Colors.teal.shade200,
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
                  Icons.hotel,
                  size: 180,
                  color: Colors.white.withValues(alpha: 0.08),
                ),
              ),
              Center(
                child: Icon(
                  Icons.hotel,
                  size: 80,
                  color: Colors.white.withValues(alpha: 0.15),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _StatusBanner extends StatelessWidget {
  final bool isCheckedIn;
  final bool isCheckedOut;

  const _StatusBanner({required this.isCheckedIn, required this.isCheckedOut});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final (label, color, icon) = isCheckedOut
        ? ('Checked Out', Colors.grey, Icons.logout)
        : isCheckedIn
            ? ('Currently Staying', Colors.green, Icons.hotel)
            : ('Upcoming Stay', Colors.teal, Icons.upcoming);

    return Card(
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: [color.withValues(alpha: 0.1), color.withValues(alpha: 0.05)],
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 24),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      label,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                        color: color,
                      ),
                    ),
                    Text(
                      isCheckedOut
                          ? 'Your stay has ended'
                          : isCheckedIn
                              ? 'You are currently staying here'
                              : 'Your stay is coming up',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
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

class _HotelInfoCard extends StatelessWidget {
  final Accommodation accommodation;

  const _HotelInfoCard({required this.accommodation});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.hotel, color: Colors.teal, size: 20),
                const SizedBox(width: 8),
                Text('Hotel Information', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
              ],
            ),
            const SizedBox(height: 14),
            _InfoRow(icon: Icons.business, label: 'Hotel', value: accommodation.hotelName),
            _InfoRow(icon: Icons.location_on, label: 'City', value: accommodation.city),
            if (accommodation.address != null)
              _InfoRow(icon: Icons.map, label: 'Address', value: accommodation.address!),
            if (accommodation.building != null)
              _InfoRow(icon: Icons.apartment, label: 'Building', value: accommodation.building!),
          ],
        ),
      ),
    );
  }
}

class _RoomDetailsCard extends StatelessWidget {
  final Accommodation accommodation;

  const _RoomDetailsCard({required this.accommodation});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.meeting_room, color: Colors.indigo, size: 20),
                const SizedBox(width: 8),
                Text('Room Details', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
              ],
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                Expanded(
                  child: _RoomBadge(
                    label: 'Room',
                    value: accommodation.roomNumber,
                    icon: Icons.door_front_door,
                    color: Colors.indigo,
                  ),
                ),
                const SizedBox(width: 10),
                if (accommodation.floor != null)
                  Expanded(
                    child: _RoomBadge(
                      label: 'Floor',
                      value: accommodation.floor!,
                      icon: Icons.layers,
                      color: Colors.purple,
                    ),
                  ),
                if (accommodation.bedNumber != null) ...[
                  const SizedBox(width: 10),
                  Expanded(
                    child: _RoomBadge(
                      label: 'Bed',
                      value: accommodation.bedNumber!,
                      icon: Icons.king_bed,
                      color: Colors.orange,
                    ),
                  ),
                ],
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _RoomBadge extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;

  const _RoomBadge({
    required this.label,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.15)),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 6),
          Text(value, style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold, color: color)),
          Text(label, style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
        ],
      ),
    );
  }
}

class _CheckDatesCard extends StatelessWidget {
  final Accommodation accommodation;

  const _CheckDatesCard({required this.accommodation});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final nights = accommodation.checkOut.difference(accommodation.checkIn).inDays;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.calendar_today, color: Colors.blue, size: 20),
                const SizedBox(width: 8),
                Text('Stay Duration', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _DateBlock(
                    label: 'CHECK-IN',
                    date: accommodation.checkIn,
                    color: Colors.green,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  child: Column(
                    children: [
                      Icon(Icons.arrow_forward, color: theme.colorScheme.primary, size: 20),
                      const SizedBox(height: 4),
                      Text(
                        '$nights ${nights == 1 ? 'night' : 'nights'}',
                        style: theme.textTheme.labelSmall?.copyWith(fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: _DateBlock(
                    label: 'CHECK-OUT',
                    date: accommodation.checkOut,
                    color: Colors.red,
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

class _DateBlock extends StatelessWidget {
  final String label;
  final DateTime date;
  final Color color;

  const _DateBlock({required this.label, required this.date, required this.color});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.06),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Column(
        children: [
          Text(label, style: theme.textTheme.labelSmall?.copyWith(color: color, letterSpacing: 1)),
          const SizedBox(height: 6),
          Text(
            DateFormat('MMM d').format(date),
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          Text(
            DateFormat('yyyy').format(date),
            style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
          ),
          const SizedBox(height: 2),
          Text(
            DateFormat('EEE').format(date),
            style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
          ),
        ],
      ),
    );
  }
}

class _MapButton extends StatelessWidget {
  final String? address;
  final String city;

  const _MapButton({required this.address, required this.city});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      child: InkWell(
        onTap: () {},
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: Colors.red.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.map, color: Colors.red, size: 24),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('View on Google Maps', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                    Text(
                      address ?? city,
                      style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              Icon(Icons.open_in_new, color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.5), size: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class _ImagePlaceholder extends StatelessWidget {
  final Accommodation accommodation;

  const _ImagePlaceholder({required this.accommodation});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Container(
        height: 180,
        width: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Colors.teal.withValues(alpha: 0.1),
              Colors.teal.withValues(alpha: 0.05),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.hotel,
              size: 56,
              color: Colors.teal.withValues(alpha: 0.3),
            ),
            const SizedBox(height: 10),
            Text(
              accommodation.hotelName,
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
                color: Colors.teal.withValues(alpha: 0.6),
              ),
            ),
            const SizedBox(height: 4),
            Text(
              accommodation.city,
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoRow({
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
          Icon(icon, size: 18, color: Colors.teal.withValues(alpha: 0.7)),
          const SizedBox(width: 10),
          Text('$label ', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
          const Spacer(),
          Flexible(
            child: Text(value, style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w600), overflow: TextOverflow.ellipsis),
          ),
        ],
      ),
    );
  }
}
