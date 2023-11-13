import os
import sys
import json
import copy
import xml.etree.ElementTree as ET

GRAY_STYLE = "fillColor=#f5f5f5;fontColor=#CCCCCC;strokeColor=#CCCCCC;"


def parse_wf_config_file(filename):
    # 构建文件路径
    filename += '.json'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    # 读取并解析JSON文件
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Can not find file: {filename} under the same folder with current script")
        return {}
    except json.JSONDecodeError:
        print(f"JSON parse error, please check the format of {filename}")
        return {}


def highlighter(filename, config):
    filename += '.drawio'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    # Load and parse drawio file and get the root node
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Get the first diagram node
    diagram = root.find('diagram')

    if diagram is not None:
        # Go through the nodes under root and delete all these diagram nodes except the first diagram
        for node in root.findall('diagram'):
            if node is not diagram:
                root.remove(node)

        for new_diagram_name, new_diagram_nodes in config.items():
            new_diagram_nodes = set(new_diagram_nodes)

            # Make a copy of the first diagram node and update the name of the new_diagram
            new_diagram = copy.deepcopy(diagram)
            new_diagram.set('name', new_diagram_name)

            # Go through all the mxCell nodes under new_diagram and modify the style property, make it become gray
            new_diagram_nodes_id_set = set()
            for cell in new_diagram.findall('.//mxCell'):
                if cell.get('value') not in new_diagram_nodes:
                    # Do not handle lines at this step, will handle them later
                    if cell.get('source') is None and cell.get('target') is None:
                        new_diagram_nodes_id_set.add(cell.get('id'))

                        existing_style = cell.get('style', '')
                        new_style = existing_style + GRAY_STYLE
                        cell.set('style', new_style)

            # Handle lines' highlight
            for cell in new_diagram.findall('.//mxCell'):
                if cell.get('value') not in new_diagram_nodes:
                    if not (cell.get('source') is not None and cell.get('source') not in new_diagram_nodes_id_set
                            and cell.get('target') is not None and cell.get('target') not in new_diagram_nodes_id_set):
                        existing_style = cell.get('style', '')
                        new_style = existing_style + GRAY_STYLE
                        cell.set('style', new_style)

            # Add the new_diagram into root
            root.append(new_diagram)

    # Update and save the file
    tree.write(file_path)


"""
Run script
"""
if len(sys.argv) > 1:
    input_filename = sys.argv[1]
    print(f"Drawio filename is: {input_filename}.drawio")
    print(f"Config filename is: {input_filename}.json")

    wf_config = parse_wf_config_file(input_filename)
    highlighter(input_filename, wf_config)

    print(f"Finished!")
else:
    print("No filename provided.")
    print("Please use: python3 wf_highlighter.py [filename without file suffix]")
