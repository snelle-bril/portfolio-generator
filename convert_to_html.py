import markdown
import shutil
import os
from html_helper import decorate_html, read_manifest, read_template

source_folder = 'source/'
destination_folder = 'build/web/'

def copy_folder(src: str, dest: str):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)    
        shutil.copytree(src, dest)
        print(f"Folder '{src}' copied to '{dest}' successfully.")
    except Exception as e:
        print(f"Error copying folder: {e}")

print('Starting conversion...')

print('Reading manifest')
pages = read_manifest()

print('Reading template')
template = read_template()

print('Generating html files')
file_list = os.listdir(source_folder)
for filename in file_list:
    file_path = os.path.join(source_folder, filename)
    if os.path.isfile(file_path) and file_path.__contains__('.md'):
        print('Converting ' + filename)
        output_file_name = destination_folder + filename.replace('.md', '.html')
        markdown.markdownFromFile(input = source_folder + filename, output = output_file_name)
        decorate_html(output_file_name, pages, template, False)

print('Generating landing page')
decorate_html(destination_folder + '/index.html', pages, template, True)

print('Copying images')
copy_folder(source_folder + 'images/', destination_folder + 'images/')

print('Copying styles')
copy_folder(source_folder + 'styles/', destination_folder + 'styles/')

print('Done')