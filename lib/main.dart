import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ThreadsFeedPage(),
    ));

class ThreadsFeedPage extends StatefulWidget {
  const ThreadsFeedPage({super.key});
  @override
  State<ThreadsFeedPage> createState() => _ThreadsFeedPageState();
}

class _ThreadsFeedPageState extends State<ThreadsFeedPage> {
  // 🔴 請確保這是你的真實 Render 網址 (最後要有 /feed/)
  final String apiUrl = 'https://threads-mall-api.onrender.com/feed/';
  List<dynamic> posts = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchFeed();
  }

  Future<void> fetchFeed() async {
    try {
      final response = await http.get(Uri.parse(apiUrl));
      if (response.statusCode == 200) {
        setState(() {
          posts = json.decode(response.body);
          isLoading = false;
        });
      }
    } catch (e) {
      debugPrint("抓取失敗: $e");
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: const Text("Threads Mall",
            style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.black))
          : RefreshIndicator(
              onRefresh: fetchFeed,
              child: ListView.separated(
                itemCount: posts.length,
                separatorBuilder: (context, index) => const Divider(height: 1),
                itemBuilder: (context, index) => _buildThreadCard(posts[index]),
              ),
            ),
    );
  }

  Widget _buildThreadCard(Map<String, dynamic> data) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 左側：頭像與線條
          Column(
            children: [
              CircleAvatar(
                radius: 20,
                backgroundImage: NetworkImage(data['avatar_url'] ?? "https://via.placeholder.com/150"),
              ),
              const SizedBox(height: 8),
              Container(width: 2, height: 80, color: Colors.grey[200]),
            ],
          ),
          const SizedBox(width: 12),
          // 右側：內容區
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(data['username'] ?? "未知用戶",
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                const SizedBox(height: 4),
                Text(data['content'] ?? "", style: const TextStyle(fontSize: 15)),
                if (data['image_url'] != null && data['image_url'].isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.network(data['image_url'], fit: BoxFit.cover),
                    ),
                  ),
                const SizedBox(height: 8),
                // 互動按鈕列
                Row(
                  children: [
                    const Icon(Icons.favorite_border, size: 20),
                    const SizedBox(width: 16),
                    const Icon(Icons.chat_bubble_outline, size: 20),
                    const SizedBox(width: 16),
                    const Icon(Icons.repeat, size: 20),
                    const SizedBox(width: 16),
                    // 購買按鈕
                    GestureDetector(
                      onTap: () => _showPurchaseDialog(data),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey[300]!),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          "購買 \$${data['price']}",
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _showPurchaseDialog(Map<String, dynamic> data) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("確認購買"),
        content: Text("商品: ${data['content']}\n價格: \$${data['price']}\n平台抽成(5%): \$${(data['price'] * 0.05).toStringAsFixed(2)}"),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("取消")),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("確認支付")),
        ],
      ),
    );
  }
}