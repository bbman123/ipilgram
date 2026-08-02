import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../providers/settings_provider.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final theme = Theme.of(context);
    final size = MediaQuery.sizeOf(context);
    final isWide = size.width > 600;

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 140,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('Settings'),
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.blueGrey.shade800,
                      Colors.blueGrey.shade600,
                      Colors.blueGrey.shade400,
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                child: Stack(
                  children: [
                    Positioned(
                      right: -20,
                      bottom: -20,
                      child: Icon(Icons.settings, size: 120, color: Colors.white.withValues(alpha: 0.08)),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SliverPadding(
            padding: EdgeInsets.symmetric(
              horizontal: isWide ? size.width * 0.2 : 0,
              vertical: 8,
            ),
            sliver: SliverList.list(
              children: [
                _SectionHeader(title: 'Appearance'),
                _ThemeTile(
                  currentMode: settings.themeMode,
                  onChanged: (mode) => ref.read(settingsProvider.notifier).setThemeMode(mode),
                ),
                _TextSizeTile(
                  currentScale: settings.textScale,
                  onChanged: (s) => ref.read(settingsProvider.notifier).setTextScale(s),
                ),
                _SwitchTile(
                  icon: Icons.contrast,
                  title: 'High Contrast',
                  subtitle: 'Increase contrast for better visibility',
                  value: settings.highContrast,
                  onChanged: (v) => ref.read(settingsProvider.notifier).toggleHighContrast(v),
                ),
                const Divider(height: 1),
                _SectionHeader(title: 'Language'),
                _LanguageTile(
                  currentLanguage: settings.language,
                  onChanged: (lang) => ref.read(settingsProvider.notifier).setLanguage(lang),
                ),
                const Divider(height: 1),
                _SectionHeader(title: 'Notifications'),
                _SwitchTile(
                  icon: Icons.notifications_active,
                  title: 'Push Notifications',
                  subtitle: 'Receive alerts and updates',
                  value: settings.notificationsEnabled,
                  onChanged: (v) => ref.read(settingsProvider.notifier).toggleNotifications(v),
                ),
                const Divider(height: 1),
                _SectionHeader(title: 'About'),
                _InfoTile(
                  icon: Icons.info_outline,
                  title: 'App Version',
                  trailing: '1.0.0+1',
                ),
                _TapTile(
                  icon: Icons.privacy_tip_outlined,
                  title: 'Privacy Policy',
                  onTap: () => context.push('/privacy'),
                ),
                _TapTile(
                  icon: Icons.description_outlined,
                  title: 'Terms of Service',
                  onTap: () => context.push('/terms'),
                ),
                const SizedBox(height: 24),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  child: FilledButton.icon(
                    onPressed: () async {
                      final confirm = await showDialog<bool>(
                        context: context,
                        builder: (ctx) => AlertDialog(
                          title: const Text('Logout'),
                          content: const Text('Are you sure you want to logout?'),
                          actions: [
                            TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
                            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Logout')),
                          ],
                        ),
                      );
                      if (confirm == true && context.mounted) {
                        await ref.read(authProvider.notifier).logout();
                      }
                    },
                    icon: const Icon(Icons.logout),
                    label: const Text('Logout'),
                    style: FilledButton.styleFrom(
                      backgroundColor: theme.colorScheme.error,
                      minimumSize: const Size(double.infinity, 48),
                    ),
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  const _SectionHeader({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
      child: Text(
        title.toUpperCase(),
        style: Theme.of(context).textTheme.labelSmall?.copyWith(
          color: Theme.of(context).colorScheme.primary,
          fontWeight: FontWeight.w700,
          letterSpacing: 1.2,
        ),
      ),
    );
  }
}

class _ThemeTile extends StatelessWidget {
  final ThemeMode currentMode;
  final ValueChanged<ThemeMode> onChanged;

  const _ThemeTile({required this.currentMode, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const Icon(Icons.dark_mode_outlined),
      title: const Text('Theme'),
      trailing: SegmentedButton<ThemeMode>(
        segments: const [
          ButtonSegment(value: ThemeMode.light, icon: Icon(Icons.light_mode, size: 18)),
          ButtonSegment(value: ThemeMode.dark, icon: Icon(Icons.dark_mode, size: 18)),
          ButtonSegment(value: ThemeMode.system, icon: Icon(Icons.phone_android, size: 18)),
        ],
        selected: {currentMode},
        onSelectionChanged: (modes) => onChanged(modes.first),
        style: ButtonStyle(
          visualDensity: VisualDensity.compact,
          tapTargetSize: MaterialTapTargetSize.shrinkWrap,
        ),
      ),
    );
  }
}

class _TextSizeTile extends StatelessWidget {
  final double currentScale;
  final ValueChanged<double> onChanged;

  const _TextSizeTile({required this.currentScale, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const Icon(Icons.text_fields),
      title: const Text('Text Size'),
      subtitle: Row(
        children: [
          const Text('A', style: TextStyle(fontSize: 12)),
          Expanded(
            child: Slider(
              value: currentScale,
              min: 0.8,
              max: 1.5,
              divisions: 7,
              label: '${(currentScale * 100).round()}%',
              onChanged: onChanged,
            ),
          ),
          const Text('A', style: TextStyle(fontSize: 20)),
        ],
      ),
    );
  }
}

class _LanguageTile extends StatelessWidget {
  final String currentLanguage;
  final ValueChanged<String> onChanged;

  const _LanguageTile({required this.currentLanguage, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final languages = ['English', 'Hausa', 'Yoruba', 'Igbo', 'Arabic'];
    return ListTile(
      leading: const Icon(Icons.language),
      title: const Text('Language'),
      trailing: DropdownButton<String>(
        value: currentLanguage,
        underline: const SizedBox(),
        items: languages.map((l) => DropdownMenuItem(value: l, child: Text(l))).toList(),
        onChanged: (v) {
          if (v != null) onChanged(v);
        },
      ),
    );
  }
}

class _SwitchTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final bool value;
  final ValueChanged<bool> onChanged;

  const _SwitchTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      secondary: Icon(icon),
      title: Text(title),
      subtitle: Text(subtitle, style: Theme.of(context).textTheme.bodySmall),
      value: value,
      onChanged: onChanged,
    );
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String trailing;

  const _InfoTile({required this.icon, required this.title, required this.trailing});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: Text(
        trailing,
        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }
}

class _TapTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;

  const _TapTile({required this.icon, required this.title, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: const Icon(Icons.chevron_right),
      onTap: onTap,
    );
  }
}
