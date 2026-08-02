import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../data/models/models.dart';
import '../../data/repositories/dashboard_repository.dart';

class DashboardState {
  final bool isLoading;
  final Flight? nextFlight;
  final Accommodation? accommodation;
  final Transport? transport;
  final int unreadNotifications;
  final int unreadAnnouncements;
  final List<AppNotification> recentNotifications;
  final List<Announcement> recentAnnouncements;
  final String? error;

  const DashboardState({
    this.isLoading = true,
    this.nextFlight,
    this.accommodation,
    this.transport,
    this.unreadNotifications = 0,
    this.unreadAnnouncements = 0,
    this.recentNotifications = const [],
    this.recentAnnouncements = const [],
    this.error,
  });

  DashboardState copyWith({
    bool? isLoading,
    Flight? nextFlight,
    Accommodation? accommodation,
    Transport? transport,
    int? unreadNotifications,
    int? unreadAnnouncements,
    List<AppNotification>? recentNotifications,
    List<Announcement>? recentAnnouncements,
    String? error,
  }) {
    return DashboardState(
      isLoading: isLoading ?? this.isLoading,
      nextFlight: nextFlight ?? this.nextFlight,
      accommodation: accommodation ?? this.accommodation,
      transport: transport ?? this.transport,
      unreadNotifications: unreadNotifications ?? this.unreadNotifications,
      unreadAnnouncements: unreadAnnouncements ?? this.unreadAnnouncements,
      recentNotifications: recentNotifications ?? this.recentNotifications,
      recentAnnouncements: recentAnnouncements ?? this.recentAnnouncements,
      error: error,
    );
  }
}

class DashboardNotifier extends StateNotifier<DashboardState> {
  final DashboardRepository _repository;

  DashboardNotifier(this._repository) : super(const DashboardState()) {
    loadDashboard();
  }

  Future<void> loadDashboard() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final results = await Future.wait([
        _repository.getFlights(),
        _repository.getAccommodations(),
        _repository.getTransports(),
        _repository.getMyNotifications(),
        _repository.getMyAnnouncements(),
      ]);

      final flights = results[0] as List<Flight>;
      final accommodations = results[1] as List<Accommodation>;
      final transports = results[2] as List<Transport>;
      final notifications = results[3] as List<AppNotification>;
      final announcements = results[4] as List<Announcement>;

      final now = DateTime.now().toUtc();
      final upcomingFlights = flights
          .where((f) => f.departureDatetime.isAfter(now))
          .toList()
        ..sort((a, b) => a.departureDatetime.compareTo(b.departureDatetime));

      final unreadNotifs = notifications.where((n) => n.readAt == null).length;
      final activeAnnouncements = announcements.where((a) {
        if (a.expiryDate == null) return true;
        return a.expiryDate!.isAfter(now);
      }).length;

      state = DashboardState(
        isLoading: false,
        nextFlight: upcomingFlights.isNotEmpty ? upcomingFlights.first : null,
        accommodation: accommodations.isNotEmpty ? accommodations.first : null,
        transport: transports.isNotEmpty ? transports.first : null,
        unreadNotifications: unreadNotifs,
        unreadAnnouncements: activeAnnouncements,
        recentNotifications: notifications.take(5).toList(),
        recentAnnouncements: announcements.take(5).toList(),
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString().replaceFirst('Exception: ', ''),
      );
    }
  }
}

final dashboardRepositoryProvider = Provider<DashboardRepository>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return DashboardRepository(dioClient.dio);
});

final dashboardProvider = StateNotifierProvider<DashboardNotifier, DashboardState>((ref) {
  final repository = ref.watch(dashboardRepositoryProvider);
  return DashboardNotifier(repository);
});
