# Project Template System - Windows 初始化腳本
# PowerShell 版本，原生 Windows 支援

param(
    [string]$ProjectName,
    [string]$ProjectType = "basic",
    [string]$ConfigType = "standard"
)

# 顏色定義
function Write-ColorOutput($ForegroundColor, $Text) {
    Write-Host $Text -ForegroundColor $ForegroundColor
}

# 顯示標題
Write-ColorOutput Blue "╔════════════════════════════════════════╗"
Write-ColorOutput Blue "║      專案模板初始化系統 v1.3.1        ║"
Write-ColorOutput Blue "║         Windows PowerShell 版本        ║"
Write-ColorOutput Blue "╚════════════════════════════════════════╝"
Write-Host ""

# 獲取專案名稱
if (-not $ProjectName) {
    $ProjectName = Read-Host "請輸入專案名稱"
    if (-not $ProjectName) {
        Write-ColorOutput Red "錯誤: 專案名稱不能為空"
        exit 1
    }
}

# 選擇專案類型
if ($ProjectType -eq "basic") {
    Write-ColorOutput Yellow "請選擇專案類型:"
    Write-Host "1) 基礎專案 (Basic Project)"
    Write-Host "2) Web 應用 (Web Application)"
    Write-Host "3) API 服務 (API Service)"
    Write-Host "4) Flutter 應用 (Flutter App)"
    Write-Host "5) Python 專案 (Python Project)"
    Write-Host "6) 自定義 (Custom)"
    
    $choice = Read-Host "選擇 (1-6)"
    switch ($choice) {
        "1" { $ProjectType = "basic" }
        "2" { $ProjectType = "web-app" }
        "3" { $ProjectType = "api-service" }
        "4" { $ProjectType = "flutter-app" }
        "5" { $ProjectType = "python-project" }
        "6" { $ProjectType = "custom" }
        default { 
            Write-ColorOutput Red "無效的選擇"
            exit 1
        }
    }
}

# 獲取專案描述
$ProjectDescription = Read-Host "請輸入專案描述"

# 選擇配置類型
Write-ColorOutput Yellow "`n請選擇 CLAUDE.md 配置類型:"
Write-Host "1) 標準專案配置"
Write-Host "2) SuperClaude v3 配置"
Write-Host "3) 合併配置"

$configChoice = Read-Host "選擇 (1-3)"
switch ($configChoice) {
    "1" { $ConfigType = "standard" }
    "2" { $ConfigType = "superclaude" }
    "3" { $ConfigType = "merged" }
    default { $ConfigType = "standard" }
}

# 創建專案目錄
$ProjectPath = Join-Path (Get-Location) $ProjectName
if (Test-Path $ProjectPath) {
    Write-ColorOutput Red "錯誤: 目錄 $ProjectName 已存在"
    exit 1
}

Write-ColorOutput Green "`n創建專案目錄..."
New-Item -ItemType Directory -Path $ProjectPath | Out-Null

# 創建基本目錄結構
$directories = @(
    ".claude",
    "src",
    "tests",
    "docs"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path (Join-Path $ProjectPath $dir) -Force | Out-Null
}

# 複製配置文件
$TemplateDir = Split-Path -Parent $PSScriptRoot
$CurrentDate = Get-Date -Format "yyyy-MM-dd"

# 創建 CLAUDE.md
$claudeTemplate = Get-Content (Join-Path $TemplateDir "templates\CLAUDE.md.template") -Raw
$claudeContent = $claudeTemplate `
    -replace "{{PROJECT_NAME}}", $ProjectName `
    -replace "{{PROJECT_TYPE}}", $ProjectType `
    -replace "{{PROJECT_DESCRIPTION}}", $ProjectDescription `
    -replace "{{CREATED_DATE}}", $CurrentDate `
    -replace "{{VERSION}}", "1.0.0"

Set-Content -Path (Join-Path $ProjectPath ".claude\CLAUDE.md") -Value $claudeContent -Encoding UTF8

# 根據配置類型添加擴展
if ($ConfigType -eq "superclaude" -or $ConfigType -eq "merged") {
    Add-Content -Path (Join-Path $ProjectPath ".claude\CLAUDE.md") -Value "`n`n# SuperClaude v3 擴展`n@EXTENSIONS.md" -Encoding UTF8
    
    # 複製 EXTENSIONS.md
    Copy-Item (Join-Path $TemplateDir "global-configs\EXTENSIONS.md") `
              (Join-Path $ProjectPath ".claude\EXTENSIONS.md")
    
    # 創建 project-customs 目錄的引用說明
    $customsReadme = @"
# Project Customs 說明

本專案使用 SuperClaude v3 的客製化擴展功能。

擴展文件位於全域配置：
~/.claude/project-customs/

如需專案特定的客製化，請在此目錄創建對應的 .md 文件。
"@
    Set-Content -Path (Join-Path $ProjectPath ".claude\PROJECT_CUSTOMS_README.md") `
                -Value $customsReadme -Encoding UTF8
}

# 創建 .gitignore
Copy-Item (Join-Path $TemplateDir ".gitignore") `
          (Join-Path $ProjectPath ".gitignore")

# 創建 .gitattributes (處理換行符號)
$gitattributes = @"
# 自動處理換行符號
* text=auto eol=lf

# Windows 批次檔保持 CRLF
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# 二進位檔案
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
"@
Set-Content -Path (Join-Path $ProjectPath ".gitattributes") -Value $gitattributes -Encoding UTF8

# 創建 README.md
$readme = @"
# $ProjectName

$ProjectDescription

## 專案資訊
- **類型**: $ProjectType
- **創建日期**: $CurrentDate
- **版本**: 1.0.0

## 快速開始

### 環境需求
- [列出所需的開發環境]

### 安裝步驟
``````bash
# 安裝相依套件
[安裝命令]
``````

### 使用方式
``````bash
# 執行專案
[執行命令]
``````

## 專案結構
``````
$ProjectName/
├── .claude/          # AI 助手配置
├── src/              # 原始碼
├── tests/            # 測試檔案
├── docs/             # 文檔
└── README.md         # 本文件
``````

## 開發指南
詳見 `.claude/CLAUDE.md` 中的開發規範。

## 授權
[授權資訊]
"@
Set-Content -Path (Join-Path $ProjectPath "README.md") -Value $readme -Encoding UTF8

# 顯示完成訊息
Write-Host ""
Write-ColorOutput Green "✅ 專案創建成功！"
Write-Host ""
Write-Host "專案位置: $ProjectPath"
Write-Host ""
Write-ColorOutput Yellow "下一步:"
Write-Host "1. cd $ProjectName"
Write-Host "2. 根據專案類型安裝相依套件"
Write-Host "3. 開始開發！"

if ($ConfigType -eq "superclaude") {
    Write-Host ""
    Write-ColorOutput Cyan "SuperClaude v3 功能已啟用 ✨"
}