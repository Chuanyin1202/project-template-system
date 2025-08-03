#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
綜合檢查腳本 - 執行所有專案檢查
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validator import main

if __name__ == '__main__':
    # 直接調用主驗證器
    sys.argv.extend(['--check', 'all'])
    main()