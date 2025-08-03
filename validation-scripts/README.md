# 專案驗證腳本 (Project Validation Scripts)

跨平台的專案品質驗證工具，使用 Python 實現，支援多種程式語言的代碼檢查。

## 🚀 快速開始

### 運行所有檢查
```bash
python validation-scripts/check-all.py
```

### 運行特定檢查
```bash
# 代碼品質檢查
python validation-scripts/check-code-quality.py

# 安全性檢查
python validation-scripts/check-security.py

# 重複代碼檢查
python validation-scripts/check-duplicates.py
```

## 📋 檢查項目

### 代碼品質檢查
- **文件大小**: 檢查超過 500 行的文件
- **行長度**: 檢查超過 120 字符的行
- **函數長度**: 檢查超過 50 行的函數
- **代碼複雜度**: 簡單的複雜度評估
- **命名規範**: 檢查文件和函數命名
- **導入檢查**: 檢查重複和未使用的導入

### 安全性檢查
- **硬編碼密碼**: 檢查硬編碼的密碼和 API 金鑰
- **SQL 注入**: 檢查潛在的 SQL 注入風險
- **不安全函數**: 檢查使用不安全的函數（如 eval）
- **文件權限**: 檢查過寬的文件權限（Unix/Linux）

### 重複代碼檢查
- **重複函數**: 檢查相同名稱的函數定義
- **重複導入**: 檢查重複的導入語句
- **相似文件**: 檢查可能相似的文件

## ⚙️ 配置

### 使用配置文件
```bash
python validation-scripts/validator.py --config validation-config.json
```

### 配置文件範例
```json
{
  "source_dir": "src",
  "file_extensions": [".py", ".js", ".ts", ".dart"],
  "max_file_lines": 500,
  "max_line_length": 120,
  "max_function_lines": 50,
  "max_complexity": 10
}
```

### 命令列參數
```bash
# 指定源代碼目錄
python validation-scripts/validator.py --source-dir lib

# 禁用彩色輸出
python validation-scripts/validator.py --no-color

# 輸出為 JSON 格式
python validation-scripts/validator.py --output json

# 輸出為 Markdown 格式
python validation-scripts/validator.py --output markdown
```

## 🌐 支援的語言

- **Python** (.py)
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx)
- **Dart/Flutter** (.dart)
- **Go** (.go)
- **Java** (.java) - 基本支援

## 📊 輸出格式

### 控制台輸出（預設）
彩色的控制台輸出，清楚顯示通過和失敗的檢查項目。

### JSON 輸出
```json
{
  "project": "/path/to/project",
  "timestamp": "2025-08-03T10:00:00",
  "summary": {
    "total": 15,
    "passed": 12,
    "failed": 3
  },
  "results": [...]
}
```

### Markdown 輸出
生成適合文檔或報告的 Markdown 格式輸出。

## 🔧 擴展驗證器

### 創建自定義驗證器
```python
from validator import ProjectValidator, ValidationResult

class MyCustomValidator(ProjectValidator):
    def run_all_checks(self):
        self.results = []
        self.results.append(self.my_custom_check())
        return self.results
    
    def my_custom_check(self):
        result = ValidationResult("我的自定義檢查")
        # 實現檢查邏輯
        return result
```

## 💡 最佳實踐

1. **定期運行**: 在提交代碼前運行檢查
2. **CI/CD 整合**: 將檢查整合到持續集成流程
3. **自定義配置**: 根據專案需求調整配置
4. **逐步改進**: 從寬鬆的標準開始，逐步提高要求

## 🐛 故障排除

### Python 版本問題
需要 Python 3.6 或以上版本。

### 編碼問題
所有文件都假設使用 UTF-8 編碼。

### 路徑問題
Windows 用戶請使用正斜線 (/) 或雙反斜線 (\\\\)。

## 📝 版本歷史

### v1.0 (2025-08-03)
- 初始版本
- 支援 Python、JavaScript、Dart
- 基本的品質、安全和重複檢查