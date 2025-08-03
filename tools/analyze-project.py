#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Analyzer - 專案分析與配置生成器
分析現有專案並生成適合的配置文件
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import platform
import re

# 顏色輸出支援
class Colors:
    """終端顏色定義"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def disable():
        """Windows 舊版本可能需要禁用顏色"""
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.CYAN = ''
        Colors.ENDC = ''
        Colors.BOLD = ''

# Windows 舊版本檢測
if platform.system() == 'Windows' and sys.version_info < (3, 6):
    Colors.disable()

class ProjectAnalyzer:
    """專案分析器"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_name = project_path.name
        self.analysis_results = {
            'project_name': self.project_name,
            'project_path': str(project_path),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'languages': [],
            'project_type': None,
            'frameworks': [],
            'structure': {},
            'dependencies': {},
            'metrics': {},
            'recommendations': []
        }
    
    def analyze(self):
        """執行完整分析"""
        print(f"\n{Colors.GREEN}分析專案: {self.project_name}{Colors.ENDC}")
        print(f"{Colors.GREEN}路徑: {self.project_path}{Colors.ENDC}\n")
        
        # 各項分析
        self.detect_languages()
        self.detect_project_type()
        self.detect_frameworks()
        self.analyze_structure()
        self.analyze_dependencies()
        self.calculate_metrics()
        self.generate_recommendations()
        
        return self.analysis_results
    
    def detect_languages(self):
        """檢測使用的程式語言"""
        print(f"{Colors.CYAN}檢測程式語言...{Colors.ENDC}")
        languages = []
        
        # 檢測各種語言的特徵文件
        language_indicators = {
            'JavaScript/TypeScript': ['package.json', '*.js', '*.ts', '*.jsx', '*.tsx'],
            'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', '*.py'],
            'Dart/Flutter': ['pubspec.yaml', '*.dart'],
            'Java': ['pom.xml', 'build.gradle', '*.java'],
            'Go': ['go.mod', '*.go'],
            'Rust': ['Cargo.toml', '*.rs'],
            'Ruby': ['Gemfile', '*.rb'],
            'PHP': ['composer.json', '*.php'],
            'C#': ['*.csproj', '*.cs'],
            'Swift': ['Package.swift', '*.swift']
        }
        
        for language, indicators in language_indicators.items():
            for indicator in indicators:
                if indicator.startswith('*'):
                    # 檢查文件擴展名
                    if list(self.project_path.rglob(indicator)):
                        languages.append(language)
                        break
                else:
                    # 檢查特定文件
                    if (self.project_path / indicator).exists():
                        languages.append(language)
                        break
        
        self.analysis_results['languages'] = list(set(languages))
        for lang in self.analysis_results['languages']:
            print(f"  {Colors.GREEN}✓{Colors.ENDC} {lang}")
    
    def detect_project_type(self):
        """檢測專案類型"""
        print(f"\n{Colors.CYAN}檢測專案類型...{Colors.ENDC}")
        
        # Flutter App
        if (self.project_path / 'pubspec.yaml').exists():
            with open(self.project_path / 'pubspec.yaml', 'r', encoding='utf-8') as f:
                if 'flutter:' in f.read():
                    self.analysis_results['project_type'] = 'flutter-app'
                    print(f"  {Colors.GREEN}✓{Colors.ENDC} Flutter 應用")
                    return
        
        # Web App
        if (self.project_path / 'package.json').exists():
            with open(self.project_path / 'package.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if any(framework in content for framework in ['react', 'vue', 'angular', 'next', 'nuxt']):
                    self.analysis_results['project_type'] = 'web-app'
                    print(f"  {Colors.GREEN}✓{Colors.ENDC} Web 應用")
                    return
        
        # API Service
        if any((self.project_path / name).exists() for name in ['app.py', 'main.py', 'server.js', 'index.js']):
            # 檢查是否有 API 框架
            api_files = ['routes', 'controllers', 'api', 'endpoints']
            if any((self.project_path / name).exists() for name in api_files):
                self.analysis_results['project_type'] = 'api-service'
                print(f"  {Colors.GREEN}✓{Colors.ENDC} API 服務")
                return
        
        # CLI Tool
        if (self.project_path / 'setup.py').exists() or (self.project_path / 'cli.py').exists():
            self.analysis_results['project_type'] = 'cli-tool'
            print(f"  {Colors.GREEN}✓{Colors.ENDC} CLI 工具")
            return
        
        # Library/Package
        if any((self.project_path / name).exists() for name in ['setup.py', 'package.json', 'Cargo.toml']):
            self.analysis_results['project_type'] = 'library'
            print(f"  {Colors.GREEN}✓{Colors.ENDC} 函式庫/套件")
            return
        
        # Default
        self.analysis_results['project_type'] = 'generic'
        print(f"  {Colors.YELLOW}⚠{Colors.ENDC} 通用專案")
    
    def detect_frameworks(self):
        """檢測使用的框架"""
        print(f"\n{Colors.CYAN}檢測框架...{Colors.ENDC}")
        frameworks = []
        
        # JavaScript 框架
        if (self.project_path / 'package.json').exists():
            try:
                with open(self.project_path / 'package.json', 'r', encoding='utf-8') as f:
                    package_json = json.load(f)
                    deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
                    
                    framework_map = {
                        'react': 'React',
                        'vue': 'Vue.js',
                        '@angular/core': 'Angular',
                        'next': 'Next.js',
                        'nuxt': 'Nuxt.js',
                        'express': 'Express.js',
                        'fastify': 'Fastify',
                        'nest': 'NestJS'
                    }
                    
                    for key, name in framework_map.items():
                        if key in deps:
                            frameworks.append(name)
            except Exception as e:
                print(f"  {Colors.YELLOW}⚠{Colors.ENDC} 無法解析 package.json: {e}")
        
        # Python 框架
        if (self.project_path / 'requirements.txt').exists():
            try:
                with open(self.project_path / 'requirements.txt', 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                    framework_map = {
                        'django': 'Django',
                        'flask': 'Flask',
                        'fastapi': 'FastAPI',
                        'pytest': 'PyTest',
                        'pandas': 'Pandas',
                        'numpy': 'NumPy'
                    }
                    
                    for key, name in framework_map.items():
                        if key in content:
                            frameworks.append(name)
            except Exception as e:
                print(f"  {Colors.YELLOW}⚠{Colors.ENDC} 無法解析 requirements.txt: {e}")
        
        self.analysis_results['frameworks'] = frameworks
        for framework in frameworks:
            print(f"  {Colors.GREEN}✓{Colors.ENDC} {framework}")
    
    def analyze_structure(self):
        """分析專案結構"""
        print(f"\n{Colors.CYAN}分析專案結構...{Colors.ENDC}")
        
        structure = {
            'directories': [],
            'key_files': [],
            'total_files': 0,
            'file_types': {}
        }
        
        # 統計目錄和文件
        for item in self.project_path.rglob('*'):
            if any(skip in str(item) for skip in ['node_modules', '__pycache__', '.git', 'venv', 'build', 'dist']):
                continue
            
            if item.is_dir():
                rel_path = item.relative_to(self.project_path)
                if len(rel_path.parts) <= 2:  # 只記錄前兩層目錄
                    structure['directories'].append(str(rel_path))
            elif item.is_file():
                structure['total_files'] += 1
                ext = item.suffix.lower()
                structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
                
                # 記錄關鍵文件
                key_files = ['README.md', 'CLAUDE.md', 'package.json', 'requirements.txt', 
                           'pubspec.yaml', 'Dockerfile', '.gitignore']
                if item.name in key_files:
                    structure['key_files'].append(item.name)
        
        self.analysis_results['structure'] = structure
        print(f"  總文件數: {structure['total_files']}")
        print(f"  目錄數: {len(structure['directories'])}")
        print(f"  主要文件類型: {', '.join(f'{k}({v})' for k, v in sorted(structure['file_types'].items(), key=lambda x: x[1], reverse=True)[:5])}")
    
    def analyze_dependencies(self):
        """分析依賴關係"""
        print(f"\n{Colors.CYAN}分析依賴關係...{Colors.ENDC}")
        
        dependencies = {
            'total': 0,
            'dev': 0,
            'outdated': []
        }
        
        # JavaScript 依賴
        if (self.project_path / 'package.json').exists():
            try:
                with open(self.project_path / 'package.json', 'r', encoding='utf-8') as f:
                    package_json = json.load(f)
                    dependencies['total'] = len(package_json.get('dependencies', {}))
                    dependencies['dev'] = len(package_json.get('devDependencies', {}))
            except:
                pass
        
        # Python 依賴
        elif (self.project_path / 'requirements.txt').exists():
            try:
                with open(self.project_path / 'requirements.txt', 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    dependencies['total'] = len(lines)
            except:
                pass
        
        self.analysis_results['dependencies'] = dependencies
        print(f"  生產依賴: {dependencies['total']}")
        print(f"  開發依賴: {dependencies['dev']}")
    
    def calculate_metrics(self):
        """計算專案指標"""
        print(f"\n{Colors.CYAN}計算專案指標...{Colors.ENDC}")
        
        metrics = {
            'lines_of_code': 0,
            'test_files': 0,
            'documentation_files': 0,
            'config_files': 0
        }
        
        # 統計代碼行數和文件類型
        code_extensions = ['.py', '.js', '.ts', '.dart', '.java', '.go', '.rs']
        test_patterns = ['test_', '_test', 'spec.', '.spec', 'tests/', 'test/']
        doc_extensions = ['.md', '.rst', '.txt']
        config_patterns = ['.json', '.yml', '.yaml', '.toml', '.ini']
        
        for file_path in self.project_path.rglob('*'):
            if any(skip in str(file_path) for skip in ['node_modules', '__pycache__', '.git', 'venv']):
                continue
            
            if file_path.is_file():
                # 統計代碼行數
                if file_path.suffix in code_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            metrics['lines_of_code'] += len(f.readlines())
                    except:
                        pass
                
                # 統計測試文件
                if any(pattern in str(file_path).lower() for pattern in test_patterns):
                    metrics['test_files'] += 1
                
                # 統計文檔文件
                if file_path.suffix in doc_extensions:
                    metrics['documentation_files'] += 1
                
                # 統計配置文件
                if file_path.suffix in config_patterns:
                    metrics['config_files'] += 1
        
        self.analysis_results['metrics'] = metrics
        print(f"  代碼行數: {metrics['lines_of_code']:,}")
        print(f"  測試文件: {metrics['test_files']}")
        print(f"  文檔文件: {metrics['documentation_files']}")
        print(f"  配置文件: {metrics['config_files']}")
    
    def generate_recommendations(self):
        """生成建議"""
        print(f"\n{Colors.CYAN}生成建議...{Colors.ENDC}")
        recommendations = []
        
        # 檢查 CLAUDE.md
        if not (self.project_path / 'CLAUDE.md').exists() and not (self.project_path / '.claude' / 'CLAUDE.md').exists():
            recommendations.append({
                'type': 'missing_file',
                'priority': 'high',
                'message': '建議添加 CLAUDE.md 配置文件以優化 AI 助手體驗'
            })
        
        # 檢查 README
        if not (self.project_path / 'README.md').exists():
            recommendations.append({
                'type': 'missing_file',
                'priority': 'high',
                'message': '建議添加 README.md 文件說明專案'
            })
        
        # 檢查測試
        if self.analysis_results['metrics']['test_files'] == 0:
            recommendations.append({
                'type': 'no_tests',
                'priority': 'medium',
                'message': '未發現測試文件，建議添加單元測試'
            })
        
        # 檢查 Git
        if not (self.project_path / '.git').exists():
            recommendations.append({
                'type': 'no_git',
                'priority': 'medium',
                'message': '建議初始化 Git 版本控制'
            })
        
        # 檢查依賴管理
        if 'Python' in self.analysis_results['languages'] and not (self.project_path / 'requirements.txt').exists():
            recommendations.append({
                'type': 'missing_deps',
                'priority': 'high',
                'message': '建議添加 requirements.txt 管理 Python 依賴'
            })
        
        self.analysis_results['recommendations'] = recommendations
        for rec in recommendations:
            priority_color = Colors.RED if rec['priority'] == 'high' else Colors.YELLOW
            print(f"  {priority_color}•{Colors.ENDC} {rec['message']}")

def generate_claude_config(analysis_results, output_path):
    """生成 CLAUDE.md 配置文件"""
    print(f"\n{Colors.CYAN}生成 CLAUDE.md 配置...{Colors.ENDC}")
    
    config_content = f"""# {analysis_results['project_name']} - AI 配置文件

此文件由專案分析工具自動生成
生成時間：{analysis_results['analysis_date']}

## 專案概述
- **專案名稱**：{analysis_results['project_name']}
- **專案類型**：{analysis_results['project_type']}
- **主要語言**：{', '.join(analysis_results['languages'])}
- **使用框架**：{', '.join(analysis_results['frameworks']) if analysis_results['frameworks'] else '無'}

## 專案結構
- **總文件數**：{analysis_results['structure']['total_files']}
- **主要目錄**：{', '.join(analysis_results['structure']['directories'][:10])}

## 開發規範

### 代碼風格
<!-- 根據專案語言自定義 -->
{generate_code_style_section(analysis_results['languages'])}

### 測試要求
- 單元測試覆蓋率目標：80%
- 測試框架：{detect_test_framework(analysis_results)}

## AI 助手指南

### 主要任務
1. 協助開發新功能
2. 優化現有代碼
3. 編寫測試案例
4. 改善文檔

### 注意事項
{generate_notes_section(analysis_results)}

## SuperClaude v3 擴展
@EXTENSIONS.md
"""
    
    # 寫入文件
    claude_path = output_path / 'CLAUDE.md'
    with open(claude_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"  {Colors.GREEN}✓{Colors.ENDC} 已生成 {claude_path}")

def generate_code_style_section(languages):
    """生成代碼風格章節"""
    styles = []
    
    if 'Python' in languages:
        styles.append("- Python: 遵循 PEP 8")
    if 'JavaScript/TypeScript' in languages:
        styles.append("- JavaScript: 使用 ESLint + Prettier")
    if 'Dart/Flutter' in languages:
        styles.append("- Dart: 遵循 Dart Style Guide")
    
    return '\n'.join(styles) if styles else "- 請根據專案需求定義"

def detect_test_framework(analysis_results):
    """檢測測試框架"""
    if 'pytest' in str(analysis_results.get('frameworks', [])):
        return 'PyTest'
    elif 'jest' in str(analysis_results.get('dependencies', {})):
        return 'Jest'
    elif analysis_results['project_type'] == 'flutter-app':
        return 'Flutter Test'
    return '待定義'

def generate_notes_section(analysis_results):
    """生成注意事項"""
    notes = []
    
    for rec in analysis_results.get('recommendations', []):
        if rec['priority'] == 'high':
            notes.append(f"- {rec['message']}")
    
    return '\n'.join(notes) if notes else "- 無特殊注意事項"

def save_analysis_report(analysis_results, output_path):
    """保存分析報告"""
    print(f"\n{Colors.CYAN}保存分析報告...{Colors.ENDC}")
    
    # JSON 格式
    json_path = output_path / 'project-analysis.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    print(f"  {Colors.GREEN}✓{Colors.ENDC} JSON 報告：{json_path}")
    
    # Markdown 格式
    md_path = output_path / 'project-analysis.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"""# 專案分析報告

**專案名稱**：{analysis_results['project_name']}  
**分析時間**：{analysis_results['analysis_date']}

## 技術棧
- **語言**：{', '.join(analysis_results['languages'])}
- **框架**：{', '.join(analysis_results['frameworks'])}
- **類型**：{analysis_results['project_type']}

## 專案指標
- **代碼行數**：{analysis_results['metrics']['lines_of_code']:,}
- **文件總數**：{analysis_results['structure']['total_files']}
- **測試文件**：{analysis_results['metrics']['test_files']}
- **文檔文件**：{analysis_results['metrics']['documentation_files']}

## 建議事項
""")
        for rec in analysis_results['recommendations']:
            priority = '🔴' if rec['priority'] == 'high' else '🟡'
            f.write(f"- {priority} {rec['message']}\n")
    
    print(f"  {Colors.GREEN}✓{Colors.ENDC} Markdown 報告：{md_path}")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='專案分析與配置生成器')
    parser.add_argument('path', nargs='?', default='.', help='專案路徑')
    parser.add_argument('--output', help='輸出目錄（預設為專案根目錄）')
    parser.add_argument('--no-claude', action='store_true', help='不生成 CLAUDE.md')
    parser.add_argument('--no-report', action='store_true', help='不生成分析報告')
    parser.add_argument('--no-color', action='store_true', help='禁用彩色輸出')
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    # 顯示標題
    print(f"{Colors.BLUE}╔════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BLUE}║       專案分析與配置生成器 v1.0        ║{Colors.ENDC}")
    print(f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.ENDC}")
    
    # 確定專案路徑
    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"{Colors.RED}錯誤：專案路徑不存在: {project_path}{Colors.ENDC}")
        sys.exit(1)
    
    # 確定輸出路徑
    output_path = Path(args.output) if args.output else project_path
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 執行分析
    analyzer = ProjectAnalyzer(project_path)
    results = analyzer.analyze()
    
    # 生成配置和報告
    if not args.no_claude:
        generate_claude_config(results, output_path)
    
    if not args.no_report:
        save_analysis_report(results, output_path)
    
    # 完成
    print(f"\n{Colors.GREEN}✅ 分析完成！{Colors.ENDC}")
    
    if results['recommendations']:
        print(f"\n{Colors.YELLOW}建議執行 init-project.py 來配置專案模板系統。{Colors.ENDC}")

if __name__ == '__main__':
    main()