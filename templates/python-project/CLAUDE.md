# Python 專案 AI 配置

## 專案規範

### Python 開發標準
- 使用 Python 3.8+
- 遵循 PEP 8 編碼規範
- 使用 type hints
- 編寫 docstrings

### 專案結構
```
project/
├── src/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── setup.py
└── README.md
```

### 必須遵循的規則
1. 使用虛擬環境 (venv/virtualenv)
2. 所有相依套件記錄在 requirements.txt
3. 編寫單元測試（pytest）
4. 使用 black 格式化代碼

### 程式碼品質
- 使用 pylint 或 flake8 檢查
- 測試覆蓋率 > 80%
- 文檔完整性