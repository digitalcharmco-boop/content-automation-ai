#!/usr/bin/env python3
"""Package monetization assets into a ZIP for delivery after purchase.

Run from the project root:
  python monetization/build_payload.py

Output: monetization_payload.zip in the project root (next to this monetization/ folder).
"""

import os
import zipfile
from pathlib import Path


def build_zip(output=None):
    base = Path(__file__).parent  # monetization/
    project_root = base.parent    # content_automation_ai/

    if output is None:
        output = project_root / 'monetization_payload.zip'
    else:
        output = Path(output)

    # Files/dirs to include in the payload ZIP
    include_dirs = ['monetization']
    skip_files = {'.pyc', '.DS_Store'}
    skip_dirs = {'__pycache__', '.venv', 'delivered_files'}
    skip_names = {'orders.json', 'sent_log.json', 'deliveries.json', 'secret_map.json', 'branding_config.json'}

    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for dir_name in include_dirs:
            dir_path = project_root / dir_name
            if not dir_path.exists():
                continue
            for root, dirs, files in os.walk(dir_path):
                # Prune skip dirs in-place
                dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
                for f in files:
                    if f.startswith('.') or any(f.endswith(ext) for ext in skip_files):
                        continue
                    if f in skip_names:
                        continue
                    full_path = Path(root) / f
                    arc_name = full_path.relative_to(project_root)
                    z.write(full_path, arcname=arc_name)

    print(f"Built payload: {output}  ({output.stat().st_size // 1024} KB)")
    return str(output)


if __name__ == '__main__':
    build_zip()
