#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Template System - 專案初始化工具
完整支援 Agent 選擇和配置的跨平台初始化腳本
v1.3.0 - 完整功能版本
"""

import os
import sys
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import platform

# 顏色輸出支援
class Colors:
    """終端顏色定義"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def disable():
        """Windows 舊版本可能需要禁用顏色"""
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.ENDC = ''
        Colors.BOLD = ''

# Windows 舊版本檢測
if platform.system() == 'Windows' and sys.version_info < (3, 6):
    Colors.disable()

def print_banner():
    """顯示歡迎橫幅"""
    print(f"""
{Colors.BLUE}╔════════════════════════════════════════╗
║      專案模板初始化系統 v1.3.0        ║
╚════════════════════════════════════════╝{Colors.ENDC}
    """)

def get_script_dir():
    """獲取腳本所在目錄"""
    return Path(__file__).parent.absolute()

def get_project_root():
    """獲取專案根目錄"""
    return get_script_dir().parent

def load_config():
    """載入配置文件"""
    config_path = get_project_root() / 'config' / 'project-types.json'
    if not config_path.exists():
        print(f"{Colors.RED}錯誤：找不到配置文件 {config_path}{Colors.ENDC}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_user_input(prompt, options=None, default=None):
    """獲取用戶輸入，支援選項驗證"""
    while True:
        user_input = input(prompt).strip()
        if default and not user_input:
            return default
        if options and user_input not in options:
            print(f"{Colors.RED}無效的選擇，請重新輸入{Colors.ENDC}")
            continue
        if user_input or default:
            return user_input
        print(f"{Colors.RED}輸入不能為空{Colors.ENDC}")

def select_project_type():
    """選擇專案類型"""
    print(f"\n{Colors.YELLOW}請選擇專案類型：{Colors.ENDC}")
    print("1) 基礎專案 (Basic Project)")
    print("2) Web 應用 (Web Application)")
    print("3) API 服務 (API Service)")
    print("4) Flutter 應用 (Flutter App)")
    print("5) 機器學習專案 (ML Project)")
    print("6) 自定義 (Custom)")
    
    choice = get_user_input("選擇 (1-6): ", ['1', '2', '3', '4', '5', '6'])
    
    type_map = {
        '1': 'basic',
        '2': 'web-app',
        '3': 'api-service',
        '4': 'flutter-app',
        '5': 'ml-project',
        '6': 'custom'
    }
    
    return type_map[choice]

def select_language():
    """選擇主要語言"""
    print(f"\n{Colors.YELLOW}請選擇主要程式語言：{Colors.ENDC}")
    print("1) JavaScript/TypeScript")
    print("2) Python")
    print("3) Dart (Flutter)")
    print("4) Java")
    print("5) Go")
    print("6) 其他")
    
    choice = get_user_input("選擇 (1-6): ", ['1', '2', '3', '4', '5', '6'])
    
    lang_map = {
        '1': 'JavaScript/TypeScript',
        '2': 'Python',
        '3': 'Dart',
        '4': 'Java',
        '5': 'Go'
    }
    
    if choice == '6':
        return get_user_input("請輸入語言名稱: ")
    
    return lang_map[choice]

def select_claude_config():
    """選擇 CLAUDE.md 配置類型"""
    print(f"\n{Colors.YELLOW}請選擇 CLAUDE.md 配置類型：{Colors.ENDC}")
    print("1) 標準專案配置 (適合一般開發)")
    print("2) SuperClaude 全域配置 (高級功能完整版)")
    print("3) 合併配置 (結合兩者優勢)")
    
    choice = get_user_input("選擇 (1-3): ", ['1', '2', '3'])
    
    config_map = {
        '1': 'standard',
        '2': 'superclaude',
        '3': 'merged'
    }
    
    return config_map[choice]

def select_mode():
    """選擇模式"""
    print(f"\n{Colors.YELLOW}請選擇模式：{Colors.ENDC}")
    print("1) 創建新專案")
    print("2) 分析現有專案")
    print("3) 混合模式 (分析後增強)")
    
    choice = get_user_input("選擇 (1-3): ", ['1', '2', '3'])
    
    mode_map = {
        '1': 'new',
        '2': 'analyze',
        '3': 'hybrid'
    }
    
    return mode_map[choice]

def select_agents():
    """選擇要啟用的 Agent"""
    print(f"\n{Colors.YELLOW}請選擇要啟用的 Agent：{Colors.ENDC}")
    print(f"{Colors.GREEN}架構層：{Colors.ENDC}")
    print("  1) Steering Architect - 專案架構師")
    print(f"{Colors.GREEN}規劃層：{Colors.ENDC}")
    print("  2) Strategic Planner - 需求規劃師")
    print(f"{Colors.GREEN}執行層：{Colors.ENDC}")
    print("  3) Task Executor - 任務執行器")
    print("  4) Flutter Developer - Flutter 專家")
    print("  5) Web Developer - Web 專家")
    print("  6) Base Developer - 通用開發者")
    print(f"{Colors.GREEN}品質層：{Colors.ENDC}")
    print("  7) Quality Assurance - 測試專家")
    print(f"{Colors.GREEN}運維層：{Colors.ENDC}")
    print("  8) DevOps Agent - 部署專家")
    print(f"{Colors.GREEN}文檔層：{Colors.ENDC}")
    print("  9) Documentation - 文檔專家")
    print()
    print("預設組合:")
    print("  A) 完整團隊 (1-9 全部)")
    print("  B) 開發團隊 (2-6)")
    print("  C) 最小團隊 (2,3,6)")
    print("  D) 自定義選擇")
    
    preset = get_user_input("選擇 (A/B/C/D): ", ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd']).upper()
    
    preset_map = {
        'A': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'B': [2, 3, 4, 5, 6],
        'C': [2, 3, 6],
    }
    
    if preset == 'D':
        agents_input = get_user_input("輸入 Agent 編號 (空格分隔): ")
        selected_numbers = [int(x) for x in agents_input.split() if x.isdigit() and 1 <= int(x) <= 9]
    else:
        selected_numbers = preset_map[preset]
    
    # 將數字轉換為 Agent 名稱
    agent_map = {
        1: 'steering-architect-agent',
        2: 'strategic-planner-agent',
        3: 'task-executor-agent',
        4: 'flutter-developer-agent',
        5: 'web-developer-agent',
        6: 'base-agent',
        7: 'quality-assurance-agent',
        8: 'devops-agent',
        9: 'documentation-agent'
    }
    
    return [agent_map[num] for num in selected_numbers]

def create_directory_structure(project_path, project_type):
    """創建專案目錄結構"""
    base_dirs = [
        '.claude/agents',
        '.ai-rules',
        'specs',
        'validation-scripts'
    ]
    
    # 創建基本目錄
    for dir_path in base_dirs:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    # 根據專案類型創建特定目錄
    if project_type == 'flutter-app':
        dirs = ['lib/core', 'lib/data', 'lib/presentation', 'test', 'assets']
    elif project_type == 'web-app':
        dirs = ['src/components', 'src/pages', 'src/services', 'src/utils', 'public', 'tests']
    elif project_type == 'api-service':
        dirs = ['src/controllers', 'src/models', 'src/services', 'src/utils', 'tests', 'config']
    else:
        dirs = ['src', 'tests', 'docs']
    
    for dir_path in dirs:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 創建目錄結構")

def setup_claude_config(project_path, config_type, project_info):
    """設置 CLAUDE.md 配置"""
    template_dir = get_project_root() / 'templates'
    global_config_dir = get_project_root() / 'global-configs'
    
    if config_type == 'standard':
        # 使用標準模板
        template_file = template_dir / project_info['type'] / 'CLAUDE.md'
        if not template_file.exists():
            template_file = template_dir / 'CLAUDE.md.template'
        
        if template_file.exists():
            content = template_file.read_text(encoding='utf-8')
            # 替換佔位符
            replacements = {
                '{{PROJECT_NAME}}': project_info['name'],
                '{{PROJECT_TYPE}}': project_info['type'],
                '{{PRIMARY_LANGUAGE}}': project_info['language'],
                '{{PROJECT_DESCRIPTION}}': project_info['description'],
                '{{CREATED_DATE}}': datetime.now().strftime('%Y-%m-%d'),
                '{{VERSION}}': '0.1.0'
            }
            for key, value in replacements.items():
                content = content.replace(key, value)
            
            (project_path / 'CLAUDE.md').write_text(content, encoding='utf-8')
            print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 已設置標準專案配置")
    
    elif config_type == 'superclaude':
        # 使用 SuperClaude 全域配置
        claude_file = global_config_dir / 'CLAUDE.md'
        if claude_file.exists():
            shutil.copy2(claude_file, project_path / 'CLAUDE.md')
        
        # 複製依賴文件
        for subdir in ['commands', 'shared']:
            src_dir = global_config_dir / subdir
            if src_dir.exists():
                dst_dir = project_path / '.claude' / subdir
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        
        print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 已設置 SuperClaude 全域配置")
        print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 已複製所有依賴文件")
    
    elif config_type == 'merged':
        # 合併配置
        # 先使用標準模板
        template_file = template_dir / project_info['type'] / 'CLAUDE.md'
        if not template_file.exists():
            template_file = template_dir / 'CLAUDE.md.template'
        
        if template_file.exists():
            content = template_file.read_text(encoding='utf-8')
            # 替換佔位符
            replacements = {
                '{{PROJECT_NAME}}': project_info['name'],
                '{{PROJECT_TYPE}}': project_info['type'],
                '{{PRIMARY_LANGUAGE}}': project_info['language'],
                '{{PROJECT_DESCRIPTION}}': project_info['description'],
                '{{CREATED_DATE}}': datetime.now().strftime('%Y-%m-%d'),
                '{{VERSION}}': '0.1.0'
            }
            for key, value in replacements.items():
                content = content.replace(key, value)
            
            # 添加 SuperClaude 功能區塊
            content += """

# SuperClaude 進階功能

## 引用全域配置
如需啟用 SuperClaude 進階功能，可以引用以下配置：

```markdown
@include .claude/shared/superclaude-core.yml#Core_Philosophy
@include .claude/shared/superclaude-rules.yml#Development_Practices
@include .claude/shared/superclaude-mcp.yml#Best_Practices
```

## 可選功能
- Advanced Token Economy
- UltraCompressed Mode
- Cognitive Archetypes (Personas)
- 中文回覆優化
- 時間意識與同步

詳細配置請參考 global-configs/ 目錄。
"""
            
            (project_path / 'CLAUDE.md').write_text(content, encoding='utf-8')
            
            # 複製 SuperClaude 依賴文件以供參考
            shared_dir = global_config_dir / 'shared'
            if shared_dir.exists():
                dst_dir = project_path / '.claude' / 'shared'
                shutil.copytree(shared_dir, dst_dir, dirs_exist_ok=True)
            
            print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 已設置合併配置（標準 + SuperClaude 參考）")

def copy_agent_configs(project_path, selected_agents):
    """複製選擇的 Agent 配置"""
    agents_dir = get_project_root() / 'agents'
    target_dir = project_path / '.claude' / 'agents'
    
    for agent in selected_agents:
        agent_file = agents_dir / f'{agent}.yaml'
        if agent_file.exists():
            shutil.copy2(agent_file, target_dir / f'{agent}.yaml')
            print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 已添加 {agent}")

def initialize_ai_rules(project_path, project_info):
    """初始化 .ai-rules 文檔"""
    ai_rules_dir = project_path / '.ai-rules'
    
    # 創建 product.md
    product_content = f"""---
title: Product Vision
description: "定義專案的核心目的、目標用戶和主要功能"
inclusion: always
---

# {project_info['name']} 產品願景

## 核心目的
{project_info['description']}

## 目標用戶
*待定義*

## 主要功能
*待定義*

## 獨特價值
*待定義*
"""
    (ai_rules_dir / 'product.md').write_text(product_content, encoding='utf-8')
    
    # 創建 tech.md
    tech_content = f"""---
title: Technology Stack
description: "專案使用的技術棧、工具和依賴"
inclusion: always
---

# 技術棧

## 核心技術
- 主要語言: {project_info['language']}
- 專案類型: {project_info['type']}

## 開發工具
*待定義*

## 測試框架
*待定義*

## 部署環境
*待定義*
"""
    (ai_rules_dir / 'tech.md').write_text(tech_content, encoding='utf-8')
    
    # 創建 structure.md
    structure_content = """---
title: Project Structure
description: "專案的目錄結構和檔案組織規範"
inclusion: always
---

# 專案結構

## 目錄結構
```
.
├── .ai-rules/          # AI 指導文檔
├── .claude/            # Claude 配置
│   └── agents/        # Agent 配置
├── specs/              # 功能規格
├── src/                # 源代碼
└── validation-scripts/ # 檢查腳本
```

## 命名規範
*待定義*

## 檔案組織原則
*待定義*
"""
    (ai_rules_dir / 'structure.md').write_text(structure_content, encoding='utf-8')
    
    print(f"{Colors.GREEN}初始化 .ai-rules 文檔...{Colors.ENDC}")

def create_project_files(project_path, project_info, selected_agents):
    """創建專案文件"""
    # 創建 PROJECT_SPECIFIC_RULES.md
    template_path = get_project_root() / 'templates' / 'PROJECT_SPECIFIC_RULES.template.md'
    if template_path.exists():
        content = template_path.read_text(encoding='utf-8')
        content = content.replace('{{PROJECT_NAME}}', project_info['name'])
        content = content.replace('{{LAST_UPDATED}}', datetime.now().strftime('%Y-%m-%d'))
        (project_path / 'PROJECT_SPECIFIC_RULES.md').write_text(content, encoding='utf-8')
    
    # 創建 .gitignore
    gitignore_content = """# 依賴
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
"""
    (project_path / '.gitignore').write_text(gitignore_content, encoding='utf-8')
    
    # 創建 README.md
    readme_content = f"""# {project_info['name']}

{project_info['description']}

## 開始使用

此專案配置了 CLAUDE.md 和 AI Agent，可以協助您進行開發。

## 專案結構

請查看 CLAUDE.md 了解專案的詳細配置和開發準則。

## Agent 配置

專案啟用了以下 Agent：
"""
    for agent in selected_agents:
        readme_content += f"\n- {agent}"
    
    (project_path / 'README.md').write_text(readme_content, encoding='utf-8')
    
    # 創建開發知識庫
    knowledge_base_content = f"""# Development Knowledge Base - {project_info['name']}

🧠 **{project_info['name']} Development Experience** - Technical challenges and solutions

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
*Created: {datetime.now().strftime('%Y-%m-%d')}*
"""
    (project_path / 'DEVELOPMENT_KNOWLEDGE_BASE.md').write_text(knowledge_base_content, encoding='utf-8')

def copy_validation_scripts(project_path, project_type):
    """複製驗證腳本"""
    validation_dir = project_path / 'validation-scripts'
    validation_dir.mkdir(exist_ok=True)
    
    # 複製 Python 驗證腳本
    scripts_dir = get_project_root() / 'validation-scripts'
    for script in ['validator.py', 'check-all.py', 'check-code-quality.py', 
                   'check-security.py', 'check-duplicates.py']:
        src = scripts_dir / script
        if src.exists():
            shutil.copy2(src, validation_dir / script)
    
    # 創建專案特定的配置文件
    config = {
        "source_dir": "lib" if project_type == "flutter-app" else "src",
        "file_extensions": {
            "flutter-app": [".dart"],
            "web-app": [".js", ".ts", ".jsx", ".tsx"],
            "api-service": [".js", ".ts", ".py"],
            "basic": [".py", ".js", ".ts"]
        }.get(project_type, [".py", ".js", ".ts"]),
        "max_file_lines": 500,
        "max_line_length": 120,
        "max_function_lines": 50,
        "max_complexity": 10,
        "project_type": project_type
    }
    
    config_path = validation_dir / 'validation-config.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"  {Colors.GREEN}[OK]{Colors.ENDC} 創建驗證腳本")

def setup_git_repo(project_path):
    """初始化 Git 倉庫"""
    try:
        subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)
        subprocess.run(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Project setup with CLAUDE.md and Agent configuration'], 
                      cwd=project_path, check=True, capture_output=True)
        print(f"{Colors.GREEN}Git 儲存庫已初始化{Colors.ENDC}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.YELLOW}Git 未安裝或初始化失敗{Colors.ENDC}")
        return False

def show_completion_message(project_info, selected_agents):
    """顯示完成訊息"""
    print(f"\n{Colors.GREEN}[SUCCESS] 專案創建成功！{Colors.ENDC}")
    print(f"\n{Colors.BLUE}專案資訊：{Colors.ENDC}")
    print(f"- 名稱: {project_info['name']}")
    print(f"- 路徑: {project_info['path']}")
    print(f"- 類型: {project_info['type']}")
    print(f"- 語言: {project_info['language']}")
    print(f"- CLAUDE.md: {project_info['claude_config']}")
    print(f"- Agents: {len(selected_agents)} 個已啟用")
    
    print(f"\n{Colors.YELLOW}下一步：{Colors.ENDC}")
    print(f"1. cd {project_info['name']}")
    print("2. 查看 CLAUDE.md 了解專案配置")
    if selected_agents:
        print("3. 查看 .claude/agents/ 了解 Agent 配置")
    if 'steering-architect-agent' in selected_agents:
        print("4. 查看 .ai-rules/ 了解專案架構")
    if project_info['claude_config'] == 'superclaude':
        print("5. SuperClaude 功能已啟用 (高級 Token 管理、中文優化等)")
    elif project_info['claude_config'] == 'merged':
        print("5. 可選啟用 SuperClaude 功能 (修改 CLAUDE.md 中的 @include)")
    print("6. 查看 PROJECT_SPECIFIC_RULES.md 記錄專案特定規則")
    print("7. 使用 python validation-scripts/check-all.py 執行專案檢查")
    if 'strategic-planner-agent' in selected_agents:
        print("8. 使用 Strategic Planner 創建新功能規格 (specs/)")
    
    print("\n開始開發！")
    print(f"\n{Colors.BLUE}提示: 使用 Claude Code 時，AI 助手會自動識別並遵循專案配置。{Colors.ENDC}")
    if project_info['claude_config'] == 'superclaude':
        print(f"{Colors.YELLOW}SuperClaude 配置啟用 - 享受更強大的 AI 開發體驗！{Colors.ENDC}")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='Project Template System - 專案初始化工具')
    parser.add_argument('project_name', nargs='?', help='專案名稱')
    parser.add_argument('-t', '--type', help='專案類型')
    parser.add_argument('-p', '--path', help='專案路徑（預設為當前目錄）')
    parser.add_argument('--no-git', action='store_true', help='不初始化 Git 倉庫')
    parser.add_argument('--no-interactive', action='store_true', help='非互動模式')
    
    args = parser.parse_args()
    
    print_banner()
    
    # 互動式輸入
    if args.no_interactive:
        # 非互動模式需要所有必要參數
        if not args.project_name or not args.type:
            print(f"{Colors.RED}錯誤：非互動模式需要指定專案名稱和類型{Colors.ENDC}")
            sys.exit(1)
        
        project_info = {
            'name': args.project_name,
            'type': args.type,
            'description': f'{args.project_name} project',
            'language': 'Python',
            'claude_config': 'standard',
            'mode': 'new'
        }
        selected_agents = ['strategic-planner-agent', 'task-executor-agent', 'base-agent']
    else:
        # 獲取專案名稱
        project_name = args.project_name or get_user_input("請輸入專案名稱: ")
        
        # 選擇專案類型
        project_type = args.type or select_project_type()
        
        # 獲取專案描述
        project_description = get_user_input("請輸入專案描述: ")
        
        # 選擇主要語言
        primary_language = select_language()
        
        # 選擇 CLAUDE.md 配置類型
        claude_config = select_claude_config()
        
        # 選擇模式
        mode = select_mode()
        
        # 選擇 Agent
        selected_agents = select_agents()
        
        project_info = {
            'name': project_name,
            'type': project_type,
            'description': project_description,
            'language': primary_language,
            'claude_config': claude_config,
            'mode': mode
        }
    
    # 確定專案路徑
    if args.path:
        project_path = Path(args.path) / project_info['name']
    else:
        project_path = Path.cwd() / project_info['name']
    
    project_info['path'] = str(project_path)
    
    # 檢查目錄是否存在
    if project_path.exists() and project_info['mode'] == 'new':
        print(f"{Colors.RED}錯誤：目錄 {project_path} 已存在{Colors.ENDC}")
        sys.exit(1)
    
    # 創建專案
    print(f"\n{Colors.GREEN}正在創建專案結構...{Colors.ENDC}")
    project_path.mkdir(parents=True, exist_ok=True)
    
    # 創建目錄結構
    create_directory_structure(project_path, project_info['type'])
    
    # 設置 CLAUDE.md
    print(f"{Colors.GREEN}設置 CLAUDE.md 配置...{Colors.ENDC}")
    setup_claude_config(project_path, project_info['claude_config'], project_info)
    
    # 複製 Agent 配置
    if selected_agents:
        print(f"{Colors.GREEN}設置 Agent 配置...{Colors.ENDC}")
        copy_agent_configs(project_path, selected_agents)
    
    # 如果選擇了 Steering Architect，初始化 .ai-rules
    if 'steering-architect-agent' in selected_agents:
        initialize_ai_rules(project_path, project_info)
    
    # 創建專案文件
    print(f"{Colors.GREEN}創建專案文件...{Colors.ENDC}")
    create_project_files(project_path, project_info, selected_agents)
    
    # 複製驗證腳本
    print(f"{Colors.GREEN}創建檢查腳本...{Colors.ENDC}")
    copy_validation_scripts(project_path, project_info['type'])
    
    # 初始化 Git
    if not args.no_git:
        init_git = True
        if not args.no_interactive:
            response = get_user_input("是否初始化 Git 儲存庫? (y/n): ", ['y', 'Y', 'n', 'N'])
            init_git = response.lower() == 'y'
        
        if init_git:
            setup_git_repo(project_path)
    
    # 顯示完成訊息
    show_completion_message(project_info, selected_agents)

if __name__ == '__main__':
    main()