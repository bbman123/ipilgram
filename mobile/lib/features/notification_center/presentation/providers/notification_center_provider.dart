import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../dashboard/data/models/app_notification.dart';
import '../../data/repositories/notification_repository.dart';

final notificationRepositoryProvider = Provider<NotificationRepository>((ref) {
  final dio = ref.watch(dioClientProvider).dio;
  return NotificationRepository(dio);
});

enum NotificationCategory { all, flight, accommodation, transport, general }

class NotificationCenterState {
  final bool isLoading;
  final List<AppNotification> allNotifications;
  final NotificationCategory selectedCategory;
  final String? error;

  const NotificationCenterState({
    this.isLoading = false,
    this.allNotifications = const [],
    this.selectedCategory = NotificationCategory.all,
    this.error,
  });

  NotificationCenterState copyWith({
    bool? isLoading,
    List<AppNotification>? allNotifications,
    NotificationCategory? selectedCategory,
    String? error,
  }) {
    return NotificationCenterState(
      isLoading: isLoading ?? this.isLoading,
      allNotifications: allNotifications ?? this.allNotifications,
      selectedCategory: selectedCategory ?? this.selectedCategory,
      error: error,
    );
  }

  List<AppNotification> get notifications {
    if (selectedCategory == NotificationCategory.all) {
      return allNotifications;
    }
    return allNotifications.where((n) => n.notificationType == selectedCategory.name).toList();
  }

  int get unreadCount => allNotifications.where((n) => n.readAt == null).length;

  int unreadCountFor(NotificationCategory cat) {
    if (cat == NotificationCategory.all) return unreadCount;
    return allNotifications.where((n) => n.notificationType == cat.name && n.readAt == null).length;
  }
}

class NotificationCenterNotifier extends StateNotifier<NotificationCenterState> {
  final NotificationRepository _repo;

  NotificationCenterNotifier(this._repo) : super(const NotificationCenterState());

  Future<void> load() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final items = await _repo.getMyNotifications();
      state = state.copyWith(isLoading: false, allNotifications: items);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  Future<void> markAsRead(int id) async {
    try {
      await _repo.markAsRead(id);
      state = state.copyWith(
        allNotifications: state.allNotifications.map((n) {
          if (n.id == id) {
            return AppNotification(
              id: n.id,
              pilgrimId: n.pilgrimId,
              title: n.title,
              message: n.message,
              notificationType: n.notificationType,
              status: 'read',
              scheduledTime: n.scheduledTime,
              sentAt: n.sentAt,
              readAt: DateTime.now().toUtc(),
              deliveryMode: n.deliveryMode,
              language: n.language,
              audioUrl: n.audioUrl,
              sourceType: n.sourceType,
              sourceId: n.sourceId,
              createdAt: n.createdAt,
              updatedAt: n.updatedAt,
            );
          }
          return n;
        }).toList(),
      );
    } catch (_) {}
  }

  void setCategory(NotificationCategory cat) {
    state = state.copyWith(selectedCategory: cat);
  }
}

final notificationCenterProvider = StateNotifierProvider<NotificationCenterNotifier, NotificationCenterState>((ref) {
  final repo = ref.watch(notificationRepositoryProvider);
  final notifier = NotificationCenterNotifier(repo);
  return notifier;
});

final unreadCountProvider = Provider<int>((ref) {
  final state = ref.watch(notificationCenterProvider);
  return state.unreadCount;
});
