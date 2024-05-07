import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
import glob
def convert_ui_file(ui_file_path, output_dir=None):
    """Converts a single UI file to a Python class.

    Args:
        ui_file_path (str): Path to the UI file.
        output_dir (str, optional): Directory to save the converted Python file.
            If not specified, the current directory is used.

    Returns:
        str: Name of the converted Python file (without extension) on success,
             or None on failure.
    """

    file_name = os.path.basename(ui_file_path)
    if not file_name.endswith(".ui"):
        print(f"Skipping {file_name}: Not a UI file.")
        return None

    try:
        # Open UI file for reading
        with open(ui_file_path, 'r') as fin:
            # Determine output filename based on input filename and output directory
            if output_dir:
                output_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".py")
            else:
                output_path = os.path.splitext(file_name)[0] + ".py"

            # Open output file for writing
            with open(output_path, 'w') as fout:
                try:
                    # Perform UI conversion
                    uic.compileUi(fin, fout, execute=False)
                    print(f"Converted {file_name} to {output_path}")
                    return os.path.splitext(file_name)[0]  # Return class name (without extension)
                except Exception as e:
                    print(f"Error converting {file_name}: {e}")
                    return None

    except FileNotFoundError as e:
        print(f"Error: File not found: {ui_file_path}")
        return None

def main():
    """Converts all UI files in the current directory or a specified path.

    Handles potential errors and displays informative messages using QMessageBox.
    """

    if len(sys.argv) > 2:
        print("Usage: python ui_converter.py [directory]")
        return

    # Get directory path (current directory by default)
    directory = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()

    # Convert all UI files in the directory
    converted_files = []
    for ui_file in glob.glob(os.path.join(directory, "*.ui")):
        converted_class_name = convert_ui_file(ui_file)
        if converted_class_name:
            converted_files.append(converted_class_name)

    # Display success or failure message (using QMessageBox for consistent look)
    if converted_files:
        message = f"Successfully converted {len(converted_files)} UI files:\n" + "\n".join(converted_files)
        QMessageBox.information(None, "UI Conversion", message, QMessageBox.Ok)
    else:
        QMessageBox.warning(None, "UI Conversion", "No UI files found or conversion failed.", QMessageBox.Ok)

if __name__ == '__main__':
    main()
