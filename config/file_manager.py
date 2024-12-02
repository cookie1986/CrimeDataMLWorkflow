import os
import shutil
from dotenv import load_dotenv

# load environment variables from the .env file
load_dotenv()

# fetch the path files
master_data_file = os.getenv("MASTER_DATA_FILE")
local_data_file_path = os.getenv("LOCAL_DATA_FILE_PATH")


if not master_data_file:
    raise Exception("No environment variable named MASTER_DATA_FILE was found in the .env file.")
if not local_data_file_path:
    raise Exception("No local file path was found in the .env file.")


def check_master_file_exists():
    """Check if the master data file exists in the specified location."""
    if os.path.exists(master_data_file):
        print(f"File exists:{master_data_file}")
        return True
    else:
        raise FileNotFoundError(f"Master data file does not exist: {master_data_file}")
    

def duplicate_master_data_locally():
    """Duplicate the master data to the local repository."""
    if not os.path.exists(master_data_file):
        FileNotFoundError("Master data file does not exist: {master_data_file}")
    
    os.makedirs(local_data_file_path, exist_ok=True)
    local_file = os.path.join(local_data_file_path, os.path.basename(master_data_file))
    shutil.copy2(master_data_file, local_file)


def delete_local_data():
    """Delete the local data file."""
    if os.path.exists(local_data_file_path):
        shutil.rmtree(local_data_file_path)
        print(f"Local data repository deleted: {local_data_file_path}")
    else:
        print(f"No local data repository found: {local_data_file_path}")


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