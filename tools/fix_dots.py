import re

files = ['events_ar.html', 'events_de.html', 'events_es.html', 'events_tr.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace dots div with simple counter
    pattern = r'<div class="dots">.*?</div>'
    replacement = '<span class="slide-counter">1 / 20</span>'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f'Fixed {f}')
