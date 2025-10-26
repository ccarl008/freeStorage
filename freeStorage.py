import os
import tempfile
from pathlib import Path
import shutil
import ctypes
import sys

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def runAsAdmin():
    if not isAdmin():
        print("Restarting script with admin privileges...")
        params = " ".join(sys.argv)
        if "--admin" not in params:
            params += " --admin"
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

def get_disk_usage():
    total, used, free = shutil.disk_usage("C:\\")
    return  free

def deleteContents(folder: Path):
    """Deletes folder content, keeps folder intact"""
    if not folder.exists():
        return
    print(f"\nCleaning: {folder}")
    try:
        items = list(folder.iterdir())
    except PermissionError:
        print(f"Access denied: {folder}")
        return
    except Exception as e:
        print(f"Error reading {folder}: {e}")
        return
    
    total = len(items)
    deleted = 0

    for item in items:
        try:
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
            deleted += 1
        except PermissionError:
            print(f"Permission denied: {item}")
        except Exception as e:
            print(f"Failed to delete {item}: {e}")
    print(f"Deleted {deleted}/{total} items in {folder.name}", end="\r")

def deleteUserTemp():
    print("Deleting User Temp Files...")
    before = get_disk_usage()
    temp_path = Path(tempfile.gettempdir())
    deleteContents(temp_path)
    after = get_disk_usage()
    freed = after - before
    print(f"Freed {freed / (1024 ** 3):.2f} GB of space from user temp files.")

def deleteSysTemp():
    print("Deleting System Temp Files...")
    before = get_disk_usage()
    system_temp = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Temp"
    deleteContents(system_temp)
    after = get_disk_usage()
    freed = after - before
    print(f"Freed {freed / (1024 ** 3):.2f} GB of space from system temp files.")
    
def deleteBrowserCache():
    print("Deleting Browser Cache...")

    user = Path.home()
    chromePaths = [
        user / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
        user / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Code Cache",
        user / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "GPUCache",
    ]
    edgePaths = [
        user / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
        user / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Code Cache",
        user / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "GPUCache",
    ]
    before = get_disk_usage()
    for path in chromePaths + edgePaths:
        deleteContents(path)
    after = get_disk_usage()
    freed = after - before
    print(f"Freed {freed / (1024 ** 3):.2f} GB of space from browser caches.")

    print("Browser cache cleanup complete.")

def main():
        
    deleteUserTemp()
    if "--browser" in sys.argv:
        deleteBrowserCache()
    deleteSysTemp()
    if "--admin" not in sys.argv and not isAdmin():
        runAsAdmin()
    print("Cleanup finished!")

    

if __name__ == "__main__":
    main()
