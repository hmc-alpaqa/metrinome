import os

def rename_main_in_c_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.c'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()

                # Replace 'int main' with 'int main_func'
                content = content.replace('int main', 'int main_func')

                with open(filepath, 'w') as f:
                    f.write(content)

                print(f"Processed {filepath}")

if __name__ == "__main__":
    path = input("Enter the directory path to process: ")
    rename_main_in_c_files(path)
    print("Processing complete.")