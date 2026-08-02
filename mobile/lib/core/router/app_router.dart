import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../features/accommodation/presentation/screens/my_accommodation_screen.dart';
import '../../features/ai_chat/presentation/screens/ai_chat_screen.dart';
import '../../features/announcement/presentation/screens/announcements_screen.dart';
import '../../features/audio_center/presentation/screens/audio_center_screen.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../../features/flight/presentation/screens/my_flight_screen.dart';
import '../../features/notification_center/presentation/screens/notification_center_screen.dart';
import '../../features/package/presentation/screens/my_package_screen.dart';
import '../../features/settings/presentation/screens/settings_screen.dart';
import '../../features/splash/presentation/screens/splash_screen.dart';
import '../../features/transport/presentation/screens/my_transport_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(path: '/', builder: (context, state) => const SplashScreen()),
      GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
      GoRoute(path: '/dashboard', builder: (context, state) => const DashboardScreen()),
      GoRoute(path: '/package', builder: (context, state) => const MyPackageScreen()),
      GoRoute(path: '/flight', builder: (context, state) => const MyFlightScreen()),
      GoRoute(path: '/accommodation', builder: (context, state) => const MyAccommodationScreen()),
      GoRoute(path: '/transport', builder: (context, state) => const MyTransportScreen()),
      GoRoute(path: '/announcements', builder: (context, state) => const AnnouncementsScreen()),
      GoRoute(path: '/notifications', builder: (context, state) => const NotificationCenterScreen()),
      GoRoute(path: '/ai-chat', builder: (context, state) => const AiChatScreen()),
      GoRoute(path: '/audio', builder: (context, state) => const AudioCenterScreen()),
      GoRoute(path: '/settings', builder: (context, state) => const SettingsScreen()),
    ],
    redirect: (context, state) {
      final status = authState.status;
      final location = state.matchedLocation;
      if (status == AuthStatus.initial) return location == '/' ? null : '/';
      final isAuth = status == AuthStatus.authenticated;
      final isLoginRoute = location == '/login';
      if (!isAuth && !isLoginRoute) return '/login';
      if (isAuth && isLoginRoute) return '/dashboard';
      return null;
    },
  );
});
