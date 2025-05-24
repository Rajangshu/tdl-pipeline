import os
import sys

def is_code_line(line):
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith(';')

def read_code_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f if is_code_line(line)]

def compare_files(orig_path, anno_path):
    orig_lines = read_code_lines(orig_path)
    anno_lines = read_code_lines(anno_path)
    max_len = max(len(orig_lines), len(anno_lines))
    diffs = []
    for i in range(max_len):
        o = orig_lines[i] if i < len(orig_lines) else "<no line>"
        a = anno_lines[i] if i < len(anno_lines) else "<no line>"
        if o != a:
            diffs.append((i+1, o, a))
    return diffs

def batch_compare(source_folder, dest_folder, report_file):
    ok_files = []
    diff_files = []
    missing_files = []
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.txt', '.tdl'))]
    details = {}

    for fname in files:
        orig_path = os.path.join(source_folder, fname)
        anno_path = os.path.join(dest_folder, fname)
        if not os.path.exists(anno_path):
            missing_files.append(fname)
            continue
        diffs = compare_files(orig_path, anno_path)
        if not diffs:
            ok_files.append(fname)
        else:
            diff_files.append(fname)
            details[fname] = diffs

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n" + "="*60 + "\n")
        f.write(" TDL CODE COMPARISON SUMMARY REPORT ".center(60, "=") + "\n")
        f.write("="*60 + "\n\n")
        f.write("FILES WITH CODE DIFFERENCES (REVIEW REQUIRED):\n\n")
        if diff_files:
            for fname in diff_files:
                f.write(f"*** {fname} ***\n")
            f.write("\n" + "-"*60 + "\n")
        else:
            f.write("None\n" + "-"*60 + "\n")

        if ok_files:
            f.write("FILES WITH NO CODE DIFFERENCES (OK):\n\n")
            for fname in ok_files:
                f.write(f"    {fname}\n")
            f.write("\n" + "-"*60 + "\n")

        if missing_files:
            f.write("FILES MISSING IN DESTINATION FOLDER:\n\n")
            for fname in missing_files:
                f.write(f"    {fname}\n")
            f.write("\n" + "-"*60 + "\n")

        if diff_files:
            f.write("\nDETAILED ERRORS:\n\n")
            for fname in diff_files:
                f.write(f"{'*'*10} FILE: {fname} {'*'*10}\n")
                for diff in details[fname]:
                    f.write(f"\n  LINE {diff[0]}:\n")
                    f.write(f"    Original : {diff[1]}\n")
                    f.write(f"    Annotated: {diff[2]}\n")
                    f.write("    " + "-"*40 + "\n")
                f.write("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        SOURCE_FOLDER = sys.argv[1]
        DEST_FOLDER = sys.argv[2]
    else:
        print("Usage: python tdlcompare.py <source_folder> <destination_folder>")
        sys.exit(1)
    report_folder = "reports"
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    report_file = os.path.join(report_folder, f"compare_report_{os.path.basename(SOURCE_FOLDER)}.txt")
    batch_compare(SOURCE_FOLDER, DEST_FOLDER, report_file)
