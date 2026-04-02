import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const BudgetApp());
}

class BudgetApp extends StatelessWidget {
  const BudgetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Budget Predictor',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const PredictPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class PredictPage extends StatefulWidget {
  const PredictPage({super.key});

  @override
  State<PredictPage> createState() => _PredictPageState();
}

class _PredictPageState extends State<PredictPage> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  String _result = 'Enter details and tap Predict.';
  bool _loading = false;

  // Override at build time with: flutter run --dart-define=API_BASE=https://your-api.onrender.com
  static const String apiBase =
      String.fromEnvironment('API_BASE', defaultValue: 'http://127.0.0.1:8000');

  Future<void> _predict() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _result = 'Predicting...';
    });

    final uri = Uri.parse('$apiBase/predict');
    final body = jsonEncode({
      'title': _titleController.text.trim(),
      'description': _descriptionController.text.trim(),
    });

    try {
      final resp = await http
          .post(uri, headers: {'Content-Type': 'application/json'}, body: body)
          .timeout(const Duration(seconds: 15));

      if (resp.statusCode == 200) {
        final data = jsonDecode(resp.body) as Map<String, dynamic>;
        final num budget = data['predicted_budget'] as num;
        final modelName = data['model']?.toString() ?? 'unknown';
        setState(() {
          _result =
              "Predicted budget: ${budget.toStringAsFixed(2)}\nModel: $modelName";
        });
      } else {
        setState(() {
          _result = 'Error ${resp.statusCode}: ${resp.body}';
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Request failed: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Upwork Budget Predictor'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: 'Title',
                  border: OutlineInputBorder(),
                ),
                maxLength: 200,
                validator: (v) =>
                    (v == null || v.trim().length < 3) ? 'Min 3 characters' : null,
              ),
              const SizedBox(height: 12),
              Expanded(
                child: TextFormField(
                  controller: _descriptionController,
                  decoration: const InputDecoration(
                    labelText: 'Description',
                    alignLabelWithHint: true,
                    border: OutlineInputBorder(),
                  ),
                  maxLines: null,
                  expands: true,
                  validator: (v) =>
                      (v == null || v.trim().length < 10) ? 'Min 10 characters' : null,
                ),
              ),
              const SizedBox(height: 12),
              FilledButton.icon(
                onPressed: _loading ? null : _predict,
                icon: _loading
                    ? const SizedBox(
                        height: 16,
                        width: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.analytics),
                label: const Text('Predict'),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                child: Text(
                  _result,
                  style: const TextStyle(fontSize: 14),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
