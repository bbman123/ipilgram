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
import '../../features/settings/presentation/screens/privacy_policy_screen.dart';
import '../../features/settings/presentation/screens/settings_screen.dart';
import '../../features/settings/presentation/screens/terms_of_service_screen.dart';
import '../../features/splash/presentation/screens/splash_screen.dart';
import '../../features/transport/presentation/screens/my_transport_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final refreshNotifier = ref.watch(authRefreshProvider);

  // Eagerly create AuthNotifier so _init() runs and calls _refreshNotifier.update().
  // ref.listen (not ref.watch) ensures GoRouter is NOT recreated on auth state changes.
  ref.listen<AuthState>(authProvider, (_, __) {});

  return GoRouter(
    initialLocation: '/',
    refreshListenable: refreshNotifier,
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
      GoRoute(path: '/privacy', builder: (context, state) => const PrivacyPolicyScreen()),
      GoRoute(path: '/terms', builder: (context, state) => const TermsOfServiceScreen()),
    ],
    redirect: (context, state) {
      final status = refreshNotifier.status;
      final location = state.matchedLocation;

      // Still initializing — stay on splash
      if (status == AuthStatus.initial) {
        return location == '/' ? null : '/';
      }

      final isAuth = status == AuthStatus.authenticated;
      final isLoginRoute = location == '/login';
      final isSplash = location == '/';

      // Not authenticated → force to login
      if (!isAuth && !isLoginRoute) return '/login';

      // Authenticated but on login or splash → push to dashboard
      if (isAuth && (isLoginRoute || isSplash)) return '/dashboard';

      return null;
    },
  );
});
