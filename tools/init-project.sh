#!/bin/bash

# 專案模板初始化腳本
# 用於快速創建配置了 CLAUDE.md 和 Agent 的新專案
# v1.3.0 - 添加 SuperClaude 全域配置支援

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 模板系統根目錄
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 顯示標題
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      專案模板初始化系統 v1.3.0        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# 獲取專案名稱
read -p "請輸入專案名稱: " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}錯誤: 專案名稱不能為空${NC}"
    exit 1
fi

# 選擇專案類型
echo -e "\n${YELLOW}請選擇專案類型:${NC}"
echo "1) 基礎專案 (Basic Project)"
echo "2) Web 應用 (Web Application)"
echo "3) API 服務 (API Service)"
echo "4) Flutter 應用 (Flutter App)"
echo "5) 機器學習專案 (ML Project)"
echo "6) 自定義 (Custom)"

read -p "選擇 (1-6): " PROJECT_TYPE_CHOICE

case $PROJECT_TYPE_CHOICE in
    1) PROJECT_TYPE="basic" ;;
    2) PROJECT_TYPE="web-app" ;;
    3) PROJECT_TYPE="api-service" ;;
    4) PROJECT_TYPE="flutter-app" ;;
    5) PROJECT_TYPE="ml-project" ;;
    6) PROJECT_TYPE="custom" ;;
    *) echo -e "${RED}無效的選擇${NC}"; exit 1 ;;
esac

# 獲取專案描述
read -p "請輸入專案描述: " PROJECT_DESCRIPTION

# 選擇主要語言
echo -e "\n${YELLOW}請選擇主要程式語言:${NC}"
echo "1) JavaScript/TypeScript"
echo "2) Python"
echo "3) Dart (Flutter)"
echo "4) Java"
echo "5) Go"
echo "6) 其他"

read -p "選擇 (1-6): " LANGUAGE_CHOICE

case $LANGUAGE_CHOICE in
    1) PRIMARY_LANGUAGE="JavaScript/TypeScript" ;;
    2) PRIMARY_LANGUAGE="Python" ;;
    3) PRIMARY_LANGUAGE="Dart" ;;
    4) PRIMARY_LANGUAGE="Java" ;;
    5) PRIMARY_LANGUAGE="Go" ;;
    6) read -p "請輸入語言名稱: " PRIMARY_LANGUAGE ;;
    *) echo -e "${RED}無效的選擇${NC}"; exit 1 ;;
esac

# 選擇 CLAUDE.md 配置類型
echo -e "\n${YELLOW}請選擇 CLAUDE.md 配置類型:${NC}"
echo "1) 標準專案配置 (適合一般開發)"
echo "2) SuperClaude 全域配置 (高級功能完整版)"
echo "3) 合併配置 (結合兩者優勢)"

read -p "選擇 (1-3): " CLAUDE_CONFIG_CHOICE

case $CLAUDE_CONFIG_CHOICE in
    1) CLAUDE_CONFIG="standard" ;;
    2) CLAUDE_CONFIG="superclaude" ;;
    3) CLAUDE_CONFIG="merged" ;;
    *) echo -e "${RED}無效的選擇${NC}"; exit 1 ;;
esac

# 選擇模式
echo -e "\n${YELLOW}請選擇模式:${NC}"
echo "1) 創建新專案"
echo "2) 分析現有專案"
echo "3) 混合模式 (分析後增強)"

read -p "選擇 (1-3): " MODE_CHOICE

case $MODE_CHOICE in
    1) MODE="new" ;;
    2) MODE="analyze" ;;
    3) MODE="hybrid" ;;
    *) echo -e "${RED}無效的選擇${NC}"; exit 1 ;;
esac

# 選擇 Agent 配置
echo -e "\n${YELLOW}請選擇要啟用的 Agent (可多選，用空格分隔):${NC}"
echo "${GREEN}架構層:${NC}"
echo "  1) Steering Architect - 專案架構師"
echo "${GREEN}規劃層:${NC}"
echo "  2) Strategic Planner - 需求規劃師"
echo "${GREEN}執行層:${NC}"
echo "  3) Task Executor - 任務執行器"
echo "  4) Flutter Developer - Flutter 專家"
echo "  5) Web Developer - Web 專家"
echo "  6) Base Developer - 通用開發者"
echo "${GREEN}品質層:${NC}"
echo "  7) Quality Assurance - 測試專家"
echo "${GREEN}運維層:${NC}"
echo "  8) DevOps Agent - 部署專家"
echo "${GREEN}文檔層:${NC}"
echo "  9) Documentation - 文檔專家"
echo
echo "預設組合:"
echo "  A) 完整團隊 (1-9 全部)"
echo "  B) 開發團隊 (2-6)"
echo "  C) 最小團隊 (2,3,6)"
echo "  D) 自定義選擇"

read -p "選擇 (A/B/C/D): " AGENT_PRESET

case $AGENT_PRESET in
    A|a) SELECTED_AGENTS="1 2 3 4 5 6 7 8 9" ;;
    B|b) SELECTED_AGENTS="2 3 4 5 6" ;;
    C|c) SELECTED_AGENTS="2 3 6" ;;
    D|d) 
        read -p "輸入 Agent 編號 (空格分隔): " SELECTED_AGENTS
        ;;
    *) echo -e "${RED}無效的選擇${NC}"; exit 1 ;;
esac

# 解析選擇的 Agent
DECLARE_AGENTS=()
for agent in $SELECTED_AGENTS; do
    case $agent in
        1) DECLARE_AGENTS+=("steering-architect-agent") ;;
        2) DECLARE_AGENTS+=("strategic-planner-agent") ;;
        3) DECLARE_AGENTS+=("task-executor-agent") ;;
        4) DECLARE_AGENTS+=("flutter-developer-agent") ;;
        5) DECLARE_AGENTS+=("web-developer-agent") ;;
        6) DECLARE_AGENTS+=("base-agent") ;;
        7) DECLARE_AGENTS+=("quality-assurance-agent") ;;
        8) DECLARE_AGENTS+=("devops-agent") ;;
        9) DECLARE_AGENTS+=("documentation-agent") ;;
    esac
done

# 創建專案目錄
PROJECT_PATH="${PWD}/${PROJECT_NAME}"
if [ -d "$PROJECT_PATH" ]; then
    echo -e "${RED}錯誤: 目錄 $PROJECT_NAME 已存在${NC}"
    exit 1
fi

echo -e "\n${GREEN}正在創建專案結構...${NC}"
mkdir -p "$PROJECT_PATH"

# 複製或創建 CLAUDE.md 根據配置類型
echo -e "${GREEN}設置 CLAUDE.md 配置...${NC}"
case $CLAUDE_CONFIG in
    "standard")
        # 使用標準模板
        if [ -f "$TEMPLATE_DIR/templates/$PROJECT_TYPE/CLAUDE.md" ]; then
            cp "$TEMPLATE_DIR/templates/$PROJECT_TYPE/CLAUDE.md" "$PROJECT_PATH/CLAUDE.md"
        else
            cp "$TEMPLATE_DIR/templates/CLAUDE.md.template" "$PROJECT_PATH/CLAUDE.md"
        fi
        
        # 替換佔位符
        sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PROJECT_TYPE}}/$PROJECT_TYPE/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PRIMARY_LANGUAGE}}/$PRIMARY_LANGUAGE/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PROJECT_DESCRIPTION}}/$PROJECT_DESCRIPTION/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{CREATED_DATE}}/$(date +%Y-%m-%d)/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{VERSION}}/0.1.0/g" "$PROJECT_PATH/CLAUDE.md"
        echo "  [OK] 已設置標準專案配置"
        ;;
        
    "superclaude")
        # 使用 SuperClaude 全域配置
        cp "$TEMPLATE_DIR/global-configs/CLAUDE.md" "$PROJECT_PATH/CLAUDE.md"
        
        # 複製依賴文件
        mkdir -p "$PROJECT_PATH/.claude/commands"
        mkdir -p "$PROJECT_PATH/.claude/shared"
        cp -r "$TEMPLATE_DIR/global-configs/commands/"* "$PROJECT_PATH/.claude/commands/"
        cp -r "$TEMPLATE_DIR/global-configs/shared/"* "$PROJECT_PATH/.claude/shared/"
        
        echo "  [OK] 已設置 SuperClaude 全域配置"
        echo "  [OK] 已複製所有依賴文件"
        ;;
        
    "merged")
        # 先使用標準模板
        if [ -f "$TEMPLATE_DIR/templates/$PROJECT_TYPE/CLAUDE.md" ]; then
            cp "$TEMPLATE_DIR/templates/$PROJECT_TYPE/CLAUDE.md" "$PROJECT_PATH/CLAUDE.md"
        else
            cp "$TEMPLATE_DIR/templates/CLAUDE.md.template" "$PROJECT_PATH/CLAUDE.md"
        fi
        
        # 替換佔位符
        sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PROJECT_TYPE}}/$PROJECT_TYPE/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PRIMARY_LANGUAGE}}/$PRIMARY_LANGUAGE/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{PROJECT_DESCRIPTION}}/$PROJECT_DESCRIPTION/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{CREATED_DATE}}/$(date +%Y-%m-%d)/g" "$PROJECT_PATH/CLAUDE.md"
        sed -i "s/{{VERSION}}/0.1.0/g" "$PROJECT_PATH/CLAUDE.md"
        
        # 添加 SuperClaude 功能區塊
        cat >> "$PROJECT_PATH/CLAUDE.md" << EOF

# SuperClaude 進階功能

## 引用全域配置
如需啟用 SuperClaude 進階功能，可以引用以下配置：

\`\`\`markdown
@include .claude/shared/superclaude-core.yml#Core_Philosophy
@include .claude/shared/superclaude-rules.yml#Development_Practices
@include .claude/shared/superclaude-mcp.yml#Best_Practices
\`\`\`

## 可選功能
- Advanced Token Economy
- UltraCompressed Mode
- Cognitive Archetypes (Personas)
- 中文回覆優化
- 時間意識與同步

詳細配置請參考 global-configs/ 目錄。
EOF
        
        # 複製 SuperClaude 依賴文件以供參考
        mkdir -p "$PROJECT_PATH/.claude/shared"
        cp -r "$TEMPLATE_DIR/global-configs/shared/"* "$PROJECT_PATH/.claude/shared/"
        
        echo "  [OK] 已設置合併配置（標準 + SuperClaude 參考）"
        ;;
esac

# 創建必要目錄
echo -e "${GREEN}創建專案目錄結構...${NC}"
mkdir -p "$PROJECT_PATH/.claude/agents"
mkdir -p "$PROJECT_PATH/.ai-rules"
mkdir -p "$PROJECT_PATH/specs"

# 複製選擇的 Agent 配置
echo -e "${GREEN}設置 Agent 配置...${NC}"
for agent in "${DECLARE_AGENTS[@]}"; do
    if [ -f "$TEMPLATE_DIR/agents/${agent}.yaml" ]; then
        cp "$TEMPLATE_DIR/agents/${agent}.yaml" "$PROJECT_PATH/.claude/agents/${agent}.yaml"
        echo "  [OK] 已添加 ${agent}"
    fi
done

# 如果選擇了 Steering Architect，初始化 .ai-rules
if [[ " ${DECLARE_AGENTS[@]} " =~ " steering-architect-agent " ]]; then
    echo -e "${GREEN}初始化 .ai-rules 文檔...${NC}"
    
    # 創建 product.md
    cat > "$PROJECT_PATH/.ai-rules/product.md" << EOF
---
title: Product Vision
description: "定義專案的核心目的、目標用戶和主要功能"
inclusion: always
---

# $PROJECT_NAME 產品願景

## 核心目的
$PROJECT_DESCRIPTION

## 目標用戶
*待定義*

## 主要功能
*待定義*

## 獨特價值
*待定義*
EOF

    # 創建 tech.md
    cat > "$PROJECT_PATH/.ai-rules/tech.md" << EOF
---
title: Technology Stack
description: "專案使用的技術棧、工具和依賴"
inclusion: always
---

# 技術棧

## 核心技術
- 主要語言: $PRIMARY_LANGUAGE
- 專案類型: $PROJECT_TYPE

## 開發工具
*待定義*

## 測試框架
*待定義*

## 部署環境
*待定義*
EOF

    # 創建 structure.md
    cat > "$PROJECT_PATH/.ai-rules/structure.md" << EOF
---
title: Project Structure
description: "專案的目錄結構和檔案組織規範"
inclusion: always
---

# 專案結構

## 目錄結構
\`\`\`
.
├── .ai-rules/          # AI 指導文檔
├── .claude/            # Claude 配置
│   └── agents/        # Agent 配置
├── specs/              # 功能規格
├── src/                # 源代碼
└── validation-scripts/ # 檢查腳本
\`\`\`

## 命名規範
*待定義*

## 檔案組織原則
*待定義*
EOF
fi

# 創建基礎專案結構
echo -e "${GREEN}創建基礎目錄結構...${NC}"
case $PROJECT_TYPE in
    "flutter-app")
        mkdir -p "$PROJECT_PATH"/{lib/{core,data,presentation},test,assets}
        ;;
    "web-app")
        mkdir -p "$PROJECT_PATH"/{src/{components,pages,services,utils},public,tests}
        ;;
    "api-service")
        mkdir -p "$PROJECT_PATH"/{src/{controllers,models,services,utils},tests,config}
        ;;
    *)
        mkdir -p "$PROJECT_PATH"/{src,tests,docs}
        ;;
esac

# 創建專案特定規則文件
echo -e "${GREEN}創建專案特定規則文件...${NC}"
if [ -f "$TEMPLATE_DIR/templates/PROJECT_SPECIFIC_RULES.template.md" ]; then
    cp "$TEMPLATE_DIR/templates/PROJECT_SPECIFIC_RULES.template.md" "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md"
    # 替換基本佔位符
    sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md"
    sed -i "s/{{LAST_UPDATED}}/$(date +%Y-%m-%d)/g" "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md"
fi

# 創建檢查腳本目錄
echo -e "${GREEN}創建檢查腳本...${NC}"
mkdir -p "$PROJECT_PATH/validation-scripts"

# 複製檢查腳本模板
for script in "$TEMPLATE_DIR/validation-scripts"/*.sh.template; do
    if [ -f "$script" ]; then
        script_name=$(basename "$script" .template)
        cp "$script" "$PROJECT_PATH/validation-scripts/$script_name"
        chmod +x "$PROJECT_PATH/validation-scripts/$script_name"
        
        # 替換佔位符
        case $PROJECT_TYPE in
            "flutter-app")
                sed -i "s/{{SOURCE_DIR}}/lib/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{FILE_EXT}}/dart/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{TEST_COMMAND}}/flutter test/g" "$PROJECT_PATH/validation-scripts/$script_name"
                ;;
            "web-app")
                sed -i "s/{{SOURCE_DIR}}/src/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{FILE_EXT}}/js/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{TEST_COMMAND}}/npm test/g" "$PROJECT_PATH/validation-scripts/$script_name"
                ;;
            *)
                sed -i "s/{{SOURCE_DIR}}/src/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{FILE_EXT}}/*/g" "$PROJECT_PATH/validation-scripts/$script_name"
                sed -i "s/{{TEST_COMMAND}}/echo 'No test command configured'/g" "$PROJECT_PATH/validation-scripts/$script_name"
                ;;
        esac
        
        sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/validation-scripts/$script_name"
        sed -i "s/{{PROJECT_TYPE}}/$PROJECT_TYPE/g" "$PROJECT_PATH/validation-scripts/$script_name"
        sed -i "s/{{PRIMARY_LANGUAGE}}/$PRIMARY_LANGUAGE/g" "$PROJECT_PATH/validation-scripts/$script_name"
        sed -i "s/{{MAX_FILE_LINES}}/500/g" "$PROJECT_PATH/validation-scripts/$script_name"
        sed -i "s/{{CONSTANTS_DIR}}/constants/g" "$PROJECT_PATH/validation-scripts/$script_name"
    fi
done

# 創建 .gitignore
echo -e "${GREEN}創建 .gitignore...${NC}"
cat > "$PROJECT_PATH/.gitignore" << EOF
# 依賴
node_modules/
venv/
.env
.env.local

# 編譯輸出
dist/
build/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系統檔案
.DS_Store
Thumbs.db

# 日誌
logs/
*.log
EOF

# 創建 README.md
echo -e "${GREEN}創建 README.md...${NC}"
cat > "$PROJECT_PATH/README.md" << EOF
# $PROJECT_NAME

$PROJECT_DESCRIPTION

## 開始使用

此專案配置了 CLAUDE.md 和 AI Agent，可以協助您進行開發。

## 專案結構

請查看 CLAUDE.md 了解專案的詳細配置和開發準則。

## Agent 配置

專案啟用了以下 Agent：
$(for agent in "${DECLARE_AGENTS[@]}"; do echo "- $agent"; done)
EOF

# 在 CLAUDE.md 中添加默認值
if [ -f "$PROJECT_PATH/CLAUDE.md" ]; then
    # 設置默認的度量標準值
    sed -i "s/{{MAX_FILE_LINES}}/500/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_METHOD_LINES}}/50/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_COMPLEXITY}}/10/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MIN_TEST_COVERAGE}}/70/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_DUPLICATION}}/5/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_LOAD_TIME}}/3/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_API_RESPONSE}}/500/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_MEMORY_USAGE}}/512MB/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{MAX_CPU_USAGE}}/80/g" "$PROJECT_PATH/CLAUDE.md"
    
    # 設置源目錄和文件擴展名
    case $PROJECT_TYPE in
        "flutter-app")
            sed -i "s/{{SOURCE_DIR}}/lib/g" "$PROJECT_PATH/CLAUDE.md"
            sed -i "s/{{FILE_EXT}}/dart/g" "$PROJECT_PATH/CLAUDE.md"
            ;;
        "web-app")
            sed -i "s/{{SOURCE_DIR}}/src/g" "$PROJECT_PATH/CLAUDE.md"
            sed -i "s/{{FILE_EXT}}/js/g" "$PROJECT_PATH/CLAUDE.md"
            ;;
        *)
            sed -i "s/{{SOURCE_DIR}}/src/g" "$PROJECT_PATH/CLAUDE.md"
            sed -i "s/{{FILE_EXT}}/*/g" "$PROJECT_PATH/CLAUDE.md"
            ;;
    esac
fi

# 創建開發知識庫檔案
echo -e "${GREEN}創建開發知識庫...${NC}"
cat > "$PROJECT_PATH/DEVELOPMENT_KNOWLEDGE_BASE.md" << EOF
# Development Knowledge Base - $PROJECT_NAME

🧠 **$PROJECT_NAME Development Experience** - Technical challenges and solutions

---

## 📋 Contents
1. [Platform/Technology Specific Experiences](#platform-experiences)
2. [Technical Challenges & Solutions](#technical-challenges)
3. [Performance Optimization](#performance-optimization)
4. [Error Handling & Debugging](#error-handling)
5. [Integration Experiences](#integration-experiences)
6. [Best Practices Discovered](#best-practices)
7. [Future Development Guidelines](#future-guidelines)

---

## Platform/Technology Specific Experiences

*待添加...*

## Technical Challenges & Solutions

*待添加...*

---
*Created: $(date +%Y-%m-%d)*
EOF

# 初始化 git
read -p "是否初始化 Git 儲存庫? (y/n): " INIT_GIT
if [ "$INIT_GIT" = "y" ] || [ "$INIT_GIT" = "Y" ]; then
    cd "$PROJECT_PATH"
    git init
    git add .
    git commit -m "Initial commit - Project setup with CLAUDE.md and Agent configuration"
    echo -e "${GREEN}Git 儲存庫已初始化${NC}"
fi

# 完成訊息
echo -e "\n${GREEN}[SUCCESS] 專案創建成功！${NC}"
echo -e "\n${BLUE}專案資訊:${NC}"
echo "- 名稱: $PROJECT_NAME"
echo "- 路徑: $PROJECT_PATH"
echo "- 類型: $PROJECT_TYPE"
echo "- 語言: $PRIMARY_LANGUAGE"
echo "- CLAUDE.md: $CLAUDE_CONFIG"
echo "- Agents: $(echo "${DECLARE_AGENTS[@]}" | wc -w) 個已啟用"

echo -e "\n${YELLOW}下一步:${NC}"
echo "1. cd $PROJECT_NAME"
echo "2. 查看 CLAUDE.md 了解專案配置"
if [ ${#DECLARE_AGENTS[@]} -gt 0 ]; then
    echo "3. 查看 .claude/agents/ 了解 Agent 配置"
fi
if [[ " ${DECLARE_AGENTS[@]} " =~ " steering-architect-agent " ]]; then
    echo "4. 查看 .ai-rules/ 了解專案架構"
fi
if [ "$CLAUDE_CONFIG" = "superclaude" ]; then
    echo "5. SuperClaude 功能已啟用 (高級 Token 管理、中文優化等)"
elif [ "$CLAUDE_CONFIG" = "merged" ]; then
    echo "5. 可選啟用 SuperClaude 功能 (修改 CLAUDE.md 中的 @include)"
fi
echo "6. 查看 PROJECT_SPECIFIC_RULES.md 記錄專案特定規則"
echo "7. 使用 ./validation-scripts/check-all.sh 執行專案檢查"
if [[ " ${DECLARE_AGENTS[@]} " =~ " strategic-planner-agent " ]]; then
    echo "8. 使用 Strategic Planner 創建新功能規格 (specs/)"
fi
echo ""
echo "開始開發！"

echo -e "\n${BLUE}提示: 使用 Claude Code 時，AI 助手會自動識別並遵循專案配置。${NC}"
if [ "$CLAUDE_CONFIG" = "superclaude" ]; then
    echo -e "${YELLOW}SuperClaude 配置啟用 - 享受更強大的 AI 開發體驗！${NC}"
fi