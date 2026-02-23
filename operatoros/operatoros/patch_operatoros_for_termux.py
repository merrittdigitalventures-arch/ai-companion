import os
import re

# Path to your OperatorOS project (this file should be inside operatoros/)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Regex patterns
MODEL_CONFIG_PATTERN = re.compile(r'model_config\s*=\s*ConfigDict\((.*?)\)', re.DOTALL)
PDC_IMPORT_PATTERN = re.compile(r'from\s+pydantic_core\s+import\s+.*')

def patch_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove any pydantic_core imports
    content = PDC_IMPORT_PATTERN.sub('# removed pydantic_core import', content)

    # Convert v2 model_config to v1 class Config
    def replace_model_config(match):
        inner = match.group(1).strip()
        # Transform key=value to key = value format inside Config
        inner_lines = []
        for kv in inner.split(','):
            if '=' in kv:
                key, val = kv.split('=', 1)
                inner_lines.append(f"        {key.strip()} = {val.strip()}")
        return "    class Config:\n" + "\n".join(inner_lines)

    content = MODEL_CONFIG_PATTERN.sub(replace_model_config, content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {file_path}")

def patch_project():
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith('.py'):
                patch_file(os.path.join(root, file))

if __name__ == '__main__':
    patch_project()
    print("OperatorOS Termux patch complete!")
