# 🤖 九大 Agent 完整指南

深入了解每個 Agent 的能力、使用時機和協作方式。

## 📊 Agent 總覽

| 層級 | Agent | 角色 | 主要輸出 |
|------|-------|------|----------|
| 架構層 | Steering Architect | 專案架構師 | .ai-rules/ |
| 規劃層 | Strategic Planner | 需求規劃師 | specs/ |
| 執行層 | Task Executor | 任務執行器 | 代碼實現 |
| 執行層 | Flutter Developer | Flutter 專家 | Flutter 代碼 |
| 執行層 | Web Developer | Web 專家 | Web 代碼 |
| 執行層 | Base Developer | 通用開發者 | 通用代碼 |
| 品質層 | Quality Assurance | 測試專家 | 測試套件 |
| 運維層 | DevOps Agent | 部署專家 | CI/CD 配置 |
| 文檔層 | Documentation | 文檔專家 | 技術文檔 |

---

## 1. 🏗️ Steering Architect Agent

### 核心職責
分析現有代碼庫並創建專案核心指導文件。

### 使用時機
- 專案初始化
- 架構重構
- 技術棧更新
- 定期架構審查

### 輸入/輸出
- **輸入**: 代碼庫、README、配置文件
- **輸出**: 
  - `.ai-rules/product.md` - 產品願景
  - `.ai-rules/tech.md` - 技術棧
  - `.ai-rules/structure.md` - 專案結構

### 工作流程
```
1. 深度掃描代碼庫
2. 自動生成初稿
3. 與用戶互動優化
4. 確認並保存文檔
```

### 實際範例
```bash
# 分析現有專案
./tools/analyze-project.sh /path/to/project

# Steering Architect 會：
# - 識別使用的框架和庫
# - 分析目錄結構
# - 推斷產品功能
# - 生成架構文檔
```

---

## 2. 📋 Strategic Planner Agent

### 核心職責
將用戶需求轉化為詳細的技術規格和任務清單。

### 使用時機
- 新功能開發
- 需求分析
- 技術設計
- 任務拆解

### 輸入/輸出
- **輸入**: 用戶需求描述
- **輸出**: 
  - `specs/{feature}/requirements.md` - 需求文檔
  - `specs/{feature}/design.md` - 技術設計
  - `specs/{feature}/tasks.md` - 任務清單

### 工作流程
```
1. 需求定義（互動式）
2. 技術設計（展示選項）
3. 任務生成（有序清單）
```

### 實際範例
```markdown
用戶：我需要一個用戶登入系統

Strategic Planner 會創建：
specs/user-auth/
├── requirements.md  # 用戶故事、驗收標準
├── design.md       # API 設計、資料模型
└── tasks.md        # 實現步驟清單
```

---

## 3. ✅ Task Executor Agent

### 核心職責
精確執行 tasks.md 中的每個任務。

### 使用時機
- 執行具體開發任務
- 實現功能細節
- 重構代碼
- 修復 bug

### 輸入/輸出
- **輸入**: `specs/{feature}/tasks.md`
- **輸出**: 代碼變更、更新的 tasks.md

### 工作模式
1. **標準模式**: 每次一個任務，需確認
2. **自主模式**: 連續執行直到完成

### 實際範例
```markdown
# tasks.md
- [ ] 1. 創建 User 模型
- [ ] 2. 實現登入 API
- [x] 3. 添加密碼加密

Task Executor 會：
- 讀取第一個未完成任務
- 精確實現該任務
- 更新任務狀態
```

---

## 4. 📱 Flutter Developer Agent

### 核心職責
Flutter 應用的專業開發。

### 專長領域
- Widget 開發
- 狀態管理（Provider、Riverpod、Bloc）
- 平台特定功能
- 性能優化

### 特色功能
- 預設 ARM64 編譯優化
- 國際化最佳實踐
- Material/Cupertino 設計

### 協作模式
```
Task Executor: "實現登入頁面 UI"
     ↓
Flutter Agent: 創建 LoginScreen Widget
     ↓
產出: lib/screens/login_screen.dart
```

---

## 5. 🌐 Web Developer Agent

### 核心職責
現代 Web 應用開發。

### 專長領域
- 前端框架（React、Vue、Angular）
- 後端開發（Node.js、Express）
- API 設計
- 響應式設計

### 特色功能
- 整合 21st.dev UI 元件搜尋
- Context7 文檔查詢
- 全端開發能力

### 典型任務
- 創建 React 元件
- 實現 RESTful API
- 設置 Webpack 配置
- 優化前端性能

---

## 6. 🔧 Base Developer Agent

### 核心職責
通用程式開發，不限定技術棧。

### 適用場景
- 腳本編寫
- 演算法實現
- 資料處理
- 工具開發

### 靈活性
- 支援多種語言
- 快速原型開發
- 跨平台開發

---

## 7. 🧪 Quality Assurance Agent

### 核心職責
自動化測試和品質保證。

### 測試類型
- 單元測試
- 整合測試
- E2E 測試
- 性能測試
- 安全測試

### 工作流程
```
1. 分析功能需求
2. 生成測試案例
3. 實現測試代碼
4. 執行測試套件
5. 生成測試報告
```

### 品質標準
- 代碼覆蓋率 ≥ 80%
- 零關鍵漏洞
- 性能無退化

---

## 8. 🚀 DevOps Agent

### 核心職責
自動化部署和基礎設施管理。

### 主要功能
- CI/CD 管道設置
- Docker 容器化
- Kubernetes 編排
- 監控和告警

### 部署策略
- 藍綠部署
- 滾動更新
- 金絲雀發布

### 輸出文件
```
- Dockerfile
- docker-compose.yml
- .github/workflows/ci-cd.yml
- kubernetes/*.yaml
```

---

## 9. 📚 Documentation Agent

### 核心職責
創建和維護專案文檔。

### 文檔類型
- API 文檔
- 用戶指南
- 開發者文檔
- 架構文檔

### 自動化功能
- 從代碼生成文檔
- 保持文檔同步
- 多語言支援
- 版本管理

---

## 🔄 Agent 協作模式

### 場景 1：新功能開發
```
1. Strategic Planner 創建規格
2. Task Executor 開始實現
3. Dev Agents 協助專業部分
4. QA Agent 編寫測試
5. Documentation 更新文檔
```

### 場景 2：專案初始化
```
1. Steering Architect 分析專案
2. 創建 .ai-rules/ 架構文檔
3. Dev Agents 根據架構開發
4. DevOps 設置部署環境
```

### 場景 3：Bug 修復
```
1. QA Agent 發現問題
2. Task Executor 修復 bug
3. QA Agent 驗證修復
4. Documentation 更新已知問題
```

---

## 💡 選擇 Agent 的決策樹

```
需要做什麼？
├── 定義專案架構 → Steering Architect
├── 規劃新功能 → Strategic Planner
├── 執行開發任務 → Task Executor + Dev Agents
├── 確保品質 → Quality Assurance
├── 部署上線 → DevOps Agent
└── 更新文檔 → Documentation Agent
```

---

## 🎯 最佳實踐

1. **循序漸進**：先啟用核心 Agent，熟悉後再增加
2. **職責分明**：讓每個 Agent 專注其專長
3. **持續協作**：Agent 間的資訊流動是關鍵
4. **定期審查**：使用 Steering Architect 定期審查架構

---

*詳細的工作流程範例請參考 [WORKFLOW_EXAMPLES.md](./WORKFLOW_EXAMPLES.md)*