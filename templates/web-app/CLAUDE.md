# CLAUDE.md - Web 應用專案配置

## 📋 專案概述
- **專案類型**: Web 應用程式
- **前端框架**: React/Vue/Next.js
- **後端技術**: Node.js/Express
- **資料庫**: PostgreSQL/MongoDB
- **主要語言**: TypeScript/JavaScript

## 🎯 開發準則

### 1. 架構原則
- **元件化設計**: UI 拆分為可重用元件
- **關注點分離**: 業務邏輯、UI、資料層分離
- **響應式設計**: 支援多種設備尺寸
- **漸進增強**: 基礎功能優先，逐步增強體驗

### 2. 前端開發規範
- **元件重用**: 創建新元件前檢查 `src/components/`
- **狀態管理**: 使用統一的狀態管理方案（Redux/Zustand/Pinia）
- **樣式系統**: 使用 CSS-in-JS 或 Tailwind CSS
- **效能優化**: Code splitting、lazy loading、圖片優化

### 3. 後端開發規範
- **RESTful API**: 遵循 REST 設計原則
- **中間件架構**: 適當使用中間件處理共通邏輯
- **錯誤處理**: 統一的錯誤處理和回應格式
- **安全性**: 輸入驗證、認證授權、CORS 設定

### 4. 專案結構
```
src/
├── client/                # 前端程式碼
│   ├── components/       # 可重用元件
│   ├── pages/           # 頁面元件
│   ├── hooks/           # 自定義 Hooks
│   ├── services/        # API 呼叫
│   ├── store/           # 狀態管理
│   └── utils/           # 工具函數
├── server/               # 後端程式碼
│   ├── controllers/     # 路由控制器
│   ├── models/          # 資料模型
│   ├── middleware/      # 中間件
│   ├── services/        # 業務邏輯
│   └── utils/           # 伺服器工具
├── shared/               # 共用程式碼
│   ├── types/           # TypeScript 類型
│   └── constants/       # 共用常數
└── tests/                # 測試檔案
```

### 5. 開發工作流程
1. **功能規劃**: 使用 TodoWrite 規劃任務
2. **元件開發**: 
   - 搜尋現有元件 (Grep)
   - 查看 UI 靈感 (21st.dev)
   - 實現元件
   - 撰寫測試
3. **API 開發**:
   - 定義端點規格
   - 實現控制器
   - 添加驗證中間件
   - 整合測試
4. **部署準備**:
   - 執行建置
   - 執行測試
   - 程式碼審查

### 6. 常用命令
```bash
# 安裝依賴
npm install

# 開發模式（前後端同時啟動）
npm run dev

# 前端開發
npm run dev:client

# 後端開發
npm run dev:server

# 建置生產版本
npm run build

# 執行測試
npm test

# 程式碼檢查
npm run lint

# 格式化程式碼
npm run format
```

### 7. 環境設定
```env
# .env.example
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=your-secret-key
API_URL=http://localhost:3000/api
```

### 8. 安全最佳實踐
- **認證**: JWT/Session + httpOnly cookies
- **授權**: 基於角色的存取控制 (RBAC)
- **輸入驗證**: 使用 joi/yup/zod 驗證
- **XSS 防護**: Content Security Policy
- **CSRF 防護**: CSRF tokens
- **SQL 注入防護**: 使用 ORM/參數化查詢

### 9. 效能優化
- **前端**:
  - Bundle 分析和優化
  - 圖片延遲載入
  - Service Worker 快取
  - CDN 部署靜態資源
- **後端**:
  - 資料庫查詢優化
  - Redis 快取
  - 負載平衡
  - 壓縮回應

### 10. 部署配置
- **Docker**: 使用多階段建置
- **CI/CD**: GitHub Actions/GitLab CI
- **監控**: 錯誤追蹤、效能監控
- **日誌**: 結構化日誌、集中管理

## 🤖 AI 助手特定規則
1. **UI 元件開發**: 優先使用 21st.dev 獲取靈感
2. **API 設計**: 遵循 OpenAPI 規範
3. **測試覆蓋**: 關鍵功能必須有測試
4. **文檔同步**: API 變更需更新文檔

---
*Web App 專案模板 v1.0.0*