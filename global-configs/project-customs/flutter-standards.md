# Flutter/Android 編譯規範 (Flutter/Android Build Standards)

## 📱 APK 編譯默認設定

### 預設配置
- **預設目標架構**：ARM64 (android-arm64)
- **預設版本類型**：Release
- **預設分割策略**：按架構分割 APK (--split-per-abi)

### 標準編譯命令
```bash
flutter build apk --release --target-platform=android-arm64 --split-per-abi
```

### 為什麼選擇這些預設值
1. **ARM64 架構**
   - 現代 Android 設備的主流架構
   - 2019 年後的設備基本都支援
   - 提供最佳效能

2. **Release 版本**
   - 最小檔案大小
   - 最佳執行效能
   - 適合實際部署

3. **架構分割**
   - 每個架構獨立 APK
   - 大幅減少檔案大小
   - Google Play 自動分發

## 🎯 編譯決策流程

### 預設行為
1. 直接執行 ARM64 release APK 編譯
2. 不詢問架構選擇（除非用戶明確要求）
3. 自動使用 --split-per-abi 優化大小

### 特殊情況處理
```bash
# 用戶要求支援所有架構
flutter build apk --release

# 用戶要求 debug 版本
flutter build apk --debug --target-platform=android-arm64

# 用戶要求特定架構
flutter build apk --release --target-platform=android-arm --split-per-abi  # 32位元
```

## ⚙️ 編譯優化建議

### 檔案大小優化
```yaml
# 在 pubspec.yaml 中配置
flutter:
  # 移除未使用的資源
  uses-material-design: true
  
  # 只包含需要的字體
  fonts:
    - family: CustomFont
      fonts:
        - asset: fonts/CustomFont-Regular.ttf
```

### 程式碼優化
```dart
// 使用 const 建構函式
const MyWidget({Key? key}) : super(key: key);

// 避免不必要的重建
class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({Key? key}) : super(key: key);
  // ...
}
```

### ProGuard/R8 配置
```properties
# android/app/proguard-rules.pro
-keep class io.flutter.** { *; }
-keep class com.example.myapp.** { *; }
```

## 📊 編譯產出說明

### 檔案位置
```
build/app/outputs/flutter-apk/
├── app-arm64-v8a-release.apk    # ARM64 版本
├── app-armeabi-v7a-release.apk  # ARM32 版本（如果編譯）
└── app-x86_64-release.apk       # x86_64 版本（如果編譯）
```

### 預期檔案大小
- **基礎 Flutter App**：~15-20 MB (ARM64)
- **加入圖片資源**：+資源大小
- **加入額外套件**：視套件大小而定

## 🚀 部署建議

### Google Play 上架
1. 使用 App Bundle 格式更佳
   ```bash
   flutter build appbundle --release
   ```

2. 自動處理多架構分發
3. 動態功能模組支援

### 直接分發 APK
1. 優先提供 ARM64 版本
2. 視需求提供 32 位元版本
3. 明確標示架構類型

## 📱 測試建議

### 實機測試
```bash
# 安裝到連接的設備
flutter install --release

# 查看設備架構
adb shell getprop ro.product.cpu.abi
```

### 效能分析
```bash
# 使用 profile 模式測試效能
flutter run --profile
```

### 相容性檢查
- 測試最低 Android 版本（通常 API 21+）
- 測試不同螢幕尺寸
- 測試不同 Android 版本