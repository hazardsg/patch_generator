# Patch Generator

Patch Generator is a Python script used to define links in the OHV Lab using link definitions similair to ContainerLab. Instead of looking up connections in the patch matrix, connections are defined in the links.yml file. Each link defines the two devices that will be patched(switch or ESX Host)and a unique patch_id. Host links will also have an encap definition and, if the link is tagged, a switch tag.

Once the links.yml file is complete, the script will build the configuration for each harness switch in the harness_config folder.

## DevContainer

All required packages are installed on the dev container.


## links.yml Format

Switch/ESX host names and interfaces should match the OHV Lab Patch Matrix. "Host:Interface" format should be used in the links.yml file. 

Example links.yml file:

```python
  # Switch to Switch Patch
  - patch_type: "switch"
    switch_a: "7280CR3-1:Ethernet1/1"
    switch_b: "7280SR3-1:Ethernet1"
    patch_id: "2000"
  
  # Host to Switch Patch - Untagged
  - patch_type: "host"
    switch: "7280SR-1:Ethernet1"
    host: "ESX1:NIC1/4"
    patch_id: "2002"
    encap: "untagged"
  
  # Host to Switch Patch - Tagged
  - patch_type: "host"
    switch: "7280SR-1:Ethernet2"
    host: "ESX1:NIC1/4"
    patch_id: "2003"
    encap: "tagged"
    switch_tag: "10"
```

Usage:

```bash
vscode@eff94367b1ab:/workspaces/patch_generator$ make patch
```