import os
import ast

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                try:
                    ast.parse(f.read(), filename=path)
                except SyntaxError as e:
                    print(f'Syntax error in {path}: {e}')
