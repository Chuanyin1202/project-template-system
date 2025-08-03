# 🚀 快速開始指南

30 秒內開始使用專案模板系統！

## 📋 前置需求

- Python 3.6+（必要）
- Git（選用）
- 對應的開發環境（Node.js、Flutter 等）

## ⚡ 快速開始

### 選項 1：創建新專案（最快速）

```bash
# 1. 執行初始化腳本
python project-template-system/tools/init-project.py    # Windows
python3 project-template-system/tools/init-project.py   # Linux/macOS

# 2. 按照提示操作：
#    - 輸入專案名稱
#    - 選擇專案類型
#    - 選擇要啟用的 Agent
#    - 選擇 CLAUDE.md 配置類型

# 3. 進入專案開始開發
cd your-project-name
```

### 選項 2：分析現有專案

```bash
# 分析當前目錄的專案
python project-template-system/tools/analyze-project.py

# 或分析指定路徑
python project-template-system/tools/analyze-project.py /path/to/project
```

## 🎯 典型工作流程

### 1. Web 應用快速啟動

```bash
# 創建專案
python tools/init-project.py
# 選擇: Web 應用 > JavaScript/TypeScript > 完整團隊 (A)

# 開始第一個功能
# 使用 Strategic Planner 創建功能規格
# 使用 Task Executor 逐步實現
```

### 2. Flutter App 開發

```bash
# 創建專案
python tools/init-project.py
# 選擇: Flutter 應用 > Dart > 開發團隊 (B)

# Flutter 特定 Agent 會協助你
```

## 📝 核心概念

### 三層文檔體系

1. **架構層** (`.ai-rules/`)
   - 由 Steering Architect 維護
   - 定義專案核心架構

2. **規範層** (`CLAUDE.md`)
   - AI 助手行為準則
   - 開發規範和流程

3. **執行層** (`specs/`)
   - 由 Strategic Planner 創建
   - 具體功能的實現計劃

### Agent 協作

```
需求 → Strategic Planner → specs/
      ↓
specs/ → Task Executor → 代碼
      ↓
代碼 → QA Agent → 測試
      ↓
測試通過 → DevOps Agent → 部署
```

## 🆘 常見問題

### Q: 我應該選擇哪些 Agent？

**新手推薦**：選擇「C) 最小團隊」
- Strategic Planner（規劃）
- Task Executor（執行）
- Base Developer（開發）

**完整開發**：選擇「A) 完整團隊」
- 包含所有 9 個 Agent

### Q: 如何開始第一個功能？

1. 確保啟用了 Strategic Planner
2. 描述你的功能需求
3. Agent 會創建 `specs/feature-name/`
4. 使用 Task Executor 開始實現

### Q: 現有專案如何整合？

1. 運行 `python analyze-project.py`
2. 系統會分析並推薦 Agent
3. 自動創建必要的配置文件

## 📚 下一步

- 閱讀 [AGENT_GUIDE.md](./AGENT_GUIDE.md) 了解每個 Agent
- 查看 [WORKFLOW_EXAMPLES.md](./WORKFLOW_EXAMPLES.md) 學習完整流程
- 參考 [BEST_PRACTICES.md](./BEST_PRACTICES.md) 獲取最佳實踐

---

💡 **專業提示**：先從簡單的配置開始，隨著熟悉度增加再啟用更多 Agent！

## 💻 不同平台注意事項

### Windows 用戶
- 使用 `python` 命令
- 如果遇到編碼問題，腳本已經處理了 cp950 編碼
- 可以直接雙擊 `init-project.bat`

### Linux/macOS 用戶
- 使用 `python3` 命令
- 如果有 Git Bash，也可以使用 `./init-project.sh`