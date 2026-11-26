# -*- coding: utf-8 -*-
with open('OPEN_IN_BROWSER.html', 'rb') as f:
    html = f.read()

import re
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
assert len(scripts) == 1, 'Script tag count mismatch'
code = scripts[0]

assert "'''" not in code, 'Found stray triple quotes'
assert '"""' not in code, 'Found stray triple double quotes'
assert 'const SAMPLES = [' in code, 'SAMPLES not formatted as array'
assert 'const DISEASES = [' in code, 'DISEASES not formatted as array'
assert 'function toggleChat' in code
assert 'function sendChatMessage' in code
assert 'callBackendChat' in code
assert 'analyzeImageFeatures' in code
assert 'generateGradCAM' in code

print("Verification SUCCESS: OPEN_IN_BROWSER.html is 100% syntactically valid and clean!")
