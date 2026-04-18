import shutil
import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed 
#COLOR TEXT!!!
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[93m"
#Gets arguments from command line for paths to source and destination folders. If not provided, it will prompt the user for input.
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="Path to source folder")
    parser.add_argument("--dst", help="Path to destination folder")
    parser.add_argument("--dry", action="store_true", help="Run a simulation without copying")

    parser.add_argument("--folder", default="raws", help="Name of subfolder for RAWs")

    parser.add_argument("--d_ext", nargs="*", default=["png", "jpg", "jpeg"], help="Destination extensions")
    parser.add_argument("--s_ext", nargs="*", default=['arw', 'cr2', 'cr3', 'nef', 'dng', 'orf', 'raf', 'rw2'], help="Source extensions")
    return parser.parse_args()

# Gets extensions of the files you have at the destination (e.g., .jpg, .png)
def get_destination_extensions():
    print("\n--- Step 3: Enter the file extensions have at the destination---")
    dest_ext_list = input("Enter file extensions separated by commas (e.g., .jpg,.png): ").strip().split(",")
    dest_ext_list = [ext.strip().lstrip('.') for ext in dest_ext_list]
    return dest_ext_list
         
# Gets extensions of the files you want to copy (e.g., .CR3, .NEF)
def get_source_extensions():
    print("\n--- Step 4: Enter the file extensions you want to copy ---")
    src_ext_list = input("Enter file extensions separated by commas (e.g. CR3, NEF): ").strip().split(",")
    src_ext_list = [ext.strip().lstrip('.') for ext in src_ext_list]
    return src_ext_list
#Main function
def main():
    
    args = get_args()
    folder_name = args.folder
    #Step 1
    #Getting Source Path
    source = args.src
    #If source path not provided as an argument, prompt the user for input
    if not source:
        source = input("Step 1: Paste the path to your Source folder:\n(The files you want to copy to another location) ").strip()
    
    #Step 2
    #Getting Destination Path
    destination = args.dst
    #If destination path not provided as an argument, prompt the user for input
    if not destination:
        destination = input("Step 2: Paste the path to your Destination folder:\n(The location you want to copy files to) ").strip()

    #Converting to Path objects
    source_path = Path(source)
    destination_path = Path(destination)
    

    #Step 3
    #Checking if paths exist
    if not source_path.exists():
        print(f"Error: {source_path} wasn't found. Please check the path and try again.")
        return
    if not destination_path.exists():
        print(f"Error: {destination_path} wasn't found. Please check the path and try again.")
        return
    #Step 4
    print(f"\n--- Step 4: File Extensions ---")
    print(f"Default destination extensions: {', '.join(args.d_ext)}")
    print(f"Default source extensions: {', '.join(args.s_ext)}")
    change = input('Press Enter to continue with default extensions or press s to input your own extensions.').strip().lower()
    if change == 's':   
    #Getting em Extensions
        dest_exts = get_destination_extensions()
        src_exts = get_source_extensions()
    else:
        dest_exts = args.d_ext
        src_exts = args.s_ext
    dest_names = set()
    #Step 5
    #Scanning destination folder for files with specified extensions
    for file in destination_path.rglob('*'):
        if folder_name in file.parts:
            continue
        #Remove the '.' to compare extensions and make it case-insensitive
        if file.suffix.lower().lstrip('.') in [ext.lower() for ext in dest_exts]:
            dest_names.add(file.stem.split('.')[0])
    print(f"\n--- Scanning {source_path.name} ---")

    #Step 6
    #Scanning source folder for files with specified extensions and matching names
    files_to_copy = []
    print(f"Searching {source_path.name} for matches...")
    for file in source_path.rglob('*'):
        #Remove the '.' to compare extensions and make it case-insensitive
        if file.suffix.lower().lstrip('.') in [ext.lower() for ext in src_exts]:
            clean_name = file.stem.split('.')[0]
            #Checking matching names between source and destination folders
            if clean_name in dest_names:
                files_to_copy.append(file)

    #Pretty output with emoji and shit
    print(f"\n{GREEN}✅ Found {len(files_to_copy)} matching RAW files!{RESET}")

    #Step 7
    if not files_to_copy:
        print("No matching files found. Exiting...")
        return
    
    if args.dry:
        print(f"\n{BLUE}--- DRY RUN MODE (No files will be moved) ---{RESET}")
        for f in files_to_copy:
            print(f"Would copy: {f.name} -> {destination_path.name}/")
        return
  
    
    #Step 8
    confirm = input(f"\nReady to copy {len(files_to_copy)} files? (y/n): ").strip().lower()
    if confirm != "y":
        print("Operation cancelled.")
        return
    
    #Makine a new folder for raws to stay
    final_destination = destination_path / folder_name
    final_destination.mkdir(exist_ok=True)
    #Step 9
    start_time = time.time()
    print(f"🚀 {CYAN}Engaging ThreadPoolExecutor (max_workers=4){RESET}...")
    

    with ThreadPoolExecutor(max_workers=4) as executor:
        #Multithreading in case you click wayyy too much
        futures = []
        for f in files_to_copy:
            relative_folder = f.relative_to(source_path).parent
            target_folder = final_destination / relative_folder
            target_folder.mkdir(parents=True, exist_ok=True)
            futures.append(executor.submit(shutil.copy2, f, target_folder))

            
        # Small progress tracker
        done = 0
        for future in as_completed(futures):
            done += 1
            if done % 5 == 0 or done == len(files_to_copy):
                print(f" 🍌 Progress: {done}/{len(files_to_copy)}...")

        end_time = time.time()
        print(f"\n {YELLOW}🍌  🍌  SUCCESS: Synced in {end_time - start_time:.2f} seconds.{RESET}")
         
if __name__ == "__main__":
    main()
