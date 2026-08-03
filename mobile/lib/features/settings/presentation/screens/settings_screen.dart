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
                // Status messages
                if (settings.isLoading)
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                    child: LinearProgressIndicator(),
                  ),
                if (settings.successMessage != null)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.check_circle, color: theme.colorScheme.primary, size: 20),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              settings.successMessage!,
                              style: TextStyle(color: theme.colorScheme.onPrimaryContainer),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                if (settings.error != null)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.errorContainer,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.error_outline, color: theme.colorScheme.error, size: 20),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              settings.error!,
                              style: TextStyle(color: theme.colorScheme.onErrorContainer),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

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

                _SectionHeader(title: 'Content Delivery'),
                _DeliveryModeTile(
                  currentMode: settings.deliveryMode,
                  onChanged: (mode) => ref.read(settingsProvider.notifier).setDeliveryMode(mode),
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
    final languages = ['English', 'Arabic', 'Hausa', 'Yoruba', 'Igbo'];
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

class _DeliveryModeTile extends StatelessWidget {
  final String currentMode;
  final ValueChanged<String> onChanged;

  const _DeliveryModeTile({required this.currentMode, required this.onChanged});

  // Display labels shown to the user in the UI
  static const List<String> displayLabels = ['Text', 'Audio', 'Text + Audio'];

  // Canonical API values sent to the backend
  static const List<String> apiValues = ['Text', 'Audio', 'TextPlusAudio'];

  @override
  Widget build(BuildContext context) {
    final icons = [Icons.text_fields, Icons.volume_up, Icons.surround_sound];

    // Find the current display label from the API value
    final currentIndex = apiValues.indexOf(currentMode);
    final selectedDisplay = currentIndex >= 0 ? displayLabels[currentIndex] : displayLabels[0];

    return ListTile(
      leading: const Icon(Icons.delivery_dining),
      title: const Text('Delivery Mode'),
      subtitle: Text(
        'Choose how you receive announcements',
        style: Theme.of(context).textTheme.bodySmall,
      ),
      trailing: DropdownButton<String>(
        value: selectedDisplay,
        underline: const SizedBox(),
        items: displayLabels.asMap().entries.map((entry) {
          return DropdownMenuItem(
            value: entry.value,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(icons[entry.key], size: 18),
                const SizedBox(width: 8),
                Text(entry.value),
              ],
            ),
          );
        }).toList(),
        onChanged: (v) {
          if (v != null) {
            final index = displayLabels.indexOf(v);
            if (index >= 0) onChanged(apiValues[index]);
          }
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
