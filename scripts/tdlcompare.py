import os

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

def batch_compare(source_folder, dest_folder):
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

    # Structured summary report
    print("\n" + "="*60)
    print(" TDL CODE COMPARISON SUMMARY REPORT ".center(60, "="))
    print("="*60)
    print("\nFILES WITH CODE DIFFERENCES (REVIEW REQUIRED):\n")
    if diff_files:
        for fname in diff_files:
            print(f"*** {fname} ***")
        print("\n" + "-"*60)
    else:
        print("None\n" + "-"*60)

    if ok_files:
        print("FILES WITH NO CODE DIFFERENCES (OK):\n")
        for fname in ok_files:
            print(f"    {fname}")
        print("\n" + "-"*60)

    if missing_files:
        print("FILES MISSING IN DESTINATION FOLDER:\n")
        for fname in missing_files:
            print(f"    {fname}")
        print("\n" + "-"*60)

    if diff_files:
        print("\nDETAILED ERRORS:\n")
        for fname in diff_files:
            print(f"{'*'*10} FILE: {fname} {'*'*10}")
            for diff in details[fname]:
                print(f"\n  LINE {diff[0]}:")
                print(f"    Original : {diff[1]}")
                print(f"    Annotated: {diff[2]}")
                print("    " + "-"*40)
            print("\n" + "="*60 + "\n")

# ---- USAGE ----
SOURCE_FOLDER = r"C:\Users\rajan\Desktop\coding by raja\machine learning\tdl code\src"
DEST_FOLDER   = r"C:\Users\rajan\Desktop\coding by raja\machine learning\tdl code\annotated"

if __name__ == "__main__":
    batch_compare(SOURCE_FOLDER, DEST_FOLDER)
