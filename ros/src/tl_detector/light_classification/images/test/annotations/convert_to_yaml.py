import os

separator = '\n'
xml_files = []
for item in os.listdir('.'):
    if item.endswith('.xml'):
        xml_files.append(item)
if len(xml_files) == 0:
    raise ValueError('No xml files found in current directory')
else:
    if not os.path.exists('./annotations.yaml'):
        with open('./annotations.yaml', 'w+') as out_file:
            for xml_file in xml_files:
                with open (xml_file) as in_file:
                    xml_content = in_file.read()
                    out_file.write(xml_content)
                    out_file.write(separator)


