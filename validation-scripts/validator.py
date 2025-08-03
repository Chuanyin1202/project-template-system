#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Validation Framework - 專案驗證框架
統一的跨平台專案品質檢查工具
"""

import os
import sys
import re
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
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

class ValidationResult:
    """驗證結果類"""
    def __init__(self, check_name: str):
        self.check_name = check_name
        self.passed = True
        self.warnings = []
        self.errors = []
        self.info = []
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.passed = False
    
    def add_info(self, message: str):
        self.info.append(message)
    
    def __str__(self):
        status = f"{Colors.GREEN}✓ 通過{Colors.ENDC}" if self.passed else f"{Colors.RED}✗ 失敗{Colors.ENDC}"
        return f"{self.check_name}: {status}"

class ProjectValidator:
    """專案驗證器基類"""
    
    def __init__(self, project_root: Path, config: Dict = None):
        self.project_root = project_root
        self.config = config or {}
        self.results = []
        
        # 從配置或自動檢測
        self.source_dir = self.config.get('source_dir', 'src')
        self.file_extensions = self.config.get('file_extensions', ['.py', '.js', '.ts', '.dart'])
        self.project_type = self.config.get('project_type', self._detect_project_type())
        self.primary_language = self.config.get('primary_language', self._detect_primary_language())
    
    def _detect_project_type(self) -> str:
        """自動檢測專案類型"""
        if (self.project_root / 'pubspec.yaml').exists():
            return 'flutter'
        elif (self.project_root / 'package.json').exists():
            return 'javascript'
        elif (self.project_root / 'requirements.txt').exists():
            return 'python'
        elif (self.project_root / 'go.mod').exists():
            return 'go'
        return 'generic'
    
    def _detect_primary_language(self) -> str:
        """自動檢測主要語言"""
        lang_map = {
            'flutter': 'dart',
            'javascript': 'javascript',
            'python': 'python',
            'go': 'go'
        }
        return lang_map.get(self.project_type, 'unknown')
    
    def get_source_files(self) -> List[Path]:
        """獲取所有源代碼文件"""
        source_path = self.project_root / self.source_dir
        if not source_path.exists():
            return []
        
        files = []
        for ext in self.file_extensions:
            files.extend(source_path.rglob(f'*{ext}'))
        return files
    
    def run_all_checks(self) -> List[ValidationResult]:
        """運行所有檢查（子類實現）"""
        raise NotImplementedError
    
    def print_summary(self):
        """打印結果摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"\n{Colors.BLUE}╔════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}║              檢查結果摘要              ║{Colors.ENDC}")
        print(f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.ENDC}")
        print(f"\n總檢查項目: {total}")
        print(f"{Colors.GREEN}通過: {passed}{Colors.ENDC}")
        print(f"{Colors.RED}失敗: {failed}{Colors.ENDC}")
        
        # 計算通過率
        pass_rate = (passed * 100 // total) if total > 0 else 0
        print(f"\n通過率: ", end='')
        if pass_rate >= 90:
            print(f"{Colors.GREEN}{pass_rate}%{Colors.ENDC} 🎉")
        elif pass_rate >= 70:
            print(f"{Colors.YELLOW}{pass_rate}%{Colors.ENDC} ⚠️")
        else:
            print(f"{Colors.RED}{pass_rate}%{Colors.ENDC} ❌")
        
        # 詳細結果
        if failed > 0:
            print(f"\n{Colors.RED}失敗項目詳情：{Colors.ENDC}")
            for result in self.results:
                if not result.passed:
                    print(f"\n{Colors.YELLOW}{result.check_name}:{Colors.ENDC}")
                    for error in result.errors:
                        print(f"  {Colors.RED}✗{Colors.ENDC} {error}")
                    for warning in result.warnings:
                        print(f"  {Colors.YELLOW}⚠{Colors.ENDC} {warning}")

class CodeQualityValidator(ProjectValidator):
    """代碼品質驗證器"""
    
    def run_all_checks(self) -> List[ValidationResult]:
        """運行所有代碼品質檢查"""
        self.results = []
        
        # 各項檢查
        self.results.append(self.check_file_size())
        self.results.append(self.check_line_length())
        self.results.append(self.check_function_length())
        self.results.append(self.check_complexity())
        self.results.append(self.check_naming_conventions())
        self.results.append(self.check_imports())
        
        return self.results
    
    def check_file_size(self) -> ValidationResult:
        """檢查文件大小"""
        result = ValidationResult("檔案大小檢查")
        max_lines = self.config.get('max_file_lines', 500)
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    if lines > max_lines:
                        result.add_error(f"{file_path.relative_to(self.project_root)}: {lines} 行 (超過限制 {max_lines})")
            except Exception as e:
                result.add_warning(f"無法讀取 {file_path}: {e}")
        
        return result
    
    def check_line_length(self) -> ValidationResult:
        """檢查行長度"""
        result = ValidationResult("行長度檢查")
        max_length = self.config.get('max_line_length', 120)
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if len(line.rstrip()) > max_length:
                            result.add_warning(
                                f"{file_path.relative_to(self.project_root)}:{i} "
                                f"行長度 {len(line.rstrip())} (建議不超過 {max_length})"
                            )
            except Exception as e:
                result.add_warning(f"無法讀取 {file_path}: {e}")
        
        return result
    
    def check_function_length(self) -> ValidationResult:
        """檢查函數長度"""
        result = ValidationResult("函數長度檢查")
        max_lines = self.config.get('max_function_lines', 50)
        
        patterns = {
            'python': r'^\s*def\s+\w+',
            'javascript': r'^\s*(function\s+\w+|const\s+\w+\s*=\s*\()',
            'dart': r'^\s*\w+\s+\w+\s*\(',
        }
        
        pattern = patterns.get(self.primary_language)
        if not pattern:
            result.add_info("跳過：不支援的語言")
            return result
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    in_function = False
                    function_start = 0
                    function_name = ""
                    indent_level = 0
                    
                    for i, line in enumerate(lines):
                        if re.match(pattern, line):
                            in_function = True
                            function_start = i
                            function_name = line.strip()
                            indent_level = len(line) - len(line.lstrip())
                        elif in_function and line.strip() and len(line) - len(line.lstrip()) <= indent_level:
                            function_length = i - function_start
                            if function_length > max_lines:
                                result.add_error(
                                    f"{file_path.relative_to(self.project_root)}:{function_start+1} "
                                    f"函數 '{function_name[:30]}...' 長度 {function_length} 行 (超過限制 {max_lines})"
                                )
                            in_function = False
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result
    
    def check_complexity(self) -> ValidationResult:
        """檢查代碼複雜度"""
        result = ValidationResult("代碼複雜度檢查")
        max_complexity = self.config.get('max_complexity', 10)
        
        # 簡單的複雜度檢查：計算條件語句數量
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'switch']
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 簡單統計複雜度關鍵字
                    complexity = sum(1 for keyword in complexity_keywords 
                                   if f' {keyword} ' in content or f'\n{keyword} ' in content)
                    
                    if complexity > max_complexity * 3:  # 檔案級別的粗略估計
                        result.add_warning(
                            f"{file_path.relative_to(self.project_root)} "
                            f"可能過於複雜 (複雜度指標: {complexity})"
                        )
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result
    
    def check_naming_conventions(self) -> ValidationResult:
        """檢查命名規範"""
        result = ValidationResult("命名規範檢查")
        
        # 各語言的命名規範
        conventions = {
            'python': {
                'file': r'^[a-z_]+\.py$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'function': r'^[a-z_][a-z0-9_]*$',
            },
            'javascript': {
                'file': r'^[a-zA-Z][a-zA-Z0-9]*\.(js|ts)$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'function': r'^[a-z][a-zA-Z0-9]*$',
            },
            'dart': {
                'file': r'^[a-z_]+\.dart$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'function': r'^[a-z][a-zA-Z0-9]*$',
            }
        }
        
        convention = conventions.get(self.primary_language, {})
        if not convention:
            result.add_info("跳過：不支援的語言")
            return result
        
        # 檢查文件命名
        for file_path in self.get_source_files():
            filename = file_path.name
            if 'file' in convention and not re.match(convention['file'], filename):
                result.add_warning(f"檔案命名不符合規範: {filename}")
        
        return result
    
    def check_imports(self) -> ValidationResult:
        """檢查導入語句"""
        result = ValidationResult("導入檢查")
        
        # 檢查重複和未使用的導入
        import_patterns = {
            'python': r'^(import\s+\S+|from\s+\S+\s+import)',
            'javascript': r'^(import\s+.*from|const\s+.*=\s*require)',
            'dart': r'^import\s+',
        }
        
        pattern = import_patterns.get(self.primary_language)
        if not pattern:
            result.add_info("跳過：不支援的語言")
            return result
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    imports = []
                    
                    for line in lines:
                        if re.match(pattern, line):
                            imports.append(line.strip())
                    
                    # 檢查重複導入
                    if len(imports) != len(set(imports)):
                        result.add_warning(f"{file_path.relative_to(self.project_root)} 有重複的導入語句")
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result

class SecurityValidator(ProjectValidator):
    """安全性驗證器"""
    
    def run_all_checks(self) -> List[ValidationResult]:
        """運行所有安全檢查"""
        self.results = []
        
        self.results.append(self.check_hardcoded_secrets())
        self.results.append(self.check_sql_injection())
        self.results.append(self.check_unsafe_functions())
        self.results.append(self.check_file_permissions())
        
        return self.results
    
    def check_hardcoded_secrets(self) -> ValidationResult:
        """檢查硬編碼的敏感資訊"""
        result = ValidationResult("敏感資訊檢查")
        
        # 敏感資訊模式
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', '硬編碼的密碼'),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', '硬編碼的 API 金鑰'),
            (r'secret[_-]?key\s*=\s*["\'][^"\']+["\']', '硬編碼的密鑰'),
            (r'token\s*=\s*["\'][^"\']+["\']', '硬編碼的 Token'),
        ]
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern, desc in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            # 排除環境變數引用
                            if not re.search(r'(process\.env|os\.environ|getenv)', content):
                                result.add_error(f"{file_path.relative_to(self.project_root)}: 發現{desc}")
            except Exception as e:
                result.add_warning(f"無法檢查 {file_path}: {e}")
        
        return result
    
    def check_sql_injection(self) -> ValidationResult:
        """檢查 SQL 注入風險"""
        result = ValidationResult("SQL 注入檢查")
        
        # SQL 注入風險模式
        sql_patterns = [
            r'query.*\+.*["\']',  # 字串拼接
            r'execute.*\+.*["\']',
            r'f["\'].*SELECT.*{',  # Python f-string
            r'\$.*SELECT.*\$',  # 模板字串
        ]
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in sql_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            result.add_warning(f"{file_path.relative_to(self.project_root)}: 可能的 SQL 注入風險")
            except Exception as e:
                result.add_warning(f"無法檢查 {file_path}: {e}")
        
        return result
    
    def check_unsafe_functions(self) -> ValidationResult:
        """檢查不安全的函數使用"""
        result = ValidationResult("不安全函數檢查")
        
        # 各語言的不安全函數
        unsafe_functions = {
            'python': ['eval', 'exec', 'compile', '__import__'],
            'javascript': ['eval', 'Function', 'setTimeout.*["\']', 'setInterval.*["\']'],
        }
        
        functions = unsafe_functions.get(self.primary_language, [])
        if not functions:
            result.add_info("跳過：不支援的語言")
            return result
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for func in functions:
                        if re.search(rf'\b{func}\s*\(', content):
                            result.add_warning(
                                f"{file_path.relative_to(self.project_root)}: "
                                f"使用了不安全的函數 '{func}'"
                            )
            except Exception as e:
                result.add_warning(f"無法檢查 {file_path}: {e}")
        
        return result
    
    def check_file_permissions(self) -> ValidationResult:
        """檢查文件權限"""
        result = ValidationResult("文件權限檢查")
        
        if platform.system() == 'Windows':
            result.add_info("跳過：Windows 系統")
            return result
        
        for file_path in self.get_source_files():
            try:
                # 檢查是否有過寬的權限
                mode = file_path.stat().st_mode
                if mode & 0o022:  # 其他用戶可寫
                    result.add_warning(f"{file_path.relative_to(self.project_root)}: 文件權限過寬")
            except Exception as e:
                result.add_warning(f"無法檢查 {file_path}: {e}")
        
        return result

class DuplicationValidator(ProjectValidator):
    """重複代碼驗證器"""
    
    def run_all_checks(self) -> List[ValidationResult]:
        """運行重複代碼檢查"""
        self.results = []
        
        self.results.append(self.check_duplicate_functions())
        self.results.append(self.check_duplicate_imports())
        self.results.append(self.check_similar_files())
        
        return self.results
    
    def check_duplicate_functions(self) -> ValidationResult:
        """檢查重複的函數定義"""
        result = ValidationResult("重複函數檢查")
        
        function_patterns = {
            'python': r'def\s+(\w+)\s*\(',
            'javascript': r'function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*\(',
            'dart': r'(\w+)\s+(\w+)\s*\(',
        }
        
        pattern = function_patterns.get(self.primary_language)
        if not pattern:
            result.add_info("跳過：不支援的語言")
            return result
        
        all_functions = {}
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(pattern, content)
                    for match in matches:
                        func_name = match if isinstance(match, str) else next(m for m in match if m)
                        if func_name in all_functions:
                            result.add_warning(
                                f"函數 '{func_name}' 在多個文件中定義: "
                                f"{all_functions[func_name]} 和 {file_path.relative_to(self.project_root)}"
                            )
                        else:
                            all_functions[func_name] = file_path.relative_to(self.project_root)
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result
    
    def check_duplicate_imports(self) -> ValidationResult:
        """檢查重複的導入語句"""
        result = ValidationResult("重複導入檢查")
        
        import_patterns = {
            'python': r'^(import\s+(\S+)|from\s+(\S+)\s+import)',
            'javascript': r'^import\s+.*from\s+["\']([^"\']+)["\']',
            'dart': r'^import\s+["\']([^"\']+)["\']',
        }
        
        pattern = import_patterns.get(self.primary_language)
        if not pattern:
            result.add_info("跳過：不支援的語言")
            return result
        
        for file_path in self.get_source_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    imports = []
                    
                    for i, line in enumerate(lines):
                        match = re.match(pattern, line)
                        if match:
                            import_stmt = line.strip()
                            if import_stmt in imports:
                                result.add_warning(
                                    f"{file_path.relative_to(self.project_root)}:{i+1} "
                                    f"重複的導入語句"
                                )
                            imports.append(import_stmt)
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result
    
    def check_similar_files(self) -> ValidationResult:
        """檢查相似的文件"""
        result = ValidationResult("相似文件檢查")
        
        # 簡單的相似度檢查：比較文件大小和行數
        file_info = {}
        for file_path in self.get_source_files():
            try:
                size = file_path.stat().st_size
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                key = (size, lines)
                if key in file_info:
                    result.add_warning(
                        f"文件可能相似: {file_info[key]} 和 "
                        f"{file_path.relative_to(self.project_root)} "
                        f"(相同大小和行數)"
                    )
                else:
                    file_info[key] = file_path.relative_to(self.project_root)
            except Exception as e:
                result.add_warning(f"無法分析 {file_path}: {e}")
        
        return result

class AllValidator(ProjectValidator):
    """綜合驗證器"""
    
    def __init__(self, project_root: Path, config: Dict = None):
        super().__init__(project_root, config)
        self.validators = [
            CodeQualityValidator(project_root, config),
            SecurityValidator(project_root, config),
            DuplicationValidator(project_root, config),
        ]
    
    def run_all_checks(self) -> List[ValidationResult]:
        """運行所有驗證器的檢查"""
        self.results = []
        
        for validator in self.validators:
            print(f"\n{Colors.BLUE}運行 {validator.__class__.__name__}...{Colors.ENDC}")
            results = validator.run_all_checks()
            self.results.extend(results)
            
            # 顯示每個驗證器的結果
            for result in results:
                print(f"  {result}")
        
        return self.results

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='專案品質驗證工具')
    parser.add_argument('path', nargs='?', default='.', help='專案路徑')
    parser.add_argument('--check', choices=['all', 'quality', 'security', 'duplication'], 
                       default='all', help='檢查類型')
    parser.add_argument('--config', help='配置文件路徑')
    parser.add_argument('--source-dir', help='源代碼目錄')
    parser.add_argument('--no-color', action='store_true', help='禁用彩色輸出')
    parser.add_argument('--output', choices=['console', 'json', 'markdown'], 
                       default='console', help='輸出格式')
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    # 載入配置
    config = {}
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"{Colors.RED}無法載入配置文件: {e}{Colors.ENDC}")
    
    if args.source_dir:
        config['source_dir'] = args.source_dir
    
    # 確定專案路徑
    project_root = Path(args.path).resolve()
    if not project_root.exists():
        print(f"{Colors.RED}錯誤：專案路徑不存在: {project_root}{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.BLUE}╔════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BLUE}║         專案品質驗證工具 v1.0          ║{Colors.ENDC}")
    print(f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.ENDC}")
    print(f"\n專案路徑: {project_root}")
    
    # 選擇驗證器
    if args.check == 'quality':
        validator = CodeQualityValidator(project_root, config)
    elif args.check == 'security':
        validator = SecurityValidator(project_root, config)
    elif args.check == 'duplication':
        validator = DuplicationValidator(project_root, config)
    else:
        validator = AllValidator(project_root, config)
    
    # 運行檢查
    print(f"檢查類型: {args.check}")
    print(f"專案類型: {validator.project_type}")
    print(f"主要語言: {validator.primary_language}")
    
    results = validator.run_all_checks()
    
    # 輸出結果
    if args.output == 'json':
        # JSON 輸出
        output = {
            'project': str(project_root),
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(results),
                'passed': sum(1 for r in results if r.passed),
                'failed': sum(1 for r in results if not r.passed)
            },
            'results': [
                {
                    'check': r.check_name,
                    'passed': r.passed,
                    'errors': r.errors,
                    'warnings': r.warnings,
                    'info': r.info
                }
                for r in results
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.output == 'markdown':
        # Markdown 輸出
        print(f"\n# 專案品質驗證報告")
        print(f"\n**專案**: {project_root}")
        print(f"**時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n## 摘要")
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        print(f"- 總檢查項目: {total}")
        print(f"- 通過: {passed}")
        print(f"- 失敗: {total - passed}")
        print(f"\n## 詳細結果")
        for result in results:
            status = "✅" if result.passed else "❌"
            print(f"\n### {status} {result.check_name}")
            if result.errors:
                print("\n**錯誤:**")
                for error in result.errors:
                    print(f"- {error}")
            if result.warnings:
                print("\n**警告:**")
                for warning in result.warnings:
                    print(f"- {warning}")
    else:
        # 控制台輸出
        validator.print_summary()
    
    # 返回狀態碼
    if all(r.passed for r in results):
        print(f"\n{Colors.GREEN}✅ 所有檢查通過！{Colors.ENDC}")
        sys.exit(0)
    else:
        failed_count = sum(1 for r in results if not r.passed)
        print(f"\n{Colors.RED}❌ 有 {failed_count} 項檢查失敗，請修復後再試。{Colors.ENDC}")
        sys.exit(1)

if __name__ == '__main__':
    main()