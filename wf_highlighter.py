import os
import sys
import json
import copy
import xml.etree.ElementTree as ElementTree

GRAY_STYLE = "fillColor=#f5f5f5;fontColor=#CCCCCC;strokeColor=#CCCCCC;"


def parse_wf_config_file(filename):
    filename += '.json'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    # Read and parse JSON file
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


def highlighted_children(new_diagram, highlighted_id_set):
    for cell in new_diagram.findall('.//mxCell'):
        if cell.get('style') is not None:
            if cell.get('source') is None and cell.get('target') is None and cell.get('parent') in highlighted_id_set:
                highlighted_id_set.add(cell.get('id'))


def highlighter(filename, config):
    filename += '.drawio'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    # Load and parse drawio file and get the root node
    tree = ElementTree.parse(file_path)
    root = tree.getroot()

    # Get the main diagram node, this diagram include all the nodes
    main_diagram = root.find('diagram')

    if main_diagram is not None:
        # Clean the old sub diagrams
        for node in root.findall('diagram'):
            if node is not main_diagram:
                root.remove(node)

        # `new_diagram_name` is the sub-workflow name
        # `new_diagram_nodes` is the sub-workflow node set
        for new_diagram_name, new_diagram_nodes in config.items():
            new_diagram_nodes = set(new_diagram_nodes)

            # Make a copy of the main diagram node and update the name of the new_diagram
            new_diagram = copy.deepcopy(main_diagram)
            new_diagram.set('name', new_diagram_name)

            # Get basic highlighted nodes id set based on the configuration
            highlighted_id_set = set()
            for cell in new_diagram.findall('.//mxCell'):
                if cell.get('style') is not None:
                    if cell.get('value') in new_diagram_nodes or cell.get('id') in new_diagram_nodes:
                        highlighted_id_set.add(cell.get('id'))

            # Get the children of these highlighted nodes id set, except lines
            highlighted_children(new_diagram, highlighted_id_set)

            # Get the highlighted line ids set
            for cell in new_diagram.findall('.//mxCell'):
                if cell.get('value') not in new_diagram_nodes and cell.get('style') is not None:
                    if (cell.get('source') is not None and cell.get('source') in highlighted_id_set
                            and cell.get('target') is not None and cell.get('target') in highlighted_id_set):
                        highlighted_id_set.add(cell.get('id'))

            # Get the children of these highlighted nodes id set, for lines' label
            highlighted_children(new_diagram, highlighted_id_set)

            # Start dimming
            for cell in new_diagram.findall('.//mxCell'):
                if cell.get('style') is not None:
                    if cell.get('id') not in highlighted_id_set:
                        existing_style = cell.get('style', '')
                        if not existing_style.endswith(GRAY_STYLE):
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
