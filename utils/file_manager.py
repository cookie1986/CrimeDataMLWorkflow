import os
import shutil
from dotenv import load_dotenv
from config.settings import settings

# load environment variables from the .env file (stored in config subdir)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config','.env')
load_dotenv(dotenv_path)

# fetch the path files
# master_data_file = os.getenv("MASTER_DATA_FILE")
# local_data_file_path = os.getenv("LOCAL_DATA_FILE_PATH")


if not settings.MASTER_DATA_FILE:
    raise Exception("No environment variable named MASTER_DATA_FILE was found in the .env file.")
if not settings.LOCAL_DATA_FILE_PATH:
    raise Exception("No local file path was found in the .env file.")


def check_master_file_exists():
    """Check if the master data file exists in the specified location."""
    if os.path.exists(settings.MASTER_DATA_FILE):
        print(f"Master data file exists:{settings.MASTER_DATA_FILE}")
        return True
    else:
        raise FileNotFoundError(f"Master data file does not exist: {settings.MASTER_DATA_FILE}")
    

def duplicate_master_data_locally():
    """Duplicate the master data to the local repository."""
    # if not os.path.exists(master_data_file):
    if not os.path.exists(settings.MASTER_DATA_FILE):
        FileNotFoundError(f"Master data file does not exist: {settings.MASTER_DATA_FILE}")
    
    # os.makedirs(local_data_file_path, exist_ok=True)
    os.makedirs(settings.LOCAL_DATA_FILE_PATH, exist_ok=True)
    local_file = os.path.join(settings.LOCAL_DATA_FILE_PATH, os.path.basename(settings.MASTER_DATA_FILE))
    shutil.copy2(settings.MASTER_DATA_FILE, local_file)


def delete_local_data():
    """Delete the local data file."""
    if os.path.exists(settings.LOCAL_DATA_FILE_PATH):
        shutil.rmtree(settings.LOCAL_DATA_FILE_PATH)
        print(f"Local data repository deleted: {settings.LOCAL_DATA_FILE_PATH}")
    else:
        print(f"No local data repository found: {settings.LOCAL_DATA_FILE_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Data management script")
    parser.add_argument("--check", action="store_true", help="Check if the master file exists.")
    parser.add_argument("--duplicate", action="store_true", help="Duplicate the master file locally.")
    parser.add_argument("--delete", action="store_true", help="Delete the local data repository.")

    args = parser.parse_args()

    if args.check:
        check_master_file_exists()
    if args.duplicate:
        duplicate_master_data_locally()
    if args.delete:
        delete_local_data()