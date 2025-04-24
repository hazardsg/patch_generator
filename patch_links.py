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
    
    if link['patch_type'] == 'switch':
        harness_switch_1, harness_interface_1 = patch_matrix[link['switch_a']].split(":")
        harness_switch_2, harness_interface_2 = patch_matrix[link['switch_b']].split(":")
        patch_id = link['patch_id']

        
        if harness_switch_1 == harness_switch_2:
            # Values pass to the templates.
            kwargs = {
                'harness_interface_1': harness_interface_1,
                'harness_interface_2': harness_interface_2,
                'patch_id': patch_id
            }

            # Get the template tile.
            template_file = "switch_same_harness.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{harness_switch_1}.cfg", "a") as f:
                f.write(output)
        else:
            # Values pass to the templates.
            kwargs = {
                'harness_interface': harness_interface_1,
                'patch_id': patch_id
            }

            # Get the template tile.
            template_file = "switch_different_harness.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{harness_switch_1}.cfg", "a") as f:
                f.write(output)

                    # Values pass to the templates.
            kwargs = {
                'harness_interface': harness_interface_2,
                'patch_id': patch_id
            }

            # Get the template tile.
            template_file = "switch_different_harness.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{harness_switch_2}.cfg", "a") as f:
                f.write(output)
            
    elif link['patch_type'] == 'host':
        switch, switch_interface = patch_matrix[link['switch']].split(":")
        host_switch, host_interface = link['host'].split(":")
        patch_id = link['patch_id']
        try:
            switch_tag = link['switch_tag']
        except KeyError:
            switch_tag = '0'

        kwargs = {
            'switch': switch,
            'switch_interface': switch_interface,
            'host_switch': host_switch,
            'host_interface': host_interface,
            'patch_id': patch_id,
            'encap': link['encap'],
            'switch_tag': switch_tag
                
        }
        if switch == host_switch:
            # Get the template tile.
            template_file = "host_local_switch.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{host_switch}.cfg", "a") as f:
                f.write(output)

        else:
            # Get the template tile.
            template_file = "host_local_switch.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{host_switch}.cfg", "a") as f:
                f.write(output)

            # Get the template tile.
            template_file = "host_remote_switch.jinja2"
            template = templateEnv.get_template(template_file)
            
            # Render the template
            output = template.render(**kwargs)  

            # Save the template to the act/ directory
            with open(f"harness_config/{switch}.cfg", "a") as f:
                f.write(output)