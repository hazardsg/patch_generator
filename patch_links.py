import jinja2
import yaml
import csv
import os
from pprint import pprint

# Jinja2 setup
templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
templateEnv = jinja2.Environment(loader=templateLoader)

# Initialize the harness config files
for i in range(1, 5):
    with open(f'harness_config/HARNESS{i}.cfg', 'w') as f: 
        pass 

# Load the list of links that will be used to create the Harness switch config.
with open("links.yml", "r") as f:
    switch_links = yaml.load(f, Loader=yaml.FullLoader)

patch_matrix = {}

with open("ohv_patch_matrix.csv", 'r') as f:
  for line in csv.DictReader(f):
        patch_matrix[line['a_node']+":"+line['a_node_interface']] = line['b_node']+":"+line["b_node_interface"]

# pprint(patch_matrix)

for link in switch_links['link_list']:
    harness_switch_1, harness_interface_1 = patch_matrix[link['switch_1']].split(":")
    harness_switch_2, harness_interface_2 = patch_matrix[link['switch_2']].split(":")
    patch_id = link['patch_id']
    pprint(harness_switch_1)
    pprint(harness_switch_2)
    if harness_switch_1 == harness_switch_2:
        # Values pass to the templates.
        kwargs = {
            'harness_interface_1': harness_interface_1,
            'harness_interface_2': harness_interface_2,
            'patch_id': patch_id
        }

        # Get the template tile.
        template_file = "same_harness.jinja2"
        template = templateEnv.get_template(template_file)
        
        # Render the template
        output = template.render(**kwargs)  

        # Save the template to the act/ directory
        with open(f"harness_config/{harness_switch_1}.cfg", "a+") as f:
            f.write(output)
    else:
        # Values pass to the templates.
        kwargs = {
            'harness_interface_1': harness_interface_1,
            'patch_id': patch_id
        }

        # Get the template tile.
        template_file = "different_harness.jinja2"
        template = templateEnv.get_template(template_file)
        
        # Render the template
        output = template.render(**kwargs)  

        # Save the template to the act/ directory
        with open(f"harness_config/{harness_switch_1}.cfg", "a+") as f:
            f.write(output)

                # Values pass to the templates.
        kwargs = {
            'harness_interface_1': harness_interface_2,
            'patch_id': patch_id
        }

        # Get the template tile.
        template_file = "different_harness.jinja2"
        template = templateEnv.get_template(template_file)
        
        # Render the template
        output = template.render(**kwargs)  

        # Save the template to the act/ directory
        with open(f"harness_config/{harness_switch_2}.cfg", "a+") as f:
            f.write(output)