import sys
from pathlib import Path

target = Path(r'C:\Users\charm\content_automation_ai')
patch = 'if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")\n'

fixed = 0
for f in target.glob('*.py'):
    if f.name == 'fix_encoding.py':
        continue
    try:
        txt = f.read_text(encoding='utf-8')
        if 'reconfigure' not in txt and 'import sys' in txt:
            txt = txt.replace('import sys\n', 'import sys\n' + patch, 1)
            f.write_text(txt, encoding='utf-8')
            fixed += 1
            print(f'Patched: {f.name}')
    except Exception as e:
        print(f'Skip {f.name}: {e}')

print(f'\nDone: {fixed} files patched')
