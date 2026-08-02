import 'package:flutter/material.dart';

class TermsOfServiceScreen extends StatelessWidget {
  const TermsOfServiceScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Terms of Service'),
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
              'Hajj Pilgrim Portal — Terms of Service',
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
              '1. Acceptance of Terms',
              'By downloading, installing, or using the Hajj Pilgrim Portal ("the App"), you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use the App. These terms constitute a legally binding agreement between you and the Hajj Pilgrim Portal team.',
            ),
            _buildSection(
              theme,
              '2. Use of the Application',
              'The App is designed to assist Hajj pilgrims with:\n\n'
              '• Managing travel itineraries and schedules\n'
              '• Accessing flight, accommodation, and transport information\n'
              '• Receiving important notifications and announcements\n'
              '• Interacting with an AI-powered pilgrimage assistant\n'
              '• Accessing audio guides and announcements\n\n'
              'You may use the App only for its intended purpose and in compliance with all applicable laws and regulations.',
            ),
            _buildSection(
              theme,
              '3. User Responsibilities',
              'You are responsible for:\n\n'
              '• Maintaining the confidentiality of your login credentials\n'
              '• All activities that occur under your account\n'
              '• Providing accurate and up-to-date personal information\n'
              '• Notifying us immediately of any unauthorized use of your account\n'
              '• Using the App in a respectful and appropriate manner\n'
              '• Not attempting to disrupt or compromise the App\'s security',
            ),
            _buildSection(
              theme,
              '4. Privacy',
              'Your use of the App is also governed by our Privacy Policy, which describes how we collect, use, and protect your personal information. By using the App, you consent to the data practices described in the Privacy Policy. Please review it carefully.',
            ),
            _buildSection(
              theme,
              '5. AI Assistant Disclaimer',
              'The App includes an AI-powered assistant powered by Google Gemini. Please note:\n\n'
              '• AI responses are generated algorithmically and may contain errors\n'
              '• AI responses should not be considered professional religious or medical advice\n'
              '• Critical travel decisions should be verified with official sources\n'
              '• The AI assistant may not always be available due to technical limitations\n'
              '• We are not responsible for decisions made based on AI-generated content',
            ),
            _buildSection(
              theme,
              '6. Accuracy of Information',
              'While we strive to provide accurate and timely information:\n\n'
              '• Flight schedules, hotel assignments, and transport details are subject to change\n'
              '• We make reasonable efforts to keep information current\n'
              '• Users should verify critical information with official sources\n'
              '• We are not liable for inaccuracies in third-party data\n'
              '• Notification timing may vary based on system conditions',
            ),
            _buildSection(
              theme,
              '7. Availability',
              'We aim to provide uninterrupted service, but:\n\n'
              '• The App requires an internet connection for most features\n'
              '• Scheduled maintenance may temporarily limit access\n'
              '• Third-party service outages may affect functionality\n'
              '• We do not guarantee 100% uptime\n'
              '• We will endeavor to notify users of planned downtime',
            ),
            _buildSection(
              theme,
              '8. Limitation of Liability',
              'To the maximum extent permitted by law:\n\n'
              '• The App is provided "as is" without warranties of any kind\n'
              '• We are not liable for any indirect, incidental, or consequential damages\n'
              '• Our total liability shall not exceed the amount paid for the App (if applicable)\n'
              '• We are not responsible for travel disruptions, missed flights, or similar incidents\n'
              '• Users rely on the App at their own risk for non-critical information',
            ),
            _buildSection(
              theme,
              '9. Termination',
              'We reserve the right to:\n\n'
              '• Suspend or terminate your access to the App at any time\n'
              '• Remove content that violates these terms\n'
              '• Deactivate accounts that are inactive or compromised\n\n'
              'You may terminate your use of the App at any time by uninstalling it from your device and contacting us to delete your account.',
            ),
            _buildSection(
              theme,
              '10. Contact',
              'For questions about these Terms of Service:\n\n'
              'Hajj Pilgrim Portal Team\n'
              'Email: support@hajjpilgrim.ng\n'
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
