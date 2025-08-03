#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重複代碼檢查腳本
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validator import main

if __name__ == '__main__':
    # 調用重複代碼檢查
    sys.argv.extend(['--check', 'duplication'])
    main()