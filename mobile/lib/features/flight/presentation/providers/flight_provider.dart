import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../dashboard/data/models/models.dart';

final selectedFlightProvider = StateProvider<Flight?>((ref) => null);
