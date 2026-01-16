from tkinter import Tk, filedialog
import base64
import os

def select_py_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select a Python file to obfuscate",
        filetypes=[("Python files", "*.py")]
    )

def obfuscate_python_code(code):
    encoded = base64.b64encode(code.encode("utf-8")).decode("utf-8")
    loader = (
        "import base64\n"
        f"exec(base64.b64decode('{encoded}').decode('utf-8'))"
    )
    return loader

def main():
    file_path = select_py_file()

    if not file_path:
        print("No file selected")
        return

    if not file_path.endswith(".py"):
        print("Only .py files are allowed")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    obfuscated_code = obfuscate_python_code(original_code)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(obfuscated_code)

    print("File successfully obfuscated")
    print("File overwritten:", file_path)

if __name__ == "__main__":
    main()
