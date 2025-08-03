# 程式碼重用檢查原則 (Code Reuse Principles)

## 🔍 修改前必查

### 核心要求
- **徹底檢查現有架構**：在新增任何功能、元件或服務前，必須先完整檢查專案中是否已有類似實現
- **搜尋相關程式碼**：使用 grep、搜尋工具查找可能的現有實現
- **理解設計模式**：了解專案的架構設計，遵循既有模式

### 檢查流程
1. **全域搜尋**
   ```bash
   # 搜尋相關功能關鍵字
   grep -r "authentication" ./src
   grep -r "login\|signin\|auth" ./src
   
   # 搜尋相似元件
   find . -name "*button*" -o -name "*modal*"
   ```

2. **架構分析**
   - 檢查 `/components` 目錄的共用元件
   - 檢查 `/services` 或 `/utils` 的工具函數
   - 檢查 `/hooks` 的自定義 hooks
   - 檢查 `/contexts` 的狀態管理

3. **相依性檢查**
   - 查看 package.json 已安裝的套件
   - 確認是否有現成的解決方案

## ♻️ 優先重用原則

### 重用策略
1. **使用現有元件**
   - 優先使用已存在的元件、服務、工具類別、輔助函數
   - 查看元件的 props 是否可以滿足需求
   - 考慮擴展現有元件而非創建新元件

2. **擴展而非新建**
   ```javascript
   // ❌ 錯誤：創建新的按鈕元件
   const SubmitButton = () => { ... }
   
   // ✅ 正確：擴展現有按鈕元件
   <Button variant="submit" onClick={handleSubmit}>
     提交
   </Button>
   ```

3. **共用邏輯抽取**
   ```javascript
   // 發現重複的驗證邏輯時
   // ❌ 錯誤：在多處複製相同邏輯
   
   // ✅ 正確：抽取為共用函數
   // utils/validation.js
   export const validateEmail = (email) => { ... }
   export const validatePhone = (phone) => { ... }
   ```

## 🚫 避免技術債

### DRY 原則實踐
- **不重複造輪子**：相同功能不應有多個實現
- **持續重構**：發現重複程式碼時立即重構，而非放任累積
- **保持 DRY 原則**：Don't Repeat Yourself - 每個知識點在系統中只有單一、明確的表述

### 重構時機
1. **立即重構**
   - 發現第二次重複時就應該抽取
   - 不要等到第三次或更多次

2. **重構範例**
   ```javascript
   // 發現重複的 API 呼叫邏輯
   // 重構前：在多個元件中重複
   const fetchUser = async (id) => {
     const response = await fetch(`/api/users/${id}`);
     return response.json();
   };
   
   // 重構後：抽取到 services/api.js
   export const userAPI = {
     get: (id) => apiClient.get(`/users/${id}`),
     update: (id, data) => apiClient.put(`/users/${id}`, data),
     delete: (id) => apiClient.delete(`/users/${id}`)
   };
   ```

## 📝 實施檢查清單

### 修改程式碼前必須確認：
- [ ] **搜尋現有實現**：是否已有類似功能存在？
- [ ] **評估重用可能**：能否通過修改現有程式碼達成目標？
- [ ] **遵循專案模式**：是否遵循專案既定的設計模式？
- [ ] **避免功能重複**：新增的程式碼是否會造成功能重複？
- [ ] **考慮擴展性**：是否應該創建更通用的解決方案？

### 決策矩陣
| 情況 | 行動 |
|------|------|
| 找到完全符合的現有功能 | 直接使用 |
| 找到類似但不完全符合的功能 | 擴展或修改現有功能 |
| 找到可重用的部分邏輯 | 抽取共用部分，組合使用 |
| 確實沒有相關實現 | 創建新功能，但要考慮通用性 |

### 程式碼審查重點
1. **命名一致性**：新程式碼是否遵循專案命名規範
2. **結構一致性**：檔案組織是否符合專案結構
3. **模式一致性**：是否使用專案既定的設計模式
4. **風格一致性**：程式碼風格是否與專案保持一致