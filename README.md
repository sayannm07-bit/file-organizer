Automated File Organizer 

A command-line Python tool that sorts files by extension. It is safe by default: it only previews planned moves unless --apply is specified.

Features : 
Source and destination paths provided as command-line arguments
Categories: Images, Documents, Archives, Media, Code, and Others
Dry-run preview by default
Moves files only when --apply is used
Duplicate filename protection using incremental suffixes
Skips subdirectories and the running script
Writes organizer_log.txt after an actual run
Reports invalid directories and file-operation errors

Requirements : 
Python 3.9+ recommended
No third-party packages

Preview (does not move files) : 
python main.py --source ./organizer_test --target ./organized_test

Apply the moves : 
After reviewing the preview:
python main.py --source ./organizer_test --target ./organized_test --apply

Safe Test Setup : 
Create organizer_test and place copies of sample files inside it.
Run the preview command first.
Check that the source and target are different folders and the paths look correct.
Run with --apply.
Verify the output folders and organizer_log.txt.
Do not begin with important personal folders or your full Downloads directory.

Categories : 
Images: .png, .jpg, .gif, .svg
Documents: .pdf, .docx, .txt, .xlsx, .pptx
Archives: .zip, .rar, .7z, .tar
Media: .mp3, .wav, .mp4, .mkv
Code: .py, .java, .cpp, .html, .css, .json
Others: extensions not listed above

Safety and Limitations : 
Without --apply, the program does not move files. It does not recursively process subdirectories. Duplicate names receive suffixes such as _1. Permission errors and files in use may prevent a move; keep backups of important files.

Concepts Practised : 
argparse, pathlib, shutil, categorization dictionaries, exception handling, and file-system automation.