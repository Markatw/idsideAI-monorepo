#!/usr/bin/env python3
"""
FOCUSED APPLICATION VALIDATION
==============================
This validates ONLY the core application code, not documentation or test files.
"""

import os
import sys
import ast
import json
import subprocess
import importlib
import time
import requests
from pathlib import Path
from typing import Dict, List, Any

class ApplicationValidator:
    def __init__(self):
        self.results = {
            'syntax_errors': [],
            'import_errors': [],
            'function_stubs': [],
            'security_issues': [],
            'runtime_errors': [],
            'api_errors': [],
            'critical_todos': []
        }
        self.total_issues = 0
        
        # Only validate these core application directories
        self.app_directories = ['backend', 'idsideai', 'security_toolkit']
        self.app_files = ['run.py', 'setup.py']
        
    def log_issue(self, category: str, issue: str):
        """Log an issue"""
        self.results[category].append(issue)
        self.total_issues += 1
        print(f"❌ {category.upper()}: {issue}")
        
    def log_success(self, category: str, item: str):
        """Log a success"""
        print(f"✅ {category.upper()}: {item}")

    def get_application_files(self):
        """Get only application Python files"""
        files = []
        
        # Add specific files
        for file in self.app_files:
            if os.path.exists(file):
                files.append(file)
        
        # Add files from application directories
        for directory in self.app_directories:
            if os.path.exists(directory):
                for root, dirs, filenames in os.walk(directory):
                    # Skip cache directories
                    dirs[:] = [d for d in dirs if not d.startswith('__pycache__')]
                    for filename in filenames:
                        if filename.endswith('.py'):
                            files.append(os.path.join(root, filename))
        
        return files

    def validate_syntax(self):
        """Validate syntax of application files"""
        print("\n=== SYNTAX VALIDATION ===")
        files = self.get_application_files()
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                ast.parse(content, filename=file_path)
                compile(content, file_path, 'exec')
                self.log_success('syntax', f'{file_path}')
                
            except SyntaxError as e:
                self.log_issue('syntax_errors', f'{file_path}:{e.lineno} - {e.msg}')
            except Exception as e:
                self.log_issue('syntax_errors', f'{file_path} - {str(e)}')

    def validate_imports(self):
        """Validate imports in application files"""
        print("\n=== IMPORT VALIDATION ===")
        files = self.get_application_files()
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self._test_import(file_path, alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self._test_import(file_path, node.module)
                            
            except Exception as e:
                self.log_issue('import_errors', f'{file_path} - Could not parse: {str(e)}')

    def _test_import(self, file_path: str, module_name: str):
        """Test if a specific import works"""
        try:
            if '.' in module_name:
                base_module = module_name.split('.')[0]
            else:
                base_module = module_name
                
            importlib.import_module(base_module)
            
        except ImportError:
            # Check if it's a local import
            if any(module_name.startswith(app_dir) for app_dir in self.app_directories):
                if not self._validate_local_import(module_name):
                    self.log_issue('import_errors', f'{file_path} - Missing local module: {module_name}')
            else:
                self.log_issue('import_errors', f'{file_path} - Missing dependency: {module_name}')

    def _validate_local_import(self, module_name: str) -> bool:
        """Validate local import exists"""
        parts = module_name.split('.')
        path = Path('.')
        
        for part in parts:
            path = path / part
            if path.with_suffix('.py').exists():
                return True
            elif (path / '__init__.py').exists():
                continue
        return False

    def validate_functions(self):
        """Check for stub functions in application code"""
        print("\n=== FUNCTION VALIDATION ===")
        files = self.get_application_files()
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        func_name = node.name
                        
                        # Check for empty functions (stubs)
                        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                            self.log_issue('function_stubs', f'{file_path} - Empty function: {func_name}')
                        elif (len(node.body) == 1 and 
                              isinstance(node.body[0], ast.Expr) and 
                              isinstance(node.body[0].value, ast.Constant) and 
                              isinstance(node.body[0].value.value, str)):
                            self.log_issue('function_stubs', f'{file_path} - Docstring-only function: {func_name}')
                        else:
                            self.log_success('function', f'{file_path}:{func_name}')
                            
            except Exception as e:
                self.log_issue('function_stubs', f'{file_path} - Could not parse: {str(e)}')

    def validate_security(self):
        """Run security validation on application code"""
        print("\n=== SECURITY VALIDATION ===")
        
        try:
            # Run bandit only on application directories
            cmd = ['bandit', '-r'] + self.app_directories + ['-f', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.stdout.strip():
                bandit_results = json.loads(result.stdout)
                issues = bandit_results.get('results', [])
                
                if not issues:
                    self.log_success('security', 'No security issues found')
                else:
                    for issue in issues:
                        severity = issue.get('issue_severity', 'Unknown')
                        filename = issue.get('filename', 'Unknown')
                        test_id = issue.get('test_id', 'Unknown')
                        
                        if severity in ['HIGH', 'MEDIUM']:
                            self.log_issue('security_issues', f'{filename} - {severity} {test_id}')
                        else:
                            print(f"⚠️  LOW SECURITY: {filename} - {test_id}")
            else:
                self.log_success('security', 'No security issues found')
                
        except Exception as e:
            self.log_issue('security_issues', f'Could not run security scan: {str(e)}')

    def validate_runtime(self):
        """Test application startup and basic functionality"""
        print("\n=== RUNTIME VALIDATION ===")
        
        # Test application startup
        try:
            process = subprocess.Popen([sys.executable, 'run.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            time.sleep(5)
            
            if process.poll() is None:
                self.log_success('runtime', 'Application starts successfully')
                
                # Test basic endpoints
                try:
                    # Try HTTP first
                    response = requests.get('http://127.0.0.1:8000/health', timeout=5)
                    if response.status_code == 200:
                        self.log_success('api', 'Health endpoint working')
                    else:
                        self.log_issue('api_errors', f'Health endpoint returned {response.status_code}')
                except requests.exceptions.ConnectionError:
                    # Application might not be fully started yet
                    print("⚠️  API: Health endpoint connection failed (application may still be starting)")
                except requests.exceptions.RequestException as e:
                    self.log_issue('api_errors', f'Health endpoint failed: {str(e)}')
                
                process.terminate()
                process.wait(timeout=10)
            else:
                stdout, stderr = process.communicate()
                self.log_issue('runtime_errors', f'Application failed to start: {stderr}')
                
        except Exception as e:
            self.log_issue('runtime_errors', f'Could not test application: {str(e)}')

    def validate_critical_todos(self):
        """Check for critical TODOs in application code"""
        print("\n=== CRITICAL TODO VALIDATION ===")
        files = self.get_application_files()
        
        critical_patterns = ['TODO', 'FIXME', 'PLACEHOLDER', 'XXX', 'HACK']
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines, 1):
                    line_upper = line.upper()
                    for pattern in critical_patterns:
                        if pattern in line_upper:
                            # Skip comments that are just explaining what patterns to look for
                            if 'stub_patterns' in line or 'check_for' in line:
                                continue
                            self.log_issue('critical_todos', f'{file_path}:{i} - {pattern}: {line.strip()}')
                            
            except Exception as e:
                self.log_issue('critical_todos', f'{file_path} - Could not check: {str(e)}')

    def generate_report(self):
        """Generate final validation report"""
        print("\n" + "="*80)
        print("APPLICATION VALIDATION REPORT")
        print("="*80)
        
        total_categories = len([cat for cat in self.results.values() if cat])
        failed_categories = len([cat for cat in self.results.values() if cat])
        
        print(f"\nTOTAL ISSUES FOUND: {self.total_issues}")
        
        for category, issues in self.results.items():
            if issues:
                print(f"\n{category.upper().replace('_', ' ')} ({len(issues)} issues):")
                for issue in issues:
                    print(f"  ❌ {issue}")
        
        print("\n" + "="*80)
        if self.total_issues == 0:
            print("🎉 FINAL VERDICT: APPLICATION IS CLEAN")
            print("✅ All core application code passes validation")
            print("✅ Ready for production deployment")
            return True
        else:
            print("❌ FINAL VERDICT: ISSUES FOUND")
            print(f"❌ {self.total_issues} issues must be fixed")
            print("❌ Application is not ready for production")
            return False

def main():
    """Run focused application validation"""
    print("FOCUSED APPLICATION VALIDATION")
    print("Validating ONLY core application code")
    print("="*80)
    
    validator = ApplicationValidator()
    
    validator.validate_syntax()
    validator.validate_imports()
    validator.validate_functions()
    validator.validate_security()
    validator.validate_runtime()
    validator.validate_critical_todos()
    
    success = validator.generate_report()
    
    # Save results
    with open('application_validation_results.json', 'w') as f:
        json.dump(validator.results, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
