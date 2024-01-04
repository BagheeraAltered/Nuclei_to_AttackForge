import json
import sys

def format_nuclei_output(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            raw_json_objects = file.read().strip()

        # Assuming each JSON object is separated by a newline followed by a curly brace
        # Add commas and wrap in square brackets
        fixed_json_string = "[" + raw_json_objects.replace("}\n{", "},\n{") + "]"

        # Parse it into an actual JSON object to check if it's valid JSON
        parsed_json = json.loads(fixed_json_string)

        # Now write it back to a new file with indentation
        with open(output_file_path, 'w') as outfile:
            json.dump(parsed_json, outfile, indent='\t')

        print(f"Formatted JSON has been written to {output_file_path}")
    except json.JSONDecodeError as e:
        # If there's an error, let the user know and show the problematic line
        error_line = fixed_json_string.splitlines()[e.lineno - 1]
        print(f"JSON decode error near line {e.lineno}: {e}")
        print(f"Error line content: {error_line}")
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: fixjsonarray.py <input_file_path> <output_file_path>")
        sys.exit(1)

    # The path to your original nuclei output
    input_file_path = sys.argv[1]
    # The path to the new, formatted JSON file
    output_file_path = sys.argv[2]

    format_nuclei_output(input_file_path, output_file_path)
