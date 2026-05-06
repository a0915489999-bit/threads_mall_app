import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const ThreadsMall());

class ThreadsMall extends StatelessWidget {
  const ThreadsMall({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(scaffoldBackgroundColor: Colors.black),
      home: const ProductPage(),
    );
  }
}

class ProductPage extends StatefulWidget {
  const ProductPage({super.key});

  @override
  State<ProductPage> createState() => _ProductPageState();
}

class _ProductPageState extends State<ProductPage> {
  Map<String, dynamic>? productData;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchProduct();
  }

// 修改前的本地測試
// final String url = 'http://127.0.0.1:8000/product/product_001';

// 修改後的雲端正式版
final String url = 'https://threads-mall-backend-ni-de-ming-zi.onrender.com/product/product_001';

Future<void> fetchProductData() async {
  try {
    final response = await http.get(Uri.parse(url));
    
    if (response.statusCode == 200) {
      // 解析雲端傳回的 JSON
      var data = json.decode(response.body);
      print("成功獲取雲端商品：${data['name']}");
      
      setState(() {
        productName = data['name'];
        price = data['price'];
        // 記得加上你設計的 5% 佣金邏輯！
      });
    }
  } catch (e) {
    print("連線至 Render 失敗: $e");
  }
}
  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Scaffold(body: Center(child: CircularProgressIndicator(color: Colors.white)));
    if (productData == null) return const Scaffold(body: Center(child: Text("商品載入失敗，請檢查網路")));

    return Scaffold(
      appBar: AppBar(backgroundColor: Colors.black, title: const Text('商品詳情')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            ListTile(
              leading: const CircleAvatar(child: Icon(Icons.person)),
              title: Text(productData!['seller']),
              subtitle: const Text('Verified Seller'),
            ),
            Container(
              height: 300,
              width: double.infinity,
              color: const Color(0xFF1E1E1E),
              child: const Icon(Icons.shopping_bag, size: 100),
            ),
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(productData!['name'], style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Text('NT\$ ${productData!['price']}', style: const TextStyle(fontSize: 22, color: Colors.greenAccent)),
                  const SizedBox(height: 20),
                  Text(productData!['description'], style: const TextStyle(color: Colors.white70)),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(15),
          child: ElevatedButton(
            onPressed: () => _showCheckout(context),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.white, foregroundColor: Colors.black),
            child: const Text('立即購買', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
        ),
      ),
    );
  }

  void _showCheckout(BuildContext context) {
    int price = productData!['price'];
    int fee = (price * 0.05).toInt();

    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF121212),
      builder: (context) => Padding(
        padding: const EdgeInsets.all(30),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('費用明細', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            _infoRow('商品價格', 'NT\$ $price'),
            _infoRow('5% 服務費', 'NT\$ $fee'),
            const Divider(),
            _infoRow('總金額', 'NT\$ ${price + fee}', isBold: true),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: () {}, child: const Text('前往結帳'))
          ],
        ),
      ),
    );
  }

  Widget _infoRow(String label, String val, {bool isBold = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [Text(label), Text(val, style: TextStyle(fontWeight: isBold ? FontWeight.bold : FontWeight.normal))],
      ),
    );
  }
}