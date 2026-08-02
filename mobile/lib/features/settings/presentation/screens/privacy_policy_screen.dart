import 'package:flutter/material.dart';

class PrivacyPolicyScreen extends StatelessWidget {
  const PrivacyPolicyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy Policy'),
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                theme.colorScheme.primary,
                theme.colorScheme.primary.withValues(alpha: 0.7),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Hajj Pilgrim Portal — Privacy Policy',
              style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              'Version 1.0.0 • Effective Date: August 2, 2026',
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            ),
            const SizedBox(height: 24),
            _buildSection(
              theme,
              '1. Introduction',
              'Welcome to the Hajj Pilgrim Portal ("the App"). This Privacy Policy describes how we collect, use, disclose, and protect your personal information when you use our mobile application designed to assist pilgrims during their Hajj journey. By using the App, you consent to the practices described in this policy.',
            ),
            _buildSection(
              theme,
              '2. Information We Collect',
              'We collect the following types of information:\n\n'
              '• Personal Identification Information: Full name, email address, phone number, nationality, passport number, and emergency contact details.\n'
              '• Travel Information: Flight details, accommodation assignments, transport arrangements, and package selections.\n'
              '• Usage Data: App interaction patterns, feature usage, session duration, and device information.\n'
              '• Location Data: With your explicit consent, we may collect real-time location data to provide location-based services such as navigation and nearby facility alerts.\n'
              '• Audio Data: Voice queries submitted to the AI assistant are processed to generate responses and audio output.',
            ),
            _buildSection(
              theme,
              '3. How We Use Your Information',
              'Your information is used to:\n\n'
              '• Provide personalized pilgrimage management services\n'
              '• Display your flight, accommodation, and transport details\n'
              '• Send timely notifications and reminders relevant to your journey\n'
              '• Power the AI assistant to answer your pilgrimage-related queries\n'
              '• Generate audio versions of announcements and guidance\n'
              '• Improve app functionality and user experience\n'
              '• Ensure security and prevent unauthorized access',
            ),
            _buildSection(
              theme,
              '4. Data Security',
              'We implement industry-standard security measures to protect your data, including:\n\n'
              '• End-to-end encryption for data in transit (TLS/SSL)\n'
              '• Encrypted storage of authentication tokens\n'
              '• Secure API communication with JWT-based authentication\n'
              '• Regular security audits and vulnerability assessments\n'
              '• Access controls limiting data access to authorized personnel only',
            ),
            _buildSection(
              theme,
              '5. Third-Party Services',
              'The App may integrate with the following third-party services:\n\n'
              '• Google Gemini AI: For powering the AI assistant feature. Queries are processed in accordance with Google\'s privacy policy.\n'
              '• Firebase Cloud Messaging: For delivering push notifications.\n'
              '• Hosting Providers: Our backend infrastructure is hosted on secure cloud platforms.\n\n'
              'These third parties have their own privacy policies governing the use of your data.',
            ),
            _buildSection(
              theme,
              '6. Location Data',
              'With your explicit consent, we collect and use location data to:\n\n'
              '• Provide navigation assistance to religious sites\n'
              '• Alert you to nearby facilities and services\n'
              '• Enable location-based notifications\n\n'
              'You may disable location services at any time through your device settings. Disabling location services may limit certain app features.',
            ),
            _buildSection(
              theme,
              '7. Notifications',
              'We send notifications to keep you informed about:\n\n'
              '• Flight reminders and gate changes\n'
              '• Accommodation check-in/check-out updates\n'
              '• Transport pickup schedules\n'
              '• Important Hajj-related announcements\n'
              '• Safety alerts and emergency information\n\n'
              'You can manage notification preferences in the App settings.',
            ),
            _buildSection(
              theme,
              '8. Your Rights',
              'You have the right to:\n\n'
              '• Access your personal data stored in the App\n'
              '• Request correction of inaccurate data\n'
              '• Request deletion of your data\n'
              '• Opt out of non-essential data collection\n'
              '• Withdraw consent for location tracking\n'
              '• Export your data in a portable format\n\n'
              'To exercise these rights, please contact us using the information below.',
            ),
            _buildSection(
              theme,
              '9. Contact Information',
              'If you have questions about this Privacy Policy or wish to exercise your rights, please contact:\n\n'
              'Hajj Pilgrim Portal Team\n'
              'Email: privacy@hajjpilgrim.ng\n'
              'Website: https://ipilgram.onrender.com',
            ),
            const SizedBox(height: 32),
            Text(
              '© 2026 Hajj Pilgrim Portal. All rights reserved.',
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildSection(ThemeData theme, String title, String body) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 8),
          Text(
            body,
            style: theme.textTheme.bodyMedium?.copyWith(
              height: 1.6,
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }
}
