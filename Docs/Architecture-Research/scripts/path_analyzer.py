import os
import glob
import re

search_dir = "d:\\AI-Student Platform"
exclude_dirs = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'instance', 'static', 'templates'}

patterns = [
    r'os\.path\.abspath\([^\)]+\)',
    r'open\([\'"][^\'"]+[\'"]',
    r'sqlite:///[^\'"]+',
    r'os\.environ\.get\([\'"][^\'"]+[\'"]',
]

print("Path Analysis Results:")
for root, dirs, files in os.walk(search_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    lines = f.readlines()
                except UnicodeDecodeError:
                    continue
                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            print(f"{os.path.relpath(file_path, search_dir)}:{i+1} - {line.strip()}")
