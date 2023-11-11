import os
import subprocess


def generate_dot_files(input_bc_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate DOT files
    cmd = f"opt -dot-cfg {input_bc_file}"
    subprocess.run(cmd, shell=True, check=True)

    # Move DOT files to the output directory
    dot_files = [f for f in os.listdir() if f.endswith(".dot")]
    for dot_file in dot_files:
        os.rename(dot_file, os.path.join(output_dir, dot_file))


def process_directory(input_directory):
    # Loop through all bitcode files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".bc"):
            print(filename)
            input_bc_file = os.path.join(input_directory, filename)
            # Create a directory based on the input filename
            output_dir = os.path.join(f'{filename.split(".")[0]}_bc')
            generate_dot_files(input_bc_file, output_dir)


if __name__ == "__main__":
    # Change this to your input directory
    input_directory = "/home/dchen327/coding/hmc/metrinome/src/experiments/coreutils"
    process_directory(input_directory)
