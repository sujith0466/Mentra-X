import os
import re

FRONTEND_SRC = r"d:\AI-Student Platform\frontend\src"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content = re.sub(r'(?<!dark:)bg-obsidian-900', r'bg-slate-50 dark:bg-obsidian-900', content)
    content = re.sub(r'(?<!dark:)bg-obsidian-800', r'bg-white dark:bg-obsidian-800', content)
    content = re.sub(r'(?<!dark:)bg-obsidian-950', r'bg-white dark:bg-obsidian-900', content)
    content = re.sub(r'dark:bg-obsidian-950', r'dark:bg-obsidian-900', content)
    content = re.sub(r'(?<!dark:)bg-obsidian-600', r'bg-slate-200 dark:bg-obsidian-600', content)
    content = re.sub(r'(?<!dark:)bg-obsidian-700', r'bg-slate-100 dark:bg-obsidian-700', content)
    
    content = re.sub(r'(?<!dark:)text-white', r'text-slate-900 dark:text-white', content)
    content = re.sub(r'(?<!dark:)text-slate-100', r'text-slate-800 dark:text-slate-100', content)
    content = re.sub(r'(?<!dark:)text-slate-200', r'text-slate-700 dark:text-slate-200', content)
    content = re.sub(r'(?<!dark:)text-slate-300', r'text-slate-600 dark:text-slate-300', content)
    
    content = re.sub(r'(?<!dark:)border-obsidian-600', r'border-slate-200 dark:border-obsidian-600', content)
    content = re.sub(r'(?<!dark:)border-white/5', r'border-slate-200 dark:border-white/5', content)
    content = re.sub(r'(?<!dark:)border-white/10', r'border-slate-200 dark:border-white/10', content)
    content = re.sub(r'(?<!dark:)border-white/20', r'border-slate-300 dark:border-white/20', content)
    
    content = re.sub(r'(?<!dark:)hover:bg-obsidian-600', r'hover:bg-slate-200 dark:hover:bg-obsidian-600', content)
    content = re.sub(r'(?<!dark:)hover:bg-obsidian-700', r'hover:bg-slate-100 dark:hover:bg-obsidian-700', content)
    
    content = content.replace("dark:dark:", "dark:")
    
    content = content.replace("text-slate-900 dark:text-slate-900 dark:text-white", "text-slate-900 dark:text-white")
    content = content.replace("bg-white dark:bg-white dark:bg-obsidian", "bg-white dark:bg-obsidian")
    content = content.replace("bg-slate-50 dark:bg-slate-50 dark:bg-obsidian", "bg-slate-50 dark:bg-obsidian")
    content = content.replace("text-slate-800 dark:text-slate-800 dark:text-slate-100", "text-slate-800 dark:text-slate-100")
    
    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed_files = 0
for root, _, files in os.walk(FRONTEND_SRC):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            if process_file(os.path.join(root, file)):
                changed_files += 1

print(f"Processed and fixed theme classes in {changed_files} files.")
