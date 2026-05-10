import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:threadsmall/main.dart'; // 確保這行路徑指向你的專案名稱

void main() {
  testWidgets('ThreadsMall 畫面初始化測試', (WidgetTester tester) async {
    // 1. 建立並啟動 ThreadsMall App
    await tester.pumpWidget(const ThreadsMall());

    // 2. 驗證 App 啟動時是否正確顯示「載入中」狀態 (CircularProgressIndicator)
    // 因為 fetchProductData 是非同步的，剛啟動時 isLoading 為 true
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // 3. 測試 UI 結構是否存在 (例如 AppBar 標題)
    // 我們使用 pump() 來模擬時間流逝，等待畫面刷新
    await tester.pump();

    // 驗證測試環境中是否捕捉到 AppBar 的文字
    // 註：在沒有模擬 API 回傳的情況下，測試通常會停在 Loading 或顯示連線失敗
    expect(find.text('Threads 精選商品'), findsNothing); // 初始狀態還沒載入完成
  });

  testWidgets('基本元件存在性測試', (WidgetTester tester) async {
    await tester.pumpWidget(const ThreadsMall());
    
    // 檢查 MaterialApp 是否存在
    expect(find.byType(MaterialApp), findsOneWidget);
    
    // 檢查背景顏色是否為黑色 (ThemeData 定義)
    final MaterialApp app = tester.widget(find.byType(MaterialApp));
    expect(app.theme?.scaffoldBackgroundColor, Colors.black);
  });
}