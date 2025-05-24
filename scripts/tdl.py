import os
import re
import sys

SECTION_HEADERS = [
    (r'^\[Report:',      '\n;;--------------------\n;; REPORT DEFINITION\n;;--------------------\n'),
    (r'^\[Form:',        '\n;;--------------------\n;; FORM DEFINITION\n;;--------------------\n'),
    (r'^\[Part:',        '\n;;--------------------\n;; PART DEFINITION\n;;--------------------\n'),
    (r'^\[Line:',        '\n;;--------------------\n;; LINE DEFINITION\n;;--------------------\n'),
    (r'^\[Field:',       '\n;;--------------------\n;; FIELD DEFINITION\n;;--------------------\n'),
    (r'^\[Collection:',  '\n;;--------------------\n;; COLLECTION DEFINITION\n;;--------------------\n'),
    (r'^\[System:',      '\n;;--------------------\n;; SYSTEM/FORMULA DEFINITION\n;;--------------------\n'),
    (r'^\[function:',    '\n;;--------------------\n;; FUNCTION DEFINITION\n;;--------------------\n'),
    (r'^\[button:',      '\n;;--------------------\n;; BUTTON DEFINITION\n;;--------------------\n'),
]

def annotate_tdl_file(src_path, dest_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    filename = os.path.basename(src_path)
    header = [
        ';===============================================================================\n',
        f'; Annotated File: {filename}\n',
        '; This file is auto-annotated for documentation and section clarity.\n',
        '; Original code is preserved. No logic or code is changed.\n',
        ';===============================================================================\n\n'
    ]
    annotated = header.copy()
    for line in lines:
        for pattern, doc in SECTION_HEADERS:
            if re.match(pattern, line.strip(), re.IGNORECASE):
                annotated.append(doc)
                break
        annotated.append(line)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.writelines(annotated)

def batch_annotate_tdl(source_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for fname in os.listdir(source_folder):
        if fname.lower().endswith(('.txt', '.tdl')):
            src_path = os.path.join(source_folder, fname)
            dest_path = os.path.join(dest_folder, fname)
            annotate_tdl_file(src_path, dest_path)
            print(f"Annotated: {fname}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        SOURCE_FOLDER = sys.argv[1]
        DEST_FOLDER = sys.argv[2]
    else:
        print("Usage: python tdl.py <source_folder> <destination_folder>")
        sys.exit(1)
    batch_annotate_tdl(SOURCE_FOLDER, DEST_FOLDER)
    print("\nBatch annotation complete. Annotated files are in:", DEST_FOLDER)
