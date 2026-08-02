import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../data/models/models.dart';
import '../../data/repositories/package_repository.dart';

enum PackageStatus { initial, loading, loaded, empty, error }

class PackageState {
  final PackageStatus status;
  final PackageDetail? package;
  final String? error;

  const PackageState({
    this.status = PackageStatus.initial,
    this.package,
    this.error,
  });

  PackageState copyWith({
    PackageStatus? status,
    PackageDetail? package,
    String? error,
  }) {
    return PackageState(
      status: status ?? this.status,
      package: package ?? this.package,
      error: error,
    );
  }
}

class PackageNotifier extends StateNotifier<PackageState> {
  final PackageRepository _repository;

  PackageNotifier(this._repository) : super(const PackageState()) {
    loadPackage();
  }

  Future<void> loadPackage() async {
    state = state.copyWith(status: PackageStatus.loading, error: null);
    try {
      final package = await _repository.getMyPackage();
      state = PackageState(status: PackageStatus.loaded, package: package);
    } catch (e) {
      final msg = e.toString().replaceFirst('Exception: ', '');
      if (msg.contains('404') || msg.toLowerCase().contains('no package')) {
        state = const PackageState(status: PackageStatus.empty);
      } else {
        state = PackageState(status: PackageStatus.error, error: msg);
      }
    }
  }
}

final packageRepositoryProvider = Provider<PackageRepository>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return PackageRepository(dioClient.dio);
});

final packageProvider = StateNotifierProvider<PackageNotifier, PackageState>((ref) {
  final repository = ref.watch(packageRepositoryProvider);
  return PackageNotifier(repository);
});
