#!/usr/bin/env python3
import os
import ast
import json
import subprocess
import sys
from pathlib import Path

def audit_syntax_errors():
    """Find ALL syntax errors in Python files"""
    print("=== SYNTAX ERRORS ===")
    errors = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        ast.parse(f.read(), filename=path)
                except SyntaxError as e:
                    errors.append(f"{path}:{e.lineno}: {e.msg}")
                except Exception as e:
                    errors.append(f"{path}: Parse error - {e}")
    
    for error in errors:
        print(f"SYNTAX ERROR: {error}")
    return len(errors)

def audit_import_errors():
    """Find ALL import errors and missing modules"""
    print("\n=== IMPORT ERRORS ===")
    errors = []
    missing_modules = set()
    
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        tree = ast.parse(f.read())
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                try:
                                    __import__(alias.name.split('.')[0])
                                except ImportError:
                                    missing_modules.add(alias.name)
                                    errors.append(f"{path}: Missing import {alias.name}")
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                try:
                                    __import__(node.module.split('.')[0])
                                except ImportError:
                                    missing_modules.add(node.module)
                                    errors.append(f"{path}: Missing module {node.module}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    for error in errors[:50]:  # Limit output
        print(f"IMPORT ERROR: {error}")
    
    print(f"\nMISSING MODULES: {sorted(missing_modules)}")
    return len(errors)

def audit_configuration_conflicts():
    """Find conflicting configurations"""
    print("\n=== CONFIGURATION CONFLICTS ===")
    
    # Find all config files
    configs = {
        'requirements': list(Path('.').rglob('requirements*.txt')),
        'docker_compose': list(Path('.').rglob('docker-compose*.yml')),
        'dockerfiles': list(Path('.').rglob('Dockerfile*')),
        'env_files': list(Path('.').rglob('.env*')),
        'main_files': list(Path('.').rglob('main.py')) + list(Path('.').rglob('app.py')),
        'setup_files': list(Path('.').rglob('setup.py')) + list(Path('.').rglob('pyproject.toml'))
    }
    
    conflicts = 0
    for config_type, files in configs.items():
        if len(files) > 1:
            print(f"CONFLICT: Multiple {config_type} files:")
            for f in files:
                print(f"  - {f}")
            conflicts += len(files) - 1
    
    return conflicts

def audit_database_issues():
    """Find database configuration problems"""
    print("\n=== DATABASE ISSUES ===")
    issues = []
    
    # Check for multiple database configs
    db_files = list(Path('.').rglob('*database*')) + list(Path('.').rglob('*db*'))
    db_files = [f for f in db_files if f.is_file() and f.suffix == '.py']
    
    for db_file in db_files:
        try:
            with open(db_file, 'r') as f:
                content = f.read()
                if 'sqlite' in content.lower() and 'postgresql' in content.lower():
                    issues.append(f"Mixed DB types in {db_file}")
                if 'password' in content.lower() and 'changeme' in content.lower():
                    issues.append(f"Default password in {db_file}")
        except Exception as e:
            print(f"Error processing {db_file}: {e}")
    
    for issue in issues:
        print(f"DB ISSUE: {issue}")
    
    return len(issues)

def audit_security_gaps():
    """Find remaining security issues"""
    print("\n=== SECURITY GAPS ===")
    issues = []
    
    # Check for hardcoded secrets
    secret_patterns = ['password', 'secret', 'key', 'token']
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith(('.py', '.yml', '.yaml', '.json')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        for pattern in secret_patterns:
                            if f'{pattern}=' in content or f'{pattern}:' in content:
                                if 'changeme' in content or 'your_' in content or 'placeholder' in content:
                                    issues.append(f"Hardcoded {pattern} in {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    for issue in issues[:20]:
        print(f"SECURITY GAP: {issue}")
    
    return len(issues)

def audit_runtime_errors():
    """Check for potential runtime errors"""
    print("\n=== POTENTIAL RUNTIME ERRORS ===")
    issues = []
    
    # Check for undefined variables, missing attributes, etc.
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Look for common runtime error patterns
                        if '.get(' not in content and '[' in content and ']' in content:
                            issues.append(f"Potential KeyError in {path}")
                        if 'None.' in content:
                            issues.append(f"Potential AttributeError in {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    for issue in issues[:10]:
        print(f"RUNTIME RISK: {issue}")
    
    return len(issues)

def main():
    print("COMPREHENSIVE CODEBASE AUDIT")
    print("=" * 50)
    
    total_issues = 0
    total_issues += audit_syntax_errors()
    total_issues += audit_import_errors()
    total_issues += audit_configuration_conflicts()
    total_issues += audit_database_issues()
    total_issues += audit_security_gaps()
    total_issues += audit_runtime_errors()
    
    print(f"\n=== SUMMARY ===")
    print(f"TOTAL ISSUES FOUND: {total_issues}")
    print(f"CODEBASE STATUS: {'BROKEN' if total_issues > 50 else 'NEEDS WORK' if total_issues > 10 else 'OK'}")

if __name__ == "__main__":
    main()
