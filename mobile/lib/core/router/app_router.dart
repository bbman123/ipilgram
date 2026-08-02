import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../../features/splash/presentation/screens/splash_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),
    ],
    redirect: (context, state) {
      final status = authState.status;
      final location = state.matchedLocation;

      // Still initializing — stay on splash
      if (status == AuthStatus.initial) {
        return location == '/' ? null : '/';
      }

      final isAuth = status == AuthStatus.authenticated;
      final isLoginRoute = location == '/login';

      // Not authenticated → force to login
      if (!isAuth && !isLoginRoute) return '/login';

      // Authenticated but on login → push to dashboard
      if (isAuth && isLoginRoute) return '/dashboard';

      return null;
    },
  );
});
