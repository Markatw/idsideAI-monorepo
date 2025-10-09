import os
import ast
import re
from collections import defaultdict

def extract_imports_from_file(file_path):
    """Extract import statements from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return imports

def get_requirements_from_file(req_file):
    """Extract package names from requirements.txt file."""
    packages = set()
    try:
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before ==, >=, etc.)
                    package = re.split(r'[=<>!]', line)[0].strip()
                    packages.add(package.lower())
    except FileNotFoundError:
        print(f"Requirements file not found: {req_file}")
    except Exception as e:
        print(f"Error reading {req_file}: {e}")
    
    return packages

def scan_imports():
    """Scan all Python files for imports."""
    all_imports = set()
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = extract_imports_from_file(file_path)
                all_imports.update(imports)
    
    return all_imports

def main():
    print("Scanning Python imports...")
    imports = scan_imports()
    
    print("Reading requirements files...")
    main_req = get_requirements_from_file('requirements.txt')
    backend_req = get_requirements_from_file('backend/requirements.txt')
    
    all_requirements = main_req.union(backend_req)
    
    # Standard library modules (partial list)
    stdlib_modules = {
        'os', 'sys', 'time', 'datetime', 'json', 'urllib', 'http', 'collections',
        'itertools', 'functools', 'operator', 're', 'math', 'random', 'string',
        'pathlib', 'typing', 'asyncio', 'concurrent', 'threading', 'multiprocessing',
        'logging', 'warnings', 'traceback', 'inspect', 'copy', 'pickle', 'base64',
        'hashlib', 'hmac', 'secrets', 'uuid', 'enum', 'dataclasses', 'abc',
        'contextlib', 'weakref', 'gc', 'ast', 'py_compile'
    }
    
    # Filter out standard library and local imports
    third_party_imports = {imp for imp in imports 
                          if imp not in stdlib_modules 
                          and not imp.startswith('.')
                          and not imp in ['app', 'backend', 'idsideai', 'Sprint26']}
    
    missing_deps = third_party_imports - all_requirements
    
    print(f"\nFound {len(imports)} total imports")
    print(f"Found {len(third_party_imports)} third-party imports")
    print(f"Found {len(all_requirements)} declared dependencies")
    
    if missing_deps:
        print(f"\nMissing dependencies ({len(missing_deps)}):")
        for dep in sorted(missing_deps):
            print(f"  - {dep}")
    else:
        print("\nNo missing dependencies found!")
    
    # Check for duplicate requirements
    print(f"\nChecking for duplicate requirements...")
    with open('backend/requirements.txt', 'r') as f:
        backend_lines = f.readlines()
    
    seen_packages = {}
    duplicates = []
    for i, line in enumerate(backend_lines):
        line = line.strip()
        if line and not line.startswith('#'):
            package = re.split(r'[=<>!]', line)[0].strip().lower()
            if package in seen_packages:
                duplicates.append((package, seen_packages[package], i+1))
            else:
                seen_packages[package] = i+1
    
    if duplicates:
        print("Found duplicate packages in backend/requirements.txt:")
        for package, first_line, second_line in duplicates:
            print(f"  - {package}: lines {first_line} and {second_line}")

if __name__ == "__main__":
    main()
