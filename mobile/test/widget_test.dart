import 'package:flutter_test/flutter_test.dart';
import 'package:hajj_pilgrims/main.dart';

void main() {
  testWidgets('App renders splash screen', (WidgetTester tester) async {
    await tester.pumpWidget(const HajjPilgrimApp());
    await tester.pumpAndSettle();
    expect(find.text('Hajj Pilgrim'), findsOneWidget);
  });
}
