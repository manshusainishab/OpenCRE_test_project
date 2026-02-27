CODE_EXTENSIONS = {"py", "js", "ts", "java", "go", "c", "cpp", "rb"}
DOC_EXTENSIONS = {"md", "yaml", "yml"}
LOCK_FILES = {"package-lock.json", "yarn.lock"}

def route_commit(commit):
    files = commit["files"]

    meaningful_files = []
    structural_files = []

    for f in files:
        filename = f.split("/")[-1]

        if filename in LOCK_FILES:
            structural_files.append(f)
            continue

        if "." in filename:
            ext = filename.split(".")[-1]

            if ext in CODE_EXTENSIONS or ext in DOC_EXTENSIONS:
                meaningful_files.append(f)
            else:
                structural_files.append(f)
        else:
            structural_files.append(f)

    # If ALL files are structural → discard
    if len(meaningful_files) == 0:
        return "discard"

    # If contains code files
    if any(f.split(".")[-1] in CODE_EXTENSIONS for f in meaningful_files):
        return "code_filter"

    # Otherwise treat as documentation/config
    return "gemini_direct"