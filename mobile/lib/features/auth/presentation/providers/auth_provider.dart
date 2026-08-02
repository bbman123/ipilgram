import 'package:flutter/foundation.dart';
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

class AuthRefreshNotifier extends ChangeNotifier {
  AuthStatus _status = AuthStatus.initial;

  AuthStatus get status => _status;

  void update(AuthStatus newStatus) {
    if (_status != newStatus) {
      _status = newStatus;
      notifyListeners();
    }
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;
  final DioClient _dioClient;
  final AuthRefreshNotifier _refreshNotifier;

  AuthNotifier(this._repository, this._dioClient, this._refreshNotifier)
      : super(const AuthState()) {
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
    _refreshNotifier.update(state.status);
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(status: AuthStatus.loading, error: null);
    _refreshNotifier.update(AuthStatus.loading);
    try {
      await _repository.login(email, password);
      final user = await _repository.getMe();
      await _saveUserPrefs(user);
      state = AuthState(status: AuthStatus.authenticated, user: user);
    } catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      state = AuthState(status: AuthStatus.error, error: message);
    }
    _refreshNotifier.update(state.status);
  }

  Future<void> logout() async {
    await _repository.logout();
    await _clearUserPrefs();
    state = const AuthState(status: AuthStatus.unauthenticated);
    _refreshNotifier.update(AuthStatus.unauthenticated);
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

final authRefreshProvider = Provider<AuthRefreshNotifier>((ref) {
  return AuthRefreshNotifier();
});

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
  final refreshNotifier = ref.watch(authRefreshProvider);
  return AuthNotifier(repository, dioClient, refreshNotifier);
});
