import re

def remove_content_inside_tags(input_file, output_file, tag):
    with open(input_file, 'r') as infile:
        content = infile.read()

    pattern = re.compile(f'\[{tag}\](?:(?!{tag}\]).)*\[/{tag}\]', flags=re.DOTALL)
    content = re.sub(pattern, '', content)

    with open(output_file, 'w') as outfile:
        outfile.write(content)

file = "/Users/george/Downloads/wiki/output-0005.txt"

for _ in range(7):
    remove_content_inside_tags(file, file, "tpl")
