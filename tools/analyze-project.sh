#!/bin/bash

# Project Template System - 專案分析腳本
# 調用 Python 版本進行專案分析
# v1.3.1 - 使用 Python 腳本

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}錯誤：未找到 Python。請先安裝 Python 3.6 或以上版本。${NC}"
    echo -e "您可以從以下網址下載 Python："
    echo -e "https://www.python.org/downloads/"
    exit 1
fi

# 確定 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# 獲取腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 調用 Python 腳本
exec $PYTHON_CMD "$SCRIPT_DIR/analyze-project.py" "$@"