import 'dart:developer' as developer;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dio/dio.dart' as dio;
import '../../../../core/constants/api_constants.dart';
import '../../../../core/constants/storage_keys.dart';

/// Mapping between display labels (shown in UI) and canonical API values (sent to backend).
const Map<String, String> deliveryModeDisplayToApi = {
  'Text': 'Text',
  'Audio': 'Audio',
  'Text + Audio': 'TextPlusAudio',
};

/// Mapping between canonical API values and display labels.
const Map<String, String> deliveryModeApiToDisplay = {
  'Text': 'Text',
  'Audio': 'Audio',
  'TextPlusAudio': 'Text + Audio',
};

/// Normalize any delivery mode value (display label, legacy format, or canonical)
/// to the canonical API value.
String normalizeDeliveryMode(String mode) {
  // Check if it's already a canonical API value
  if (deliveryModeApiToDisplay.containsKey(mode)) {
    return mode;
  }
  // Check if it's a display label
  final apiValue = deliveryModeDisplayToApi[mode];
  if (apiValue != null) {
    return apiValue;
  }
  // Handle legacy formats
  final lower = mode.toLowerCase().trim();
  if (lower == 'text') return 'Text';
  if (lower == 'audio') return 'Audio';
  if (lower == 'text + audio' || lower == 'textplusaudio' || lower == 'text_and_audio') {
    return 'TextPlusAudio';
  }
  // Default to Text
  return 'Text';
}

class SettingsState {
  final ThemeMode themeMode;
  final String language;
  final String deliveryMode;
  final bool notificationsEnabled;
  final double textScale;
  final bool highContrast;
  final bool isLoading;
  final String? error;
  final String? successMessage;

  const SettingsState({
    this.themeMode = ThemeMode.system,
    this.language = 'English',
    this.deliveryMode = 'Text',
    this.notificationsEnabled = true,
    this.textScale = 1.0,
    this.highContrast = false,
    this.isLoading = false,
    this.error,
    this.successMessage,
  });

  SettingsState copyWith({
    ThemeMode? themeMode,
    String? language,
    String? deliveryMode,
    bool? notificationsEnabled,
    double? textScale,
    bool? highContrast,
    bool? isLoading,
    String? error,
    String? successMessage,
    bool clearError = false,
    bool clearSuccess = false,
  }) {
    return SettingsState(
      themeMode: themeMode ?? this.themeMode,
      language: language ?? this.language,
      deliveryMode: deliveryMode ?? this.deliveryMode,
      notificationsEnabled: notificationsEnabled ?? this.notificationsEnabled,
      textScale: textScale ?? this.textScale,
      highContrast: highContrast ?? this.highContrast,
      isLoading: isLoading ?? this.isLoading,
      error: clearError ? null : (error ?? this.error),
      successMessage: clearSuccess ? null : (successMessage ?? this.successMessage),
    );
  }
}

class SettingsNotifier extends StateNotifier<SettingsState> {
  SettingsNotifier() : super(const SettingsState()) {
    _load();
  }

  dio.Dio _createClient() {
    return dio.Dio(dio.BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ));
  }

  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(StorageKeys.accessToken);
  }

  // ---------------------------------------------------------------------------
  // LOAD: Local first (instant UI), then backend overwrites (source of truth)
  // ---------------------------------------------------------------------------
  Future<void> _load() async {
    final prefs = await SharedPreferences.getInstance();

    // Step 1: Load from local SharedPreferences for instant UI
    final themeIndex = prefs.getInt('themeMode') ?? 0;
    final lang = prefs.getString(StorageKeys.language) ?? 'English';
    final delivery = prefs.getString(StorageKeys.deliveryMode) ?? 'Text';
    final notifs = prefs.getBool('notifications') ?? true;
    final textScale = prefs.getDouble('textScale') ?? 1.0;
    final highContrast = prefs.getBool('highContrast') ?? false;

    state = SettingsState(
      themeMode: ThemeMode.values[themeIndex],
      language: lang,
      deliveryMode: delivery,
      notificationsEnabled: notifs,
      textScale: textScale,
      highContrast: highContrast,
    );

    developer.log('Settings loaded from local: language=$lang, delivery=$delivery');

    // Step 2: Load from backend (source of truth) and overwrite local
    await _loadFromBackend();
  }

  Future<void> _loadFromBackend() async {
    final token = await _getToken();
    if (token == null) {
      developer.log('No auth token, skipping backend load');
      return;
    }

    try {
      final client = _createClient();
      final response = await client.get(
        '/preferences/me',
        options: dio.Options(headers: {'Authorization': 'Bearer $token'}),
      );

      final data = response.data;
      if (data is Map && data['success'] == true && data['data'] != null) {
        final prefData = data['data'] as Map;
        final backendLang = prefData['preferred_language'] as String? ?? state.language;
        final backendDelivery = prefData['delivery_mode'] as String? ?? state.deliveryMode;

        // Overwrite local state with backend values (backend is source of truth)
        state = state.copyWith(
          language: backendLang,
          deliveryMode: backendDelivery,
        );

        // Sync to local SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString(StorageKeys.language, backendLang);
        await prefs.setString(StorageKeys.deliveryMode, backendDelivery);

        developer.log('Backend load: language=$backendLang, delivery=$backendDelivery');
      }
    } catch (e) {
      developer.log('Backend load failed, using local values: $e');
    }
  }

  // ---------------------------------------------------------------------------
  // SAVE: Write to backend first, then confirm to local
  // ---------------------------------------------------------------------------
  Future<void> _saveToBackend({String? language, String? deliveryMode}) async {
    final token = await _getToken();
    if (token == null) {
      developer.log('No auth token, skipping backend save');
      return;
    }

    final payload = <String, dynamic>{};
    if (language != null) payload['preferred_language'] = language;
    if (deliveryMode != null) payload['delivery_mode'] = deliveryMode;

    if (payload.isEmpty) return;

    developer.log('Saving to backend: $payload');

    try {
      final client = _createClient();
      final response = await client.put(
        '/preferences/me',
        data: payload,
        options: dio.Options(headers: {'Authorization': 'Bearer $token'}),
      );

      final responseData = response.data;
      if (responseData is Map && responseData['success'] == true) {
        developer.log('Backend save OK: ${responseData['message']}');

        // Confirm from backend response
        final prefData = responseData['data'] as Map?;
        if (prefData != null) {
          final confirmedLang = prefData['preferred_language'] as String? ?? language;
          final confirmedDelivery = prefData['delivery_mode'] as String? ?? deliveryMode;

          // Write confirmed values to local
          final prefs = await SharedPreferences.getInstance();
          if (confirmedLang != null) await prefs.setString(StorageKeys.language, confirmedLang);
          if (confirmedDelivery != null) await prefs.setString(StorageKeys.deliveryMode, confirmedDelivery);

          state = state.copyWith(
            language: confirmedLang ?? state.language,
            deliveryMode: confirmedDelivery ?? state.deliveryMode,
            successMessage: 'Settings saved',
            clearError: true,
          );
          developer.log('Confirmed: language=$confirmedLang, delivery=$confirmedDelivery');
        }
      } else {
        final errorMsg = responseData?['message'] ?? 'Unknown error';
        state = state.copyWith(error: 'Failed to save: $errorMsg', clearSuccess: true);
        developer.log('Backend save failed: $errorMsg');
      }
    } on dio.DioException catch (e) {
      final msg = e.response?.data?['message'] ?? e.message ?? 'Network error';
      state = state.copyWith(error: 'Save failed: $msg', clearSuccess: true);
      developer.log('Dio error: $msg');
    } catch (e) {
      state = state.copyWith(error: 'Save failed: $e', clearSuccess: true);
      developer.log('Unexpected error: $e');
    }
  }

  // ---------------------------------------------------------------------------
  // USER ACTIONS
  // ---------------------------------------------------------------------------
  Future<void> setThemeMode(ThemeMode mode) async {
    state = state.copyWith(themeMode: mode, clearError: true, clearSuccess: true);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('themeMode', mode.index);
  }

  Future<void> setLanguage(String lang) async {
    final previous = state.language;
    state = state.copyWith(language: lang, isLoading: true, clearError: true, clearSuccess: true);

    // Write to local immediately for instant UI
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(StorageKeys.language, lang);

    developer.log('Language changed: $previous -> $lang');

    // Save to backend (source of truth)
    await _saveToBackend(language: lang);
    state = state.copyWith(isLoading: false);
  }

  Future<void> setDeliveryMode(String mode) async {
    final previous = state.deliveryMode;
    state = state.copyWith(deliveryMode: mode, isLoading: true, clearError: true, clearSuccess: true);

    // Write to local immediately for instant UI
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(StorageKeys.deliveryMode, mode);

    developer.log('Delivery mode changed: $previous -> $mode');

    // Save to backend (source of truth)
    await _saveToBackend(deliveryMode: mode);
    state = state.copyWith(isLoading: false);
  }

  Future<void> toggleNotifications(bool value) async {
    state = state.copyWith(notificationsEnabled: value, clearError: true, clearSuccess: true);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('notifications', value);
  }

  Future<void> setTextScale(double scale) async {
    state = state.copyWith(textScale: scale, clearError: true, clearSuccess: true);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('textScale', scale);
  }

  Future<void> toggleHighContrast(bool value) async {
    state = state.copyWith(highContrast: value, clearError: true, clearSuccess: true);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('highContrast', value);
  }

  void clearMessages() {
    state = state.copyWith(clearError: true, clearSuccess: true);
  }
}

final settingsProvider = StateNotifierProvider<SettingsNotifier, SettingsState>((ref) {
  return SettingsNotifier();
});
