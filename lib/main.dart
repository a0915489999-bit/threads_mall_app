import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MaterialApp(home: ProductPage()));

class ProductPage extends StatefulWidget {
  const ProductPage({super.key});
  @override
  State<ProductPage> createState() => _ProductPageState();
}

class _ProductPageState extends State<ProductPage> {
  // 🔴 請確保這是你的真實 Render 網址
  final String apiUrl = 'https://threads-mall-api.onrender.com/product/1';
  Map<String, dynamic>? product;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      final response = await http.get(Uri.parse(apiUrl));
      if (response.statusCode == 200) {
        setState(() {
          product = json.decode(response.body);
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
        product = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    if (product == null) return const Scaffold(body: Center(child: Text("載入失敗，請檢查 API")));

    return Scaffold(
      appBar: AppBar(title: const Text("Threads Mall")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 使用 ?? 預防 Null 報錯
            Text(product!['name']?.toString() ?? "無名稱", style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Text("價格: \$${product!['price'] ?? 0}"),
            Text("佣金比例: ${(product!['commission_rate'] ?? 0.0) * 100}%"),
          ],
        ),
      ),
    );
  }
}