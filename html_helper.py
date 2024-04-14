import os

manifest_filename = 'manifest.txt'
template_filename = 'template.html'

def read_manifest() -> list[str]:
    pages = []
    with open(manifest_filename, 'r', encoding='utf-8') as file:
        manifest = file.read()
        manifest_lines = manifest.split('\n')
        for line in manifest_lines:
            parts = line.split(':')
            if len(parts) == 3:
                pages.append(parts)
    return pages

def read_template() -> str:
    with open(template_filename, 'r', encoding='utf-8') as file:
        template = file.read()
        return template

def apply_template(content: str, pages: list[str], template: str, content_is_grid: bool) -> str:
    new_content = 'Applying template failed'
    template_parts = template.split('{menu-item}')
    if len(template_parts) == 2:
        extra_parts = template_parts[1].split('{content}')
        template_parts.pop(1)
        for part in extra_parts:
            template_parts.append(part)
    
    if len(template_parts) == 3:
        page_refs = ''
        for page in pages:
            if len(page) == 3:
                page_refs += f'''
                <a class="card" href="{page[1]}.html">
                    <h4>{page[0]}</h4>
                    <img src="images/{page[2]}" alt="Button">
                </a>
                '''

        if content_is_grid:
            new_content = (template_parts[0] + page_refs + template_parts[1] + 
                           f'<div class="card-grid">{page_refs}</div>' + 
                           template_parts[2])
        else:
            new_content = (template_parts[0] + page_refs + template_parts[1] + 
                           content + template_parts[2])
    return new_content

def decorate_html(src: str, pages: list[str], template: str, content_is_grid: bool):
    if content_is_grid:
        existing_content = ''
    else:
        with open(src, 'r', encoding='utf-8') as file:
            existing_content = file.read()

    updated_content = apply_template(existing_content, pages, template, content_is_grid)
    with open(src, 'w', encoding='utf-8') as file:
        file.write(updated_content)
