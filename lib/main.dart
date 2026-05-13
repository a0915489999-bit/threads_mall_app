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
  // 🔴 請確保這是你的真實 Render 網址
  final String baseUrl = 'https://threads-mall-api.onrender.com';
  List<dynamic> posts = [];
  bool isLoading = true;
  String currentUserName = "";

  @override
  void initState() {
    super.initState();
    // 確保進入頁面後立即跳出登入視窗
    Future.delayed(Duration.zero, () => _showLoginDialog());
    fetchFeed();
  }

  // 1. 簡易登入系統
  void _showLoginDialog() {
    final TextEditingController nameController = TextEditingController();
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text("歡迎來到 Threads Mall"),
        content: TextField(
          controller: nameController,
          decoration: const InputDecoration(hintText: "請輸入你的稱呼 (例如：林帛諭)"),
        ),
        actions: [
          ElevatedButton(
            onPressed: () {
              if (nameController.text.isNotEmpty) {
                setState(() { currentUserName = nameController.text; });
                Navigator.pop(context);
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.black),
            child: const Text("開始使用", style: TextStyle(color: Colors.white)),
          )
        ],
      ),
    );
  }

  // 取得動態牆資料
  Future<void> fetchFeed() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/feed/'));
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

  // 2. 發布商品邏輯
  Future<void> _postProduct(String content, double price, String imageUrl) async {
    try {
      await http.post(
        Uri.parse('$baseUrl/products/'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          "content": content,
          "price": price,
          "image_url": imageUrl,
          "username": currentUserName,
        }),
      );
      fetchFeed(); // 刷新列表
    } catch (e) {
      debugPrint("發布失敗: $e");
    }
  }

  // 3. 留言彈窗邏輯
  void _showCommentSheet(int productId) {
    final TextEditingController commentController = TextEditingController();
    List<dynamic> comments = [];

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) => StatefulBuilder(
        builder: (context, setModalState) {
          // 內部刷新留言的方法
          Future<void> loadComments() async {
            final res = await http.get(Uri.parse('$baseUrl/comments/$productId'));
            if (res.statusCode == 200) {
              setModalState(() { comments = json.decode(res.body); });
            }
          }

          return Padding(
            padding: EdgeInsets.only(
              bottom: MediaQuery.of(context).viewInsets.bottom,
              left: 16, right: 16, top: 16
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text("留言回覆", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                const Divider(),
                SizedBox(
                  height: 250,
                  child: comments.isEmpty 
                    ? const Center(child: Text("尚無留言，快來搶頭香！"))
                    : ListView.builder(
                        itemCount: comments.length,
                        itemBuilder: (context, i) => ListTile(
                          leading: const Icon(Icons.account_circle),
                          title: Text(comments[i]['user_name'], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          subtitle: Text(comments[i]['content']),
                        ),
                      ),
                ),
                TextField(
                  controller: commentController,
                  decoration: InputDecoration(
                    hintText: "留言給賣家...",
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.send, color: Colors.blue),
                      onPressed: () async {
                        if (commentController.text.isNotEmpty) {
                          await http.post(
                            Uri.parse('$baseUrl/comments/'),
                            headers: {"Content-Type": "application/json"},
                            body: json.encode({
                              "product_id": productId,
                              "content": commentController.text,
                              "username": currentUserName
                            }),
                          );
                          commentController.clear();
                          await loadComments();
                          fetchFeed(); // 同步更新首頁留言數
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 20),
              ],
            ),
          );
        },
      ),
    );
  }

  // 發文彈窗
  void _showPostDialog() {
    final TextEditingController contentController = TextEditingController();
    final TextEditingController priceController = TextEditingController();
    final TextEditingController imageController = TextEditingController();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) => Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom, left: 20, right: 20, top: 20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text("發表新商品", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            TextField(controller: contentController, decoration: const InputDecoration(hintText: "描述你的商品...")),
            TextField(controller: priceController, decoration: const InputDecoration(hintText: "價格 (TWD)")),
            TextField(
              controller: imageController, 
              decoration: InputDecoration(
                hintText: "圖片網址",
                suffixIcon: TextButton(
                  onPressed: () {
                    // 生成一張基於時間戳的隨機美圖網址
                    imageController.text = "https://picsum.photos/seed/${DateTime.now().millisecondsSinceEpoch}/600/400";
                  },
                  child: const Text("隨機圖"),
                ),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                if (contentController.text.isNotEmpty) {
                  _postProduct(
                    contentController.text, 
                    double.tryParse(priceController.text) ?? 0, 
                    imageController.text
                  );
                  Navigator.pop(context);
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.black, 
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 45)
              ),
              child: const Text("發布"),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Text("Threads Mall ($currentUserName)", style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
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
      floatingActionButton: FloatingActionButton(
        onPressed: _showPostDialog,
        backgroundColor: Colors.black,
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }

  Widget _buildThreadCard(Map<String, dynamic> data) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Column(
            children: [
              CircleAvatar(radius: 20, backgroundImage: NetworkImage(data['avatar_url'])),
              const SizedBox(height: 8),
              Container(width: 2, height: 100, color: Colors.grey[100]),
            ],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(data['username'], style: const TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text(data['content']),
                if (data['image_url'].isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(12), 
                      child: Image.network(data['image_url'], fit: BoxFit.cover)
                    ),
                  ),
                Row(
                  children: [
                    const Icon(Icons.favorite_border, size: 20),
                    const SizedBox(width: 16),
                    GestureDetector(
                      onTap: () => _showCommentSheet(data['id']),
                      child: Row(
                        children: [
                          const Icon(Icons.chat_bubble_outline, size: 20),
                          const SizedBox(width: 4),
                          Text("${data['comments_count'] ?? 0}", style: const TextStyle(fontSize: 12)),
                        ],
                      ),
                    ),
                    const SizedBox(width: 16),
                    GestureDetector(
                      onTap: () => _showPurchaseDialog(data),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey[300]!), 
                          borderRadius: BorderRadius.circular(20)
                        ),
                        child: Text("購買 \$${data['price']}", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
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
        content: Text("商品: ${data['content']}\n價格: \$${data['price']}\n平台費(5%): \$${(data['price'] * 0.05).toStringAsFixed(2)}"),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("取消")),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("確認支付")),
        ],
      ),
    );
  }
}