import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../data/models/personalized_announcement.dart';
import '../../data/repositories/announcement_repository.dart';

final announcementRepositoryProvider = Provider<AnnouncementRepository>((ref) {
  final dio = ref.watch(dioClientProvider).dio;
  return AnnouncementRepository(dio);
});

enum AnnouncementSort { newest, priority }

class AnnouncementState {
  final bool isLoading;
  final List<PersonalizedAnnouncement> allAnnouncements;
  final String searchQuery;
  final AnnouncementSort sort;
  final String? error;

  const AnnouncementState({
    this.isLoading = false,
    this.allAnnouncements = const [],
    this.searchQuery = '',
    this.sort = AnnouncementSort.newest,
    this.error,
  });

  AnnouncementState copyWith({
    bool? isLoading,
    List<PersonalizedAnnouncement>? allAnnouncements,
    String? searchQuery,
    AnnouncementSort? sort,
    String? error,
  }) {
    return AnnouncementState(
      isLoading: isLoading ?? this.isLoading,
      allAnnouncements: allAnnouncements ?? this.allAnnouncements,
      searchQuery: searchQuery ?? this.searchQuery,
      sort: sort ?? this.sort,
      error: error,
    );
  }

  List<PersonalizedAnnouncement> get announcements {
    var list = List<PersonalizedAnnouncement>.from(allAnnouncements);

    if (searchQuery.isNotEmpty) {
      final q = searchQuery.toLowerCase();
      list = list.where((a) =>
        a.title.toLowerCase().contains(q) ||
        a.message.toLowerCase().contains(q)
      ).toList();
    }

    if (sort == AnnouncementSort.priority) {
      list.sort((a, b) => _priorityValue(b.priority).compareTo(_priorityValue(a.priority)));
    } else {
      list.sort((a, b) => (b.publishDate ?? DateTime(0)).compareTo(a.publishDate ?? DateTime(0)));
    }

    return list;
  }

  int _priorityValue(String p) {
    switch (p.toLowerCase()) {
      case 'critical': return 4;
      case 'high': return 3;
      case 'medium': return 2;
      case 'low': return 1;
      default: return 0;
    }
  }
}

class AnnouncementNotifier extends StateNotifier<AnnouncementState> {
  final AnnouncementRepository _repo;

  AnnouncementNotifier(this._repo) : super(const AnnouncementState());

  Future<void> load() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final items = await _repo.getMyAnnouncements();
      state = state.copyWith(isLoading: false, allAnnouncements: items);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  void setSearch(String query) {
    state = state.copyWith(searchQuery: query);
  }

  void setSort(AnnouncementSort sort) {
    state = state.copyWith(sort: sort);
  }
}

final announcementProvider = StateNotifierProvider<AnnouncementNotifier, AnnouncementState>((ref) {
  final repo = ref.watch(announcementRepositoryProvider);
  final notifier = AnnouncementNotifier(repo);
  return notifier;
});
