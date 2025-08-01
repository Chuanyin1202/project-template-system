# CLAUDE.md - Flutter 應用專案配置

## 📋 專案概述
- **專案類型**: Flutter 跨平台應用
- **主要語言**: Dart
- **目標平台**: Android, iOS, Web
- **Flutter 版本**: 3.x.x (stable channel)

## 🛡️ Flutter 強制執行規則

### 🚫 禁止的行為
1. **禁止硬編碼 UI 文字**
   - 所有用戶可見文字必須使用 AppLocalizations
   - 使用 `grep -r "Text('[^']*[\u4e00-\u9fff]" lib/` 檢查
   - 動態文字必須設定 placeholder 參數

2. **禁止在錯誤的生命週期方法中存取 context**
   ```dart
   // ❌ 錯誤：在 initState 中存取 InheritedWidget
   @override
   void initState() {
     super.initState();
     AppLocalizations.of(context); // 會出錯
   }
   
   // ✅ 正確：在 didChangeDependencies 中存取
   @override
   void didChangeDependencies() {
     super.didChangeDependencies();
     AppLocalizations.of(context); // 正確
   }
   ```

3. **禁止繞過平台適配**
   - 平台特定功能必須使用 `Platform.isAndroid/isIOS`
   - 不得假設所有平台行為一致

### ✅ 必須執行的檢查
1. **Widget 重用檢查**
   ```bash
   # 創建新 Widget 前搜尋
   grep -r "類似功能" lib/presentation/widgets/
   find lib/ -name "*.dart" -exec grep -l "Widget.*類似名稱" {} \;
   ```

2. **性能檢查**
   - 列表必須使用 `ListView.builder` 或類似的延遲構建
   - 圖片必須實現快取機制
   - 避免不必要的 Widget 重建

## 🌐 國際化規範 (i18n)

### 基本設置
```yaml
# pubspec.yaml
flutter:
  generate: true

dependencies:
  flutter_localizations:
    sdk: flutter
```

### ARB 檔案最佳實踐
1. **避免危險字符**
   - ❌ 直接使用 `$` 符號：會導致 gen-l10n 崩潰
   - ✅ 使用參數化：`{price}/月` 而非 `$4.99/月`

2. **正確的 placeholder 定義**
   ```json
   {
     "priceDisplay": "{amount}/月",
     "@priceDisplay": {
       "description": "顯示月費價格",
       "placeholders": {
         "amount": {
           "type": "String",
           "example": "NT$150"
         }
       }
     }
   }
   ```

3. **翻譯工作流程**
   - 小批量新增（10-20 個鍵值）
   - 每次新增後執行 `flutter gen-l10n`
   - 遇到錯誤使用二分法定位問題鍵值

## 🏗️ Flutter 專案結構

### 標準目錄結構
```
lib/
├── main.dart              # 應用入口
├── l10n/                  # 國際化檔案
│   ├── app_en.arb        # 英文
│   └── app_zh.arb        # 中文（主要）
├── core/               
│   ├── constants/         # 常數定義
│   ├── themes/           # 主題配置
│   ├── utils/            # 工具函數
│   └── errors/           # 錯誤處理
├── data/
│   ├── models/           # 資料模型
│   ├── repositories/     # 資料倉庫
│   └── services/         # API 服務
├── presentation/
│   ├── screens/          # 頁面（不含業務邏輯）
│   ├── widgets/          # 可重用元件
│   └── providers/        # 狀態管理
└── routes/               # 路由配置
```

### 分層架構規則
- **Screens**: 只負責 UI 展示和用戶互動
- **Providers/Controllers**: 處理業務邏輯和狀態
- **Services**: 處理外部通訊（API、資料庫）
- **Repositories**: 資料存取抽象層

## 🎯 Flutter 開發準則

### 1. 狀態管理規範
```dart
// ✅ 正確：使用 Provider/Riverpod/Bloc
class DataProvider extends ChangeNotifier {
  // 狀態管理邏輯
}

// ❌ 錯誤：在 Widget 中混雜業務邏輯
class MyWidget extends StatefulWidget {
  // 複雜的業務邏輯不應該在這裡
}
```

### 2. Widget 最佳實踐
- **const 構造函數**: 所有無狀態 Widget 應該是 const
- **Key 的使用**: 列表項目必須有唯一 Key
- **避免深層嵌套**: 抽取子 Widget 提高可讀性

### 3. 性能優化必須項
- 使用 `const` 減少重建
- 實施 `RepaintBoundary` 隔離昂貴的繪製
- 使用 `AutomaticKeepAliveClientMixin` 保持頁面狀態
- 圖片使用 `CachedNetworkImage` 或類似快取機制

### 4. 資料庫操作規範
```dart
// SQL 字串插值規範
// ✅ 正確：使用大括號
'SELECT * FROM ${TableNames.users}'

// ❌ 錯誤：直接使用 $ (會被當作字面字串)
'SELECT * FROM $TableNames.users'
```

## 📦 編譯與部署

### Android 編譯配置
```bash
# 預設編譯命令（ARM64 優化）
flutter build apk --release --target-platform=android-arm64 --split-per-abi

# 完整 APK（所有架構）
flutter build apk --release

# App Bundle（推薦用於 Play Store）
flutter build appbundle --release
```

### iOS 編譯配置
```bash
# iOS 編譯
flutter build ios --release

# 確保已設置正確的簽名
# 在 ios/Runner.xcworkspace 中配置
```

### Web 編譯配置
```bash
# Web 編譯（優化大小）
flutter build web --release --web-renderer canvaskit
```

## 🧪 測試策略

### 測試類型
1. **單元測試**: 測試純邏輯函數和類
2. **Widget 測試**: 測試 UI 元件行為
3. **整合測試**: 測試完整用戶流程

### 測試命令
```bash
# 執行所有測試
flutter test

# 執行特定測試
flutter test test/widget_test.dart

# 生成覆蓋率報告
flutter test --coverage
```

### Widget 測試範例
```dart
testWidgets('按鈕點擊測試', (WidgetTester tester) async {
  await tester.pumpWidget(MyApp());
  
  // 尋找按鈕
  final buttonFinder = find.text('點擊我');
  expect(buttonFinder, findsOneWidget);
  
  // 點擊按鈕
  await tester.tap(buttonFinder);
  await tester.pump();
  
  // 驗證結果
  expect(find.text('已點擊'), findsOneWidget);
});
```

## 🔧 常見問題處理

### 套件版本衝突
```bash
# 解決版本衝突
flutter pub upgrade --major-versions

# 清理並重新獲取
flutter clean
flutter pub get
```

### 平台特定問題
1. **Android 建置失敗**
   - 檢查 `android/app/build.gradle`
   - 確認 minSdkVersion >= 21
   - 執行 `flutter doctor -v`

2. **iOS 建置失敗**
   - 在 Xcode 中打開 `ios/Runner.xcworkspace`
   - 更新 Pod：`cd ios && pod update`
   - 檢查簽名配置

### 性能問題排查
```bash
# 使用 DevTools 分析
flutter pub global activate devtools
flutter pub global run devtools

# 在應用中啟用性能覆蓋
MaterialApp(
  showPerformanceOverlay: true,
  // ...
)
```

## 📊 Flutter 專案度量標準

### 性能指標
- **首次渲染時間**: < 2 秒
- **頁面切換**: < 300ms
- **列表滾動**: 保持 60 FPS
- **記憶體使用**: < 150MB（一般應用）

### 代碼品質
- **Widget 樹深度**: < 10 層
- **單一 Widget 代碼**: < 200 行
- **build 方法複雜度**: 保持簡單
- **測試覆蓋率**: > 70%

## 🚨 Flutter 專用檢查腳本

### 自動化檢查
```bash
#!/bin/bash
# Flutter 專案檢查腳本

echo "🔍 檢查硬編碼文字..."
grep -r "Text('[^']*[\u4e00-\u9fff]" lib/ --include="*.dart"

echo "🔍 檢查未使用 const..."
grep -r "Widget.*(" lib/ --include="*.dart" | grep -v "const"

echo "🔍 檢查大型 build 方法..."
find lib/ -name "*.dart" -exec grep -l "build.*{" {} \; | xargs wc -l | sort -n

echo "🔍 執行 Flutter 分析..."
flutter analyze

echo "🔍 檢查過時的套件..."
flutter pub outdated
```

## 🤖 AI 助手 Flutter 特定準則

1. **優先使用 Flutter 官方套件**
2. **遵循 Material Design 或 Cupertino 設計規範**
3. **考慮跨平台相容性**
4. **注重應用性能和用戶體驗**
5. **使用 Flutter 慣用的編程模式**

---
*Flutter 專案模板 v1.1.0 | 整合 Voxly Flutter 最佳實踐*