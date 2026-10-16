from pathlib import Path
import shutil
from datetime import datetime

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Media": {".mp3", ".wav", ".aac", ".flac", ".mp4", ".mkv", ".mov", ".avi"},
    "Code": {".py", ".java", ".cpp", ".c", ".html", ".css", ".js", ".json", ".ipynb", ".sql"},
}

def category_for(path):
    for category, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return category
    return "Others"

def unique_destination(path):
    if not path.exists():
        return path
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
        if not candidate.exists():
            return candidate
        n += 1

def build_plan(source, target):
    plan = []
    script = Path(__file__).resolve()
    for item in source.iterdir():
        if item.is_file() and item.resolve() != script:
            dest = target / category_for(item) / item.name
            plan.append((item, unique_destination(dest)))
    return plan

def move_plan(plan, target):
    log = [f"Run time: {datetime.now().isoformat(timespec='seconds')}"]
    moved = failed = 0
    for old, planned in plan:
        try:
            planned.parent.mkdir(parents=True, exist_ok=True)
            dest = unique_destination(planned)
            shutil.move(str(old), str(dest))
            print(f"Moved: {old.name} -> {dest}")
            log.append(f"MOVED: {old} -> {dest}")
            moved += 1
        except (OSError, shutil.Error) as exc:
            print(f"Could not move {old.name}: {exc}")
            log.append(f"FAILED: {old} ({exc})")
            failed += 1
    try:
        target.mkdir(parents=True, exist_ok=True)
        (target / "organizer_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Could not save log: {exc}")
    print(f"Finished: {moved} moved; {failed} failed.")


def main():
    print("=== AUTOMATED FILE ORGANIZER ===")
    try:
        source_text = input("Source folder: ").strip().strip('"')
        target_text = input("Destination folder: ").strip().strip('"')
    except EOFError:
        print("This runner does not support interactive input. Run in a terminal.")
        return
    if not source_text or not target_text:
        print("Both paths are required.")
        return
    source = Path(source_text).expanduser()
    target = Path(target_text).expanduser()
    if not source.is_dir():
        print("Error: source must be an existing folder.")
        return
    source, target = source.resolve(), target.resolve()
    if source == target or source in target.parents:
        print("Error: destination must be separate and outside the source folder.")
        return
    if target.exists() and not target.is_dir():
        print("Error: destination is not a folder.")
        return
    plan = build_plan(source, target)
    if not plan:
        print("No files found.")
        return
    print("\nPREVIEW — no files have been moved:")
    for old, new in plan:
        print(f"{old.name} -> {new.parent.name}/{new.name}")
    try:
        answer = input("Type YES to move these files: ").strip()
    except EOFError:
        print("No confirmation received. Cancelled.")
        return
    if answer != "YES":
        print("Cancelled. No files were moved.")
        return
    move_plan(plan, target)

if __name__ == "__main__":
    main()
