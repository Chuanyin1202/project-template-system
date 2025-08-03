@echo off
rem Project Template System - 專案分析腳本 (Windows)
rem 調用 Python 腳本進行專案分析

setlocal

rem 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤：未找到 Python。請先安裝 Python 3.6 或以上版本。
    echo.
    echo 您可以從以下網址下載 Python：
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

rem 獲取腳本所在目錄
set SCRIPT_DIR=%~dp0

rem 調用 Python 腳本
python "%SCRIPT_DIR%analyze-project.py" %*

rem 傳遞退出碼
exit /b %errorlevel%