import os
import re

# ----------- USER CONFIGURATION -----------
SOURCE_FOLDER = r"src"
DEST_FOLDER   = r"annotated"
# ------------------------------------------

# Section patterns and their documentation headers
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
    """Reads a TDL file, adds documentation comments, and writes to destination."""
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Prepare file header (does not touch code)
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
        # Insert section headers before matching lines, but do NOT change the line itself
        inserted = False
        for pattern, doc in SECTION_HEADERS:
            if re.match(pattern, line.strip(), re.IGNORECASE):
                annotated.append(doc)
                inserted = True
                break
        annotated.append(line)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.writelines(annotated)

def batch_annotate_tdl(source_folder, dest_folder):
    """Batch processes all .txt/.tdl files for annotation."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for fname in os.listdir(source_folder):
        if fname.lower().endswith(('.txt', '.tdl')):
            src_path = os.path.join(source_folder, fname)
            dest_path = os.path.join(dest_folder, fname)
            annotate_tdl_file(src_path, dest_path)
            print(f"Annotated: {fname}")

if __name__ == "__main__":
    batch_annotate_tdl(SOURCE_FOLDER, DEST_FOLDER)
    print("\nBatch annotation complete. Annotated files are in:", DEST_FOLDER)
    
