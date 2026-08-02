import 'dart:async';

import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/constants.dart';
import '../errors/app_exception.dart';
import 'package:logger/logger.dart';

final logger = Logger();

class DioClient {
  late final Dio _dio;
  String? _accessToken;
  String? _refreshToken;
  bool _isRefreshing = false;
  final List<_QueuedRequest> _queuedRequests = [];

  DioClient() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConstants.baseUrl,
        connectTimeout: ApiConstants.connectTimeout,
        receiveTimeout: ApiConstants.receiveTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.addAll([
      _AuthInterceptor(this),
      _LoggingInterceptor(),
    ]);
  }

  Dio get dio => _dio;

  String? get accessToken => _accessToken;
  String? get refreshToken => _refreshToken;

  void setTokens({required String accessToken, required String refreshToken}) {
    _accessToken = accessToken;
    _refreshToken = refreshToken;
    _dio.options.headers['Authorization'] = 'Bearer $accessToken';
  }

  void clearTokens() {
    _accessToken = null;
    _refreshToken = null;
    _dio.options.headers.remove('Authorization');
  }

  Future<void> restoreTokens() async {
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString(StorageKeys.accessToken);
    _refreshToken = prefs.getString(StorageKeys.refreshToken);
    if (_accessToken != null) {
      _dio.options.headers['Authorization'] = 'Bearer $_accessToken';
    }
  }

  Future<void> _persistTokens() async {
    final prefs = await SharedPreferences.getInstance();
    if (_accessToken != null) await prefs.setString(StorageKeys.accessToken, _accessToken!);
    if (_refreshToken != null) await prefs.setString(StorageKeys.refreshToken, _refreshToken!);
  }

  Future<void> clearPersistedTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(StorageKeys.accessToken);
    await prefs.remove(StorageKeys.refreshToken);
    await prefs.remove(StorageKeys.userId);
    await prefs.remove(StorageKeys.userEmail);
    await prefs.remove(StorageKeys.userName);
    await prefs.remove(StorageKeys.userRole);
  }

  Future<bool> tryRefreshToken() async {
    if (_isRefreshing) return false;
    if (_refreshToken == null) return false;

    _isRefreshing = true;
    try {
      final refreshDio = Dio(BaseOptions(
        baseUrl: ApiConstants.baseUrl,
        connectTimeout: ApiConstants.connectTimeout,
        receiveTimeout: ApiConstants.receiveTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ));

      final response = await refreshDio.post(
        ApiConstants.refreshTokenEndpoint,
        data: {'refresh_token': _refreshToken},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        _accessToken = data['access_token'] as String;
        _refreshToken = data['refresh_token'] as String;
        _dio.options.headers['Authorization'] = 'Bearer $_accessToken';
        await _persistTokens();

        for (final queued in _queuedRequests) {
          queued.options.headers['Authorization'] = 'Bearer $_accessToken';
          _dio.fetch(queued.options).then(queued.completer.complete).catchError(queued.completer.completeError);
        }
        _queuedRequests.clear();

        return true;
      }
      return false;
    } catch (e) {
      return false;
    } finally {
      _isRefreshing = false;
    }
  }
}

class _QueuedRequest {
  final RequestOptions options;
  final Completer<Response> completer;

  _QueuedRequest({required this.options, required this.completer});
}

class _AuthInterceptor extends Interceptor {
  final DioClient _client;

  _AuthInterceptor(this._client);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    if (options.path != ApiConstants.loginEndpoint &&
        options.path != ApiConstants.refreshTokenEndpoint &&
        _client.accessToken != null) {
      options.headers['Authorization'] = 'Bearer ${_client.accessToken}';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401 &&
        err.requestOptions.path != ApiConstants.refreshTokenEndpoint &&
        err.requestOptions.path != ApiConstants.loginEndpoint) {

      if (_client._isRefreshing) {
        final completer = Completer<Response>();
        _client._queuedRequests.add(_QueuedRequest(
          options: err.requestOptions,
          completer: completer,
        ));
        try {
          final response = await completer.future;
          handler.resolve(response);
        } catch (e) {
          handler.next(err);
        }
        return;
      }

      final refreshed = await _client.tryRefreshToken();
      if (refreshed) {
        err.requestOptions.headers['Authorization'] = 'Bearer ${_client.accessToken}';
        final response = await _client.dio.fetch(err.requestOptions);
        handler.resolve(response);
        return;
      }
    }
    handler.next(err);
  }
}

class _LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    logger.d('REQUEST[${options.method}] => PATH: ${options.path}');
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    logger.d('RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    logger.e('ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
    handler.next(err);
  }
}
