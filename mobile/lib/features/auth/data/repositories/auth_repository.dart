import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../../core/constants/constants.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/network/dio_client.dart';
import '../models/models.dart';

class AuthRepository {
  final DioClient _dioClient;

  AuthRepository(this._dioClient);

  Future<AuthTokens> login(String email, String password) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.loginEndpoint,
        data: {'email': email, 'password': password},
      );

      final tokens = AuthTokens.fromJson(response.data as Map<String, dynamic>);
      _dioClient.setTokens(
        accessToken: tokens.accessToken,
        refreshToken: tokens.refreshToken,
      );
      await _persistTokens(tokens);
      return tokens;
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<User> getMe() async {
    try {
      final response = await _dioClient.dio.get(ApiConstants.meEndpoint);
      final body = response.data as Map<String, dynamic>;
      final data = body['data'] as Map<String, dynamic>;
      return User.fromJson(data);
    } on DioException catch (e) {
      throw AppException.fromDioError(e);
    }
  }

  Future<void> logout() async {
    final refreshToken = _dioClient.refreshToken;
    try {
      await _dioClient.dio.post(
        ApiConstants.logoutEndpoint,
        data: {'refresh_token': refreshToken},
      );
    } on DioException {
      // Logout failure is non-critical; tokens will be cleared regardless
    } finally {
      _dioClient.clearTokens();
      await _dioClient.clearPersistedTokens();
    }
  }

  Future<bool> tryAutoLogin() async {
    await _dioClient.restoreTokens();
    return _dioClient.accessToken != null;
  }

  Future<void> _persistTokens(AuthTokens tokens) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(StorageKeys.accessToken, tokens.accessToken);
    await prefs.setString(StorageKeys.refreshToken, tokens.refreshToken);
  }
}
