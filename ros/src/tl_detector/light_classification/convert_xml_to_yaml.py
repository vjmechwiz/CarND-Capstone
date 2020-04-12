#!/usr/bin/env python
import os
import xmlplain


def mulitple_xml_to_yaml(input_folder):
    xml_files = []
    yaml_list = []
    for item in sorted(os.listdir(input_folder)):
        if item.endswith('.xml'):
            xml_files.append(item)
    if len(xml_files) == 0:
        raise ValueError('No xml files found in current directory')
    else:
        yaml_file = os.path.join(
            os.path.dirname(input_folder), 'annotations.yaml')
        with open(yaml_file, 'w+') as out_file:
            for xml_file in xml_files:
                xml_file_path = os.path.join(
                    os.path.dirname(input_folder), xml_file)
                with open(xml_file_path) as xf:
                    xml_obj = xmlplain.xml_to_obj(xf, strip_space=True, fold_dict=True)
                    yaml_list.append(xml_obj)
            xmlplain.obj_to_yaml(yaml_list, out_file)
