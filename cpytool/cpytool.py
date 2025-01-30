import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
import shutil
import zipfile

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Read CSV file
csv_file_path = 'cpytool/workfiles/dirlst.csv'
df = pd.read_csv(csv_file_path)

home_dir = 'C:\\Users\\GX171TT\\OneDrive - EY\\Documents\\Notes\\2024\\Nov24\\Windsurf'

# Create a new folder "cpytoolbkups/<timestamp>"
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
backup_dir = os.path.join('cpytool','bkups', timestamp)
print(backup_dir)
os.makedirs(backup_dir)

# Connect to SQLite database
conn = sqlite3.connect('cpytool\db\database.db')
c = conn.cursor()

# Check if the table exists before deleting
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dirlst'")
if c.fetchone():
    # Clear the SQLite table
    c.execute('DELETE FROM dirlst')
else:
    # Create the SQLite table
    c.execute('''
        CREATE TABLE dirlst (
            "from" TEXT,
            "to" TEXT,
            "backup" TEXT,
            "from_files_count" INTEGER,
            "to_files_count" INTEGER
        )
    ''')
# Populate the SQLite table with CSV data
for index, row in df.iterrows():
    from_files_count = len([f for f in os.listdir(row['from']) if os.path.isfile(os.path.join(row['from'], f))])
    to_files_count = len([f for f in os.listdir(row['to']) if os.path.isfile(os.path.join(row['to'], f))])
    to_pth = row['to'].replace(home_dir, '') if row['to'].startswith(home_dir) else None
    bkp_dr = home_dir+'\\'+backup_dir+''+to_pth
    # print(home_dir+','+backup_dir+','+to_pth+','+bkp_dr)
    c.execute('INSERT INTO dirlst ("from", "to", "backup", "from_files_count", "to_files_count") VALUES (?, ?, ?, ?, ?)', 
              (row['from'], row['to'], bkp_dr, from_files_count, to_files_count))

conn.commit()

# Read data from the table
c.execute('SELECT * FROM dirlst')
data = c.fetchall()

# Substitute home_dir value with "home_dir" in the data
data = [(row[0].replace(home_dir, "<HD>"), row[1].replace(home_dir, "<HD>"), row[2].replace(home_dir, "<HD>"), row[3], row[4]) for row in data]

# Display data using Streamlit with word wrap enabled
st.write(pd.DataFrame(data, columns=['from', 'to', 'backup', 'from_files_count', 'to_files_count']).style.set_properties(**{'white-space': 'pre-wrap'}))

# Create buttons
if st.button('Backup'):
    for row in data:
        from_dir = row[1].replace("<HD>", home_dir)
        bkup_dir = row[2].replace("<HD>", home_dir)
        if not os.path.exists(bkup_dir):
            os.makedirs(bkup_dir)
        for file_name in os.listdir(from_dir):
            from_file = os.path.join(from_dir, file_name)
            to_file = os.path.join(bkup_dir, file_name)
            if os.path.isfile(from_file) and not os.path.exists(to_file):
                shutil.copy2(from_file, to_file)
                st.write(f'Copied {from_file} to {to_file}')
            else:
                st.write(f'Skipped {from_file} (already exists)')
    
    # Zip the backup_dir folder
    zip_dir = os.path.join('cpytool', 'bkups', 'zips')
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
    zip_file = os.path.join(zip_dir, f'{timestamp}.zip')
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=backup_dir)  # Maintain folder structure
                zipf.write(file_path, arcname)
                
    st.write(f'Backup zipped to {zip_file}')
    
    # Ensure all files and directories are closed before deletion
    conn.close()
    
    # Delete all backup folders except the "zips" folder
    for folder in os.listdir(os.path.join('cpytool', 'bkups')):
        print(folder)
        folder_path = os.path.join('cpytool', 'bkups', folder)
        if os.path.isdir(folder_path) and folder != 'zips':
            try:
                # Change the permissions of the folder and its contents
                for root, dirs, files in os.walk(folder_path):
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), 0o777)
                    for file in files:
                        os.chmod(os.path.join(root, file), 0o777)
                shutil.rmtree(folder_path)
                st.write(f'Deleted backup folder {folder_path}')
            except PermissionError as e:
                st.write(f'Error deleting {folder_path}: {e}')

if st.button('Clear'):
    for row in data:
        to_dir = row[1].replace("<HD>", home_dir)
        for file_name in os.listdir(to_dir):
            file_path = os.path.join(to_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                st.write(f'Deleted {file_path}')

if st.button('Copy'):
    for row in data:
        from_dir = row[0].replace("<HD>", home_dir)
        to_dir = row[1].replace("<HD>", home_dir)
        for file_name in os.listdir(from_dir):
            from_file = os.path.join(from_dir, file_name)
            to_file = os.path.join(to_dir, file_name)
            if os.path.isfile(from_file):
                shutil.copy2(from_file, to_file)
                st.write(f'Copied {from_file} to {to_file}')

conn.close()



