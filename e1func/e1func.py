import streamlit as st
import os
import csv
from datetime import datetime

# Set the app layout to wide
st.set_page_config(layout="wide")

def get_directories_from_csv(csv_content):
    directories = []
    csv_file = csv_content.strip().split('\n')
    for row in csv_file:
        directories.append(row.strip())
    return directories

def list_files(directories):
    file_list = []
    for directory in directories:
        st.subheader(f"Files in {directory}")
        try:
            files = os.listdir(directory)
            for file in files:
                st.write(file)
                file_list.append({
                    "DIR": directory,
                    "FN": os.path.splitext(file)[0],
                    "FNE": file,
                    "FRP": os.path.join(directory, file),
                    "SEL": "N"
                })
        except FileNotFoundError:
            st.error(f"Directory not found: {directory}")
        except NotADirectoryError:
            st.error(f"Not a directory: {directory}")
    return file_list

def save_file_list(file_list, filepath):
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ["DIR", "FN", "FNE", "FRP", "SEL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in file_list:
            writer.writerow(file)

def get_latest_file_sel_values(directory):
    files = os.listdir(directory)
    csv_files = [f for f in files if f.startswith('filst') and f.endswith('.csv')]
    if not csv_files:
        return {}
    
    def extract_timestamp(filename):
        try:
            return datetime.strptime(filename[5:-4], "%Y%m%d%H%M%S")
        except ValueError:
            return None
    
    csv_files = [f for f in csv_files if extract_timestamp(f) is not None]
    if not csv_files:
        return {}
    
    latest_file = max(csv_files, key=extract_timestamp)
    sel_values = {}
    with open(os.path.join(directory, latest_file), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sel_values[row['FRP']] = row['SEL']
    return sel_values

st.title("Directory File Lister")

csv_content = """SQLcheck\\columns
SQLcheck\\sample\\pg"""

directories = get_directories_from_csv(csv_content)

edited_directories = st.text_area("Edit Directories", value="\n".join(directories), height=100)

if st.button("List Files"):
    directories = get_directories_from_csv(edited_directories)
    
    # Save the edited directories to 'e1func/workfiles/dirlst.csv'
    with open('e1func/workfiles/dirlst.csv', 'w') as file:
        file.write(edited_directories)
    
    file_list = list_files(directories)
    
    # Get SEL values from the latest file
    sel_values = get_latest_file_sel_values('e1func/workfiles')
    for file in file_list:
        file['SEL'] = sel_values.get(file['FRP'], 'N')
    
    # Save the file list to a new file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    save_file_list(file_list, f'e1func/workfiles/filst{timestamp}.csv')
