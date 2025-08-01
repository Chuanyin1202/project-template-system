# 🌟 SuperClaude 全域配置

這個目錄包含了完整的 SuperClaude v2.0.1 配置文件，提供進階的 AI 開發能力。

## 📁 目錄結構

```
global-configs/
├── CLAUDE.md              # SuperClaude 主配置文件
├── commands/              # 命令模式配置文件
│   ├── shared/           # 共享配置模式
│   └── *.md             # 各種專業命令定義
├── shared/               # SuperClaude 核心配置
│   ├── superclaude-core.yml      # 核心功能配置
│   ├── superclaude-mcp.yml       # MCP 整合配置
│   ├── superclaude-personas.yml  # 認知原型配置
│   └── superclaude-rules.yml     # 規則系統配置
└── README.md             # 本文件
```

## 🚀 SuperClaude 特色功能

### 核心能力
- **🧠 Advanced Token Economy**: 智能 token 管理和優化
- **⚡ UltraCompressed Mode**: 高效壓縮輸出模式
- **🎯 Intelligent Auto-Activation**: 智能自動啟動功能
- **📊 Performance Standards**: 嚴格的性能基準
- **🔍 Evidence-Based Standards**: 基於證據的開發標準

### 專業功能
- **🌐 語言要求**: 中文優先回覆系統
- **⏰ 時間意識**: 自動時間同步機制
- **📝 Development Knowledge Base**: 自動知識庫管理
- **🔄 程式碼重用原則**: 智能代碼復用檢查
- **🛡️ 開發限制處理**: 嚴格的技術限制處理

### MCP 整合
- **🔌 Server Capabilities Extended**: 擴展的服務器能力
- **💰 Token Economics**: 智能 token 經濟學
- **🔄 Workflows**: 高級工作流程管理
- **🎭 Cognitive Archetypes**: 認知原型系統

## 📖 使用方式

### 在新專案中使用

使用 `init-project.sh` 創建專案時，選擇配置類型：

```bash
./tools/init-project.sh

# 選擇配置類型：
# A) 標準專案配置（適合一般開發）
# B) SuperClaude 全域配置（高級功能）
# C) 合併配置（結合兩者優勢）
```

### 手動整合到現有專案

1. **複製主配置**：
   ```bash
   cp global-configs/CLAUDE.md your-project/.claude/
   ```

2. **複製依賴文件**（如果需要）：
   ```bash
   cp -r global-configs/commands your-project/.claude/
   cp -r global-configs/shared your-project/.claude/
   ```

3. **調整路徑**：
   確保 CLAUDE.md 中的 @include 路徑正確指向複製的文件。

## 🎯 配置說明

### CLAUDE.md 主要區塊

1. **Core Configuration**
   - 核心哲學和行為準則
   - 思考模式設定

2. **Performance Optimization**
   - Token 經濟管理
   - 壓縮輸出模式
   - 成本優化

3. **Development Practices**
   - 代碼生成規範
   - 品質標準
   - 安全準則

4. **Language & Workflow**
   - 中文回覆設定
   - 時間同步機制
   - 檔案管理原則

### 自定義配置

您可以根據專案需求調整配置：

```yaml
# 範例：專案特定設定
project_specific:
  language: "zh-TW"           # 繁體中文
  code_style: "strict"        # 嚴格代碼風格
  performance_mode: "high"    # 高性能模式
```

## 🔧 高級功能

### 1. 智能 Token 管理
SuperClaude 會自動優化 token 使用，提供：
- 動態壓縮輸出
- 智能上下文管理
- 成本效益分析

### 2. 認知原型系統
支援多種 AI 人格模式：
- 技術專家模式
- 產品經理模式
- 品質保證模式
- 文檔專家模式

### 3. MCP 深度整合
- 無縫連接外部服務
- 智能資料處理
- 自動化工作流程

## ⚠️ 注意事項

### 兼容性
- 需要 Claude Code v1.0+ 支援
- 部分功能需要 MCP 服務器
- @include 語法需要正確的文件路徑

### 性能考量
- SuperClaude 配置較為複雜，可能增加初始載入時間
- 建議在需要高級功能時才使用完整配置
- 可以選擇性啟用功能模組

### 自定義建議
- 根據團隊需求調整語言設定
- 可以移除不需要的功能模組
- 建議保留核心安全和品質檢查

## 🆚 與標準配置比較

| 功能 | 標準配置 | SuperClaude |
|------|----------|-------------|
| 基礎 AI 能力 | ✅ | ✅ |
| 專案模板 | ✅ | ✅ |
| Agent 協作 | ✅ | ✅ |
| 高級 Token 管理 | ❌ | ✅ |
| 認知原型系統 | ❌ | ✅ |
| MCP 深度整合 | ❌ | ✅ |
| 中文優化 | 基礎 | 完整 |
| 性能優化 | 基礎 | 高級 |

## 📚 更多資源

- [SuperClaude 官方文檔](https://github.com/your-repo/superclaude)
- [MCP 協議說明](https://modelcontextprotocol.io/)
- [認知原型指南](https://docs.anthropic.com/claude/docs)

---

*SuperClaude v2.0.1 | 專業 AI 開發框架 | 中文優化版本*