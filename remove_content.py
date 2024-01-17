import re

def remove_content_inside_tags(input_file, output_file, start_tag, end_tag, tag):
    with open(input_file, 'r', errors= 'ignore') as infile:
        content = infile.read()

    pattern = re.compile(f'{start_tag}(?:(?!{tag}\]).)*{end_tag}', flags=re.DOTALL)
    content = re.sub(pattern, '', content)

    with open(output_file, 'w', errors='ignore') as outfile:
        outfile.write(content)

file = "/Users/george/Downloads/wiki/output-0005.txt"

for _ in range(7):
    remove_content_inside_tags(file, file, "\[tpl\]", "\[/tpl\]", "tpl")
    remove_content_inside_tags(file, file, "\[ref", "ref>", "ref")
    remove_content_inside_tags(file, file, "\[ref", "ref\]", "ref")
    remove_content_inside_tags(file, file, "</ref", "ref>", "ref")
    remove_content_inside_tags(file, file, "</ref", "ref\]", "ref")
    remove_content_inside_tags(file, file, "<ref", "ref>", "ref")
    remove_content_inside_tags(file, file, "<ref", "ref\]", "ref")
    remove_content_inside_tags(file, file, "\[/ref", "ref>", "ref")
    remove_content_inside_tags(file, file, "\[/ref", "ref\]", "ref")



