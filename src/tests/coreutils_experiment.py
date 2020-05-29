"""Various utilities used only for testing and not the main REPL."""
import subprocess
import os
import sys
sys.path.append("/app/code/lang_to_cfg/")
from cpp import CPPConvert  # type: ignore


def convert_file_to_standard(file):
    """Convert a single file to the standard format."""
    converter = CPPConvert(None)
    nodes, edges, node_map, counter = converter.parse_original(file)

    # Covers case of leaf CFGs.
    if len(nodes) == 1:
        nodes.append("1")
        nodes.append("2")
        counter += 2
    filename = os.path.split(file)[1]
    # Make a temporary file (with the new content).
    with open(f'cleaned/{filename}', 'w') as new_file:
        new_file.write("digraph { \n")

        # Create the nodes and then the edges.
        for i, node in enumerate(nodes):
            if i == counter - 1:
                node += "[label=\"EXIT\"]"
            new_file.write(node + ";" + "\n")

        for edge in edges:
            for name in node_map:
                edge = edge.replace(name, node_map[name])
                edge = edge.replace(":s0", "")
                edge = edge.replace(":s1", "")

            new_file.write(edge + "\n")
        new_file.write("}")


def clean(file):
    """Remove unecessary files."""
    filepath = os.path.split(file)[0]
    os.chdir(os.path.split(filepath)[0])
    subprocess.check_call(["mkdir", "-p", "cleaned"])
    convert_file_to_standard(file)


if __name__ == "__main__":
    pass
    # """Run all CFGs through the converter to create a benchmark."""
    # files = (glob2.glob("/app/code/tests/core/separate/*"))

    # os.chdir("/app/code/tests/core/separate")
    # for file in files:
    #     name = os.path.basename(file)
    #     os.chdir(f"/app/code/tests/core/separate/{name}/")
    #     f = f".{name}.bc"
    #     subprocess.check_call(["opt", "-dot-cfg", f"{f}"])
