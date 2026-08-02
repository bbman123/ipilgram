import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../../core/constants/constants.dart';
import '../../../../core/network/dio_client.dart';
import '../../data/models/models.dart';
import '../../data/repositories/auth_repository.dart';

enum AuthStatus { initial, authenticated, unauthenticated, loading, error }

class AuthState {
  final AuthStatus status;
  final User? user;
  final String? error;

  const AuthState({
    this.status = AuthStatus.initial,
    this.user,
    this.error,
  });

  AuthState copyWith({
    AuthStatus? status,
    User? user,
    String? error,
  }) {
    return AuthState(
      status: status ?? this.status,
      user: user ?? this.user,
      error: error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;
  final DioClient _dioClient;

  AuthNotifier(this._repository, this._dioClient) : super(const AuthState()) {
    _init();
  }

  Future<void> _init() async {
    final hasToken = await _repository.tryAutoLogin();
    if (hasToken) {
      try {
        final user = await _repository.getMe();
        await _saveUserPrefs(user);
        state = AuthState(status: AuthStatus.authenticated, user: user);
      } catch (e) {
        _dioClient.clearTokens();
        await _dioClient.clearPersistedTokens();
        state = const AuthState(status: AuthStatus.unauthenticated);
      }
    } else {
      state = const AuthState(status: AuthStatus.unauthenticated);
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(status: AuthStatus.loading, error: null);
    try {
      await _repository.login(email, password);
      final user = await _repository.getMe();
      await _saveUserPrefs(user);
      state = AuthState(status: AuthStatus.authenticated, user: user);
    } catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      state = AuthState(status: AuthStatus.error, error: message);
    }
  }

  Future<void> logout() async {
    await _repository.logout();
    await _clearUserPrefs();
    state = const AuthState(status: AuthStatus.unauthenticated);
  }

  Future<void> _saveUserPrefs(User user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(StorageKeys.userId, user.id);
    await prefs.setString(StorageKeys.userEmail, user.email);
    await prefs.setString(StorageKeys.userName, user.fullName);
    await prefs.setString(StorageKeys.userRole, user.role);
  }

  Future<void> _clearUserPrefs() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(StorageKeys.userId);
    await prefs.remove(StorageKeys.userEmail);
    await prefs.remove(StorageKeys.userName);
    await prefs.remove(StorageKeys.userRole);
  }
}

final dioClientProvider = Provider<DioClient>((ref) {
  return DioClient();
});

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return AuthRepository(dioClient);
});

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final repository = ref.watch(authRepositoryProvider);
  final dioClient = ref.watch(dioClientProvider);
  return AuthNotifier(repository, dioClient);
});
