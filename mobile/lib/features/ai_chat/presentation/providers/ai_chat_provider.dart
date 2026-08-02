import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../data/repositories/ai_chat_repository.dart';

final aiChatRepositoryProvider = Provider<AiChatRepository>((ref) {
  final dio = ref.watch(dioClientProvider).dio;
  return AiChatRepository(dio);
});

class AiChatState {
  final bool isLoading;
  final List<AiChatMessage> messages;
  final String? error;

  const AiChatState({
    this.isLoading = false,
    this.messages = const [],
    this.error,
  });

  AiChatState copyWith({
    bool? isLoading,
    List<AiChatMessage>? messages,
    String? error,
  }) {
    return AiChatState(
      isLoading: isLoading ?? this.isLoading,
      messages: messages ?? this.messages,
      error: error,
    );
  }
}

class AiChatNotifier extends StateNotifier<AiChatState> {
  final AiChatRepository _repo;

  AiChatNotifier(this._repo) : super(const AiChatState()) {
    state = AiChatState(
      messages: [
        AiChatMessage(
          id: 'welcome',
          text: 'Assalamu Alaikum! I\'m your Hajj AI assistant. Ask me anything about your pilgrimage — flight details, accommodation, transport, or general guidance.',
          isUser: false,
          timestamp: DateTime.now(),
        ),
      ],
    );
  }

  Future<void> send(String text) async {
    if (text.trim().isEmpty || state.isLoading) return;

    final userMsg = AiChatMessage(
      id: 'user_${DateTime.now().millisecondsSinceEpoch}',
      text: text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMsg],
      isLoading: true,
      error: null,
    );

    try {
      final result = await _repo.ask(text.trim());
      final aiMsg = AiChatMessage(
        id: 'ai_${DateTime.now().millisecondsSinceEpoch}',
        text: result['response'] as String? ?? 'I couldn\'t process that request.',
        isUser: false,
        timestamp: DateTime.now(),
      );
      state = state.copyWith(
        messages: [...state.messages, aiMsg],
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to get response. Please try again.',
      );
    }
  }

  Future<void> sendWithAudio(String text) async {
    if (text.trim().isEmpty || state.isLoading) return;

    final userMsg = AiChatMessage(
      id: 'user_${DateTime.now().millisecondsSinceEpoch}',
      text: text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMsg],
      isLoading: true,
      error: null,
    );

    try {
      final audioPath = await _repo.askAudio(text.trim());
      final aiMsg = AiChatMessage(
        id: 'ai_${DateTime.now().millisecondsSinceEpoch}',
        text: 'Audio response generated',
        isUser: false,
        audioUrl: audioPath,
        timestamp: DateTime.now(),
      );
      state = state.copyWith(
        messages: [...state.messages, aiMsg],
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to generate audio. Please try again.',
      );
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

final aiChatProvider = StateNotifierProvider<AiChatNotifier, AiChatState>((ref) {
  final repo = ref.watch(aiChatRepositoryProvider);
  return AiChatNotifier(repo);
});
