# Windows 使用指南

## 🚀 快速開始（Windows）

### 方法一：使用 Python 腳本（強烈推薦）

1. **確保已安裝 Python**
   - 開啟命令提示字元或 PowerShell
   - 執行 `python --version` 檢查
   - 如未安裝，從 https://www.python.org/downloads/ 下載 Python 3.6 或以上版本

2. **執行初始化腳本**
   ```cmd
   cd D:\AI_Project\project-template-system\tools
   python init-project.py
   ```

3. **互動式選單**
   腳本會引導您完成以下步驟：
   - 輸入專案名稱
   - 選擇專案類型（1-6）
   - 輸入專案描述
   - 選擇主要程式語言
   - 選擇 CLAUDE.md 配置類型
   - 選擇模式（新建/分析/混合）
   - **選擇要啟用的 Agent**（完整的 9 個 Agent 系統）

4. **命令列選項**
   ```cmd
   # 直接創建專案（非互動模式）
   python init-project.py my-project --type flutter-app --no-interactive
   
   # 指定路徑
   python init-project.py my-project --path D:\Projects
   
   # 不初始化 Git
   python init-project.py my-project --no-git
   ```

### 方法二：使用批次檔（簡便方式）

1. **雙擊執行**
   - 導航到 `D:\AI_Project\project-template-system\tools`
   - 雙擊 `init-project.bat`
   - 批次檔會自動調用 Python 腳本

2. **從命令列執行**
   ```cmd
   D:\AI_Project\project-template-system\tools\init-project.bat
   ```

### 方法三：使用 Git Bash（如果已安裝）

如果您安裝了 Git for Windows，可以使用 Git Bash：

```bash
cd /d/AI_Project/project-template-system/tools
./init-project.sh
```

## 📝 Agent 選擇功能

Python 版本完整支援 9 個專業 Agent 選擇：

```
請選擇要啟用的 Agent：
架構層：
  1) Steering Architect - 專案架構師
規劃層：
  2) Strategic Planner - 需求規劃師
執行層：
  3) Task Executor - 任務執行器
  4) Flutter Developer - Flutter 專家
  5) Web Developer - Web 專家
  6) Base Developer - 通用開發者
品質層：
  7) Quality Assurance - 測試專家
運維層：
  8) DevOps Agent - 部署專家
文檔層：
  9) Documentation - 文檔專家

預設組合:
  A) 完整團隊 (1-9 全部)
  B) 開發團隊 (2-6)
  C) 最小團隊 (2,3,6)
  D) 自定義選擇
```

## 🌟 SuperClaude v3 整合

選擇 CLAUDE.md 配置類型時有三個選項：

1. **標準專案配置**：適合一般開發
2. **SuperClaude 全域配置**：高級功能完整版
3. **合併配置**：結合兩者優勢

### 啟用 SuperClaude 功能

如果選擇了 SuperClaude 或合併配置，您將獲得：
- 🧠 Advanced Token Economy
- ⚡ UltraCompressed Mode
- 🌐 中文優化
- 🎭 認知原型系統（11 個 Personas）
- ⏰ 時間意識同步

## 🛠️ 常見問題

### Q: 中文顯示亂碼
A: Python 腳本已經處理了 Windows cp950 編碼問題。如果仍有問題：
```cmd
# PowerShell 中執行
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Q: Python 命令找不到
A: 確保 Python 已加入系統 PATH：
1. 安裝 Python 時勾選「Add Python to PATH」
2. 或手動添加 Python 到環境變數

### Q: 路徑包含空格
A: 使用引號包圍路徑：
```cmd
python init-project.py "My Project" --path "D:\My Projects"
```

### Q: 權限問題
A: 以管理員身份運行命令提示字元或 PowerShell

## 💡 最佳實踐

### 1. 專案結構建議
```
D:\Projects\              # 專案根目錄
├── project-template-system\   # 模板系統
└── my-projects\          # 實際專案
    ├── project1\
    └── project2\
```

### 2. VSCode 整合
創建 `.vscode/settings.json`：
```json
{
  "files.encoding": "utf8",
  "files.eol": "\n",
  "editor.formatOnSave": true,
  "terminal.integrated.defaultProfile.windows": "Command Prompt"
}
```

### 3. 使用 WSL 2（進階選項）
如果需要完整的 Linux 環境：
```bash
# 在 WSL 中
cd /mnt/d/AI_Project/project-template-system
python3 tools/init-project.py
```

## 🎯 快速範例

### 創建 Flutter 專案
```cmd
python init-project.py my-flutter-app
# 選擇：4 (Flutter 應用)
# 選擇：A (完整團隊)
# 選擇：1 (標準配置)
```

### 創建 Web 專案
```cmd
python init-project.py my-web-app
# 選擇：2 (Web 應用)
# 選擇：B (開發團隊)
# 選擇：2 (SuperClaude 配置)
```

## 📊 驗證腳本

專案創建後，可以運行驗證腳本檢查品質：

```cmd
cd my-project
python validation-scripts\check-all.py
```

驗證項目包括：
- 代碼品質檢查
- 安全性掃描
- 重複代碼檢測
- 專案結構驗證

## 🎉 開始開發

專案創建完成後：
1. 進入專案目錄：`cd my-project`
2. 查看 `CLAUDE.md` 了解 AI 助手配置
3. 查看 `.claude/agents/` 了解啟用的 Agent
4. 開始使用 Claude Code 進行 AI 驅動開發！

---

💡 **提示**：Python 版本提供最完整的功能和最佳的跨平台兼容性，強烈建議使用！