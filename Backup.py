import os
import shutil
import datetime

def create_backup():
    # Get current date and time for backup filename
    now = datetime.datetime.now()
    filename = f"backup_{now.strftime('%Y-%m-%d_%H-%M-%S')}.zip"

    # Create a zip archive of the PC files
    zip_filename = os.path.splitext(filename)[0] + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk('/'):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start='/')
                zip_file.write(file_path, rel_path)

    # Create a manifest of the backup
    with open(filename, 'w') as f:
        f.write(zip_filename + '\n')

    print(f"Backup created successfully: {filename}")

def verify_backup():
    try:
        with zipfile.ZipFile(filename, 'r') as zip_file:
            print("Backup verification successful. Please proceed with restoration.")
            return True
    except FileNotFoundError:
        print("Backup file not found. Restoration cannot be performed.")
        return False

def restore_from_backup():
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            print("Restoration in progress...")
            for item in zip_file.infolist():
                file_path = os.path.join(os.getcwd(), item.filename)
                with open(file_path, 'wb') as f:
                    f.write(zip_file.read(item.filename))
        print("Restoration complete.")
    except Exception as e:
        print(f"Error during restoration: {e}")

# Main function
def main():
    global filename, zip_filename
    filename = "backup.zip"
    zip_filename = os.path.splitext(filename)[0] + '.zip'

    # Ask user for backup type (full or incremental)
    while True:
        choice = input("Do you want to create a full backup (F) or an incremental backup (I)? ")
        if choice.upper() == 'F':
            create_backup()
            break
        elif choice.upper() == 'I':
            # Incremental backup logic will be added later
            print("Incremental backup feature is not implemented yet.")
            return
        else:
            print("Invalid choice. Please choose F or I.")

    while True:
        response = input("Do you want to verify the backup (V)? ")
        if response.upper() == 'Y':
            verify_backup()
            break
        elif response.upper() == 'N':
            break
        else:
            print("Invalid choice. Please choose Y or N.")

    if verify_backup():
        while True:
            restore_choice = input("Do you want to proceed with restoration (R)? ")
            if restore_choice.upper() == 'Y':
                restore_from_backup()
                break
            elif restore_choice.upper() == 'N':
                print("Restoration cancelled.")
                return
            else:
                print("Invalid choice. Please choose Y or N.")

if __name__ == "__main__":
    main()
