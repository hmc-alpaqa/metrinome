"""Various utilities used only for testing and not the main REPL."""
import subprocess
import os
import sys
sys.path.append("/app/code/lang_to_cfg/")
from cpp import CPPConvert  # type: ignore


def convert_file_to_standard(file):
    """Convert a single file to the standard format."""
    converter = CPPConvert(None)
    converter.convert_file_to_standard(file)


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
