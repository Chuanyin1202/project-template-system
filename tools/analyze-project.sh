#!/bin/bash

# 專案分析腳本
# 用於分析現有專案並生成配置文件

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 模板系統根目錄
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 顯示標題
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       專案分析與配置生成器 v1.0.0      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# 獲取專案路徑
if [ -n "$1" ]; then
    PROJECT_PATH="$1"
else
    read -p "請輸入要分析的專案路徑 (預設為當前目錄): " PROJECT_PATH
    PROJECT_PATH=${PROJECT_PATH:-.}
fi

# 確保路徑存在
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}錯誤: 專案路徑不存在${NC}"
    exit 1
fi

PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")

echo -e "${GREEN}分析專案: $PROJECT_NAME${NC}"
echo -e "${GREEN}路徑: $PROJECT_PATH${NC}"
echo

# 分析函數
detect_language() {
    local languages=()
    
    # JavaScript/TypeScript
    if [ -f "$PROJECT_PATH/package.json" ]; then
        languages+=("JavaScript/TypeScript")
    fi
    
    # Python
    if [ -f "$PROJECT_PATH/requirements.txt" ] || [ -f "$PROJECT_PATH/setup.py" ] || [ -f "$PROJECT_PATH/pyproject.toml" ]; then
        languages+=("Python")
    fi
    
    # Flutter/Dart
    if [ -f "$PROJECT_PATH/pubspec.yaml" ]; then
        languages+=("Dart/Flutter")
    fi
    
    # Java
    if [ -f "$PROJECT_PATH/pom.xml" ] || [ -f "$PROJECT_PATH/build.gradle" ]; then
        languages+=("Java")
    fi
    
    # Go
    if [ -f "$PROJECT_PATH/go.mod" ]; then
        languages+=("Go")
    fi
    
    # Rust
    if [ -f "$PROJECT_PATH/Cargo.toml" ]; then
        languages+=("Rust")
    fi
    
    # Ruby
    if [ -f "$PROJECT_PATH/Gemfile" ]; then
        languages+=("Ruby")
    fi
    
    # PHP
    if [ -f "$PROJECT_PATH/composer.json" ]; then
        languages+=("PHP")
    fi
    
    echo "${languages[@]}"
}

detect_project_type() {
    # Flutter App
    if [ -f "$PROJECT_PATH/pubspec.yaml" ] && grep -q "flutter:" "$PROJECT_PATH/pubspec.yaml" 2>/dev/null; then
        echo "flutter-app"
        return
    fi
    
    # Web App (React/Vue/Angular)
    if [ -f "$PROJECT_PATH/package.json" ]; then
        if grep -q "react\|vue\|@angular" "$PROJECT_PATH/package.json" 2>/dev/null; then
            echo "web-app"
            return
        fi
    fi
    
    # API Service
    if [ -f "$PROJECT_PATH/package.json" ] && grep -q "express\|fastify\|koa" "$PROJECT_PATH/package.json" 2>/dev/null; then
        echo "api-service"
        return
    fi
    
    if [ -f "$PROJECT_PATH/requirements.txt" ] && grep -q "django\|flask\|fastapi" "$PROJECT_PATH/requirements.txt" 2>/dev/null; then
        echo "api-service"
        return
    fi
    
    # ML Project
    if [ -f "$PROJECT_PATH/requirements.txt" ] && grep -q "tensorflow\|pytorch\|scikit-learn" "$PROJECT_PATH/requirements.txt" 2>/dev/null; then
        echo "ml-project"
        return
    fi
    
    echo "basic"
}

analyze_structure() {
    echo -e "${CYAN}分析專案結構...${NC}"
    
    # 計算總檔案數
    local total_files=$(find "$PROJECT_PATH" -type f -not -path "*/\.*" -not -path "*/node_modules/*" -not -path "*/venv/*" | wc -l)
    echo "  總檔案數: $total_files"
    
    # 主要目錄
    echo "  主要目錄:"
    for dir in "$PROJECT_PATH"/*; do
        if [ -d "$dir" ] && [[ ! "$(basename "$dir")" =~ ^\. ]]; then
            local count=$(find "$dir" -type f | wc -l)
            echo "    - $(basename "$dir") ($count 個檔案)"
        fi
    done
}

# 開始分析
echo -e "${BLUE}=== 開始分析專案 ===${NC}\n"

# 1. 偵測語言
echo -e "${CYAN}偵測程式語言...${NC}"
LANGUAGES=($(detect_language))
if [ ${#LANGUAGES[@]} -eq 0 ]; then
    echo "  未偵測到特定語言"
    PRIMARY_LANGUAGE="Unknown"
else
    echo "  偵測到: ${LANGUAGES[*]}"
    PRIMARY_LANGUAGE="${LANGUAGES[0]}"
fi
echo

# 2. 偵測專案類型
echo -e "${CYAN}偵測專案類型...${NC}"
PROJECT_TYPE=$(detect_project_type)
echo "  專案類型: $PROJECT_TYPE"
echo

# 3. 分析專案結構
analyze_structure
echo

# 4. 建議 Agent 配置
echo -e "${BLUE}=== 建議的 Agent 配置 ===${NC}\n"

RECOMMENDED_AGENTS=("steering-architect-agent" "strategic-planner-agent" "task-executor-agent")

case $PROJECT_TYPE in
    "flutter-app")
        RECOMMENDED_AGENTS+=("flutter-developer-agent")
        ;;
    "web-app")
        RECOMMENDED_AGENTS+=("web-developer-agent")
        ;;
    "api-service")
        RECOMMENDED_AGENTS+=("web-developer-agent" "devops-agent")
        ;;
    *)
        RECOMMENDED_AGENTS+=("base-agent")
        ;;
esac

# 根據專案規模建議
if [ $total_files -gt 100 ]; then
    RECOMMENDED_AGENTS+=("quality-assurance-agent" "documentation-agent")
fi

echo "建議啟用的 Agent:"
for agent in "${RECOMMENDED_AGENTS[@]}"; do
    echo "  ✓ $agent"
done
echo

# 5. 詢問是否創建配置
echo -e "${YELLOW}是否要為此專案創建配置文件？${NC}"
echo "這將創建:"
echo "  - CLAUDE.md (專案配置)"
echo "  - .claude/agents/ (Agent 配置)"
echo "  - .ai-rules/ (架構文檔)"
echo "  - validation-scripts/ (檢查腳本)"
echo

read -p "繼續？(y/n): " CONTINUE

if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
    echo "已取消"
    exit 0
fi

# 6. 創建配置
echo -e "\n${GREEN}創建配置文件...${NC}"

# 創建 CLAUDE.md
if [ ! -f "$PROJECT_PATH/CLAUDE.md" ]; then
    echo "  創建 CLAUDE.md..."
    cp "$TEMPLATE_DIR/templates/CLAUDE.md.template" "$PROJECT_PATH/CLAUDE.md"
    
    # 替換佔位符
    sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{PROJECT_TYPE}}/$PROJECT_TYPE/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{PRIMARY_LANGUAGE}}/$PRIMARY_LANGUAGE/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{CREATED_DATE}}/$(date +%Y-%m-%d)/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{VERSION}}/0.1.0/g" "$PROJECT_PATH/CLAUDE.md"
    
    # 設置默認值
    sed -i "s/{{PROJECT_DESCRIPTION}}/待補充專案描述/g" "$PROJECT_PATH/CLAUDE.md"
    sed -i "s/{{PROJECT_GOALS}}/待定義專案目標/g" "$PROJECT_PATH/CLAUDE.md"
else
    echo "  CLAUDE.md 已存在，跳過"
fi

# 創建 .claude/agents 目錄
echo "  設置 Agent 配置..."
mkdir -p "$PROJECT_PATH/.claude/agents"

for agent in "${RECOMMENDED_AGENTS[@]}"; do
    if [ -f "$TEMPLATE_DIR/agents/${agent}.yaml" ]; then
        cp "$TEMPLATE_DIR/agents/${agent}.yaml" "$PROJECT_PATH/.claude/agents/"
        echo "    ✓ 已添加 $agent"
    fi
done

# 創建 .ai-rules 目錄和文件
if [[ " ${RECOMMENDED_AGENTS[@]} " =~ " steering-architect-agent " ]]; then
    echo "  初始化 .ai-rules..."
    mkdir -p "$PROJECT_PATH/.ai-rules"
    
    # 創建基礎文件
    for file in product tech structure; do
        if [ ! -f "$PROJECT_PATH/.ai-rules/${file}.md" ]; then
            touch "$PROJECT_PATH/.ai-rules/${file}.md"
            echo "    ✓ 創建 ${file}.md"
        fi
    done
fi

# 創建其他必要文件
if [ ! -f "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md" ]; then
    echo "  創建 PROJECT_SPECIFIC_RULES.md..."
    cp "$TEMPLATE_DIR/templates/PROJECT_SPECIFIC_RULES.template.md" "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md"
    sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$PROJECT_PATH/PROJECT_SPECIFIC_RULES.md"
fi

# 創建檢查腳本
echo "  設置檢查腳本..."
mkdir -p "$PROJECT_PATH/validation-scripts"
for script in "$TEMPLATE_DIR/validation-scripts"/*.sh.template; do
    if [ -f "$script" ]; then
        script_name=$(basename "$script" .template)
        cp "$script" "$PROJECT_PATH/validation-scripts/$script_name"
        chmod +x "$PROJECT_PATH/validation-scripts/$script_name"
    fi
done

echo -e "\n${GREEN}✅ 配置完成！${NC}"
echo
echo "下一步:"
echo "1. 使用 Steering Architect Agent 分析專案並完善 .ai-rules/ 文檔"
echo "2. 查看並自定義 CLAUDE.md"
echo "3. 開始使用 Agent 進行開發"
echo
echo -e "${BLUE}提示: 使用 'claude' 命令時，AI 助手會自動識別這些配置。${NC}"