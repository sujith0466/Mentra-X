import os

directory = 'd:/AI-Student Platform/frontend/src'

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'dark:hover:text-slate-900 dark:text-white' in content:
                new_content = content.replace('dark:hover:text-slate-900 dark:text-white', 'dark:hover:text-white')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {path}")
