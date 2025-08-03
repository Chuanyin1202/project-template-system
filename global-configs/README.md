# 🌟 SuperClaude v3 全域配置

這個目錄包含了配合 SuperClaude v3 的客製化擴展配置，採用最新的模組化架構。

## 📁 目錄結構

```
global-configs/
├── CLAUDE.md              # SuperClaude 入口文件
├── EXTENSIONS.md          # 客製化擴展管理
└── project-customs/       # 客製化功能模組
    ├── chinese-mode.md        # 中文優先模式
    ├── time-awareness.md      # 時間意識同步
    ├── knowledge-base.md      # 開發知識庫
    ├── technical-honesty.md   # 技術誠實原則
    ├── code-reuse.md         # 程式碼重用檢查
    └── flutter-standards.md   # Flutter 規範
```

## 🚀 使用方式

### 前置要求
您需要先安裝 SuperClaude v3：
1. SuperClaude v3 會自動生成核心文件（COMMANDS.md、FLAGS.md 等）
2. 這些文件位於 `~/.claude/` 目錄
3. 確認使用的是 SuperClaude v3（支援模組化 Markdown 架構）

### 配置架構

```
~/.claude/                    # SuperClaude 核心配置
├── CLAUDE.md                # 引用核心模組
├── COMMANDS.md              # 命令系統
├── FLAGS.md                 # 標誌系統
├── PRINCIPLES.md            # 原則
├── RULES.md                 # 規則
├── MCP.md                   # MCP 服務器
├── PERSONAS.md              # 人格系統
├── ORCHESTRATOR.md          # 智能路由
├── MODES.md                 # 操作模式
├── EXTENSIONS.md            # 擴展管理（客製化）
└── project-customs/         # 客製化模組（客製化）
```

### 整合客製化功能

1. **全域啟用**（推薦）
   - 將 `EXTENSIONS.md` 複製到 `~/.claude/`
   - 將 `project-customs/` 目錄複製到 `~/.claude/`
   - 在 `~/.claude/CLAUDE.md` 最後添加：
     ```markdown
     # Custom Extensions (Optional)
     @EXTENSIONS.md
     ```

2. **專案級別啟用**
   - 在專案中創建 `.claude/PROJECT_CONFIG.md`
   - 選擇性引用需要的擴展：
     ```markdown
     # 專案配置
     @~/.claude/project-customs/chinese-mode.md
     @~/.claude/project-customs/knowledge-base.md
     # ... 其他需要的擴展
     ```

## 🌟 客製化功能說明

### 1. 🌐 中文優先模式
- 強制使用中文回覆
- 代碼註釋使用中文
- 保留必要的英文技術術語

### 2. ⏰ 時間意識同步
- 每次對話開始執行 `date` 命令
- 避免使用錯誤的日期
- 基於系統時間而非內部時鐘

### 3. 🧠 開發知識庫管理
- 自動維護 `DEVELOPMENT_KNOWLEDGE_BASE.md`
- 記錄技術發現、挑戰和解決方案
- 結構化的知識管理模板

### 4. 🚫 技術誠實原則
- 禁止使用模擬或假資料
- 遇到限制必須立即停止並說明
- 由用戶決定替代方案

### 5. ♻️ 程式碼重用檢查
- 修改前必須徹底檢查現有架構
- 優先使用和擴展現有元件
- 嚴格遵循 DRY 原則

### 6. 📱 Flutter/Android 規範
- 預設編譯 ARM64 release APK
- 使用 --split-per-abi 優化檔案大小
- 提供最佳實踐建議

## 📖 配置優先級

```
全域配置 (~/.claude/)
    ↓
專案配置 (.claude/)
    ↓
會話覆蓋 (命令行標誌)
```

## 🔧 與 Agent 系統整合

本配置與 project-template-system 的九大 Agent 系統完全相容：
- Agents 會自動識別並使用這些擴展功能
- 可以在 Agent 配置中指定特定擴展
- 支援 Agent 級別的配置覆蓋

## 📄 版本資訊

- **更新日期**：2025-08-03
- **SuperClaude 版本**：配合 SuperClaude v3（最新版）
  - 支援 Wave Orchestration Engine
  - 支援 11 個專業 Personas
  - 支援 Loop 命令
  - 完整 MCP 服務器整合（Context7、Sequential、Magic、Playwright 等）
- **配置架構**：基於最新模組化 Markdown 架構（非 YAML）
- **整合內容**：project-template-system v1.3.0 客製化功能

## 🤝 貢獻指南

1. 新增擴展模組到 `project-customs/`
2. 在 `EXTENSIONS.md` 中註冊新模組
3. 更新本 README 文檔
4. 提交 Pull Request

---

<p align="center">
  <b>🚀 SuperClaude + 客製化擴展 = 極致開發體驗！</b>
</p>