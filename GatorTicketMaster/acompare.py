from difflib import Differ

def compare_files_with_line_numbers(file1_path, file2_path):
    # Read the contents of the files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Use Differ from difflib to compare the lines
    differ = Differ()
    diff = list(differ.compare(file1_lines, file2_lines))

    # Variables to track the line numbers for each file
    line_num_file1 = 0
    line_num_file2 = 0

    # Keep track of different line numbers
    different_lines_file1 = []
    different_lines_file2 = []

    # Display the differences with line numbers
    for line in diff:
        if line.startswith('  '):  # Lines that are the same in both files
            line_num_file1 += 1
            line_num_file2 += 1
            # print(f"Line {line_num_file1} (same): {line.strip()}")
        elif line.startswith('- '):  # Lines that are in file1 but not in file2
            line_num_file1 += 1
            different_lines_file1.append(line_num_file1)
            # print(f"Line {line_num_file1} (correct only): {line.strip()}")
        elif line.startswith('+ '):  # Lines that are in file2 but not in file1
            line_num_file2 += 1
            different_lines_file2.append(line_num_file2)
            # print(f"Line {line_num_file2} (output only): {line.strip()}")

    # Display the lines that are different in both files
    if different_lines_file1 or different_lines_file2:
        print("\n################## SUMMARY ##################")
        if different_lines_file1:
            print(f"Lines different in File 1: {different_lines_file1}")
        if different_lines_file2:
            print(f"Lines different in File 2: {different_lines_file2}")
    else:
        print("The files are identical.")

# Example usage
file1 = 'test1_correct_output.txt'
file2 = 'test1_output_file.txt'

compare_files_with_line_numbers(file1, file2)