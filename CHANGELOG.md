# 變更日誌

所有重要的變更都會記錄在這個文件中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
並且本專案遵循 [語意化版本](https://semver.org/lang/zh-TW/)。

## [1.3.1] - 2025-08-03

### 新增
- SuperClaude v3 架構支援
- 模組化 Markdown 配置系統
- 跨平台 Python 初始化腳本 (`init-project.py`)
- 跨平台 Python 分析腳本 (`analyze-project.py`)
- 跨平台 Python 驗證腳本 (`validator.py` 及相關腳本)
- Windows 原生支援（PowerShell 和批次檔）
- 命令列參數支援（--list, --type, --path, --no-git 等）
- .gitignore 文件
- LICENSE 文件 (MIT)
- CHANGELOG.md 文件
- 詳細的 Windows 使用指南
- 驗證腳本 README 文檔

### 變更
- 更新 global-configs 為 SuperClaude v3 架構
- 分離核心功能和客製化擴展
- 簡化配置結構（CLAUDE.md + EXTENSIONS.md + project-customs/）
- 移除舊的 YAML 配置系統
- 所有腳本都調用統一的 Python 版本
- 驗證腳本從 Shell 改為 Python 實現
- 分析腳本從 Shell 改為 Python 實現

### 改進
- 更清晰的配置架構
- 更好的跨平台相容性
- 更詳細的版本資訊標註
- 更友好的使用者介面
- 支援彩色輸出（可選禁用）

## [1.3.0] - 2025-08-02

### 新增
- SuperClaude v2.0.1 全域配置整合
- 三種配置模式支援（標準/SuperClaude/合併）
- 高級 Token 經濟管理
- 完整中文開發環境
- 認知原型系統

## [1.2.0] - 2025-08-02

### 新增
- 六個新的專業 Agent
- 智能 Agent 選擇功能
- 專案分析工具
- 完整的文檔系統
- 增強的工作流程

## [1.1.0] - 2025-08-02

### 新增
- Voxly 專案最佳實踐整合
- 強制執行規則系統
- 自動化檢查腳本
- Git Commit 規範

## [1.0.0] - 2025-08-01

### 新增
- 基礎模板系統
- 三個核心 Agent（Steering Architect、Strategic Planner、Task Executor）
- 專案初始化工具
- 基本文檔結構