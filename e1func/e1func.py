import streamlit as st
import os
import csv
from datetime import datetime

# Set the app layout to wide and apply a colorful, professional theme suitable for dark mode
st.set_page_config(
    layout="wide",
    page_title="Directory File Lister",
    page_icon="📁",
    initial_sidebar_state="expanded"
)

# Apply custom theme settings
st.markdown("""
    <style>
        .css-18e3th9 {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .css-1d391kg {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .css-1v3fvcr {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .css-1cpxqw2 {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .css-1aumxhk {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .css-1d391kg .stButton button {
            background-color: #4CAF50;
            color: #ffffff;
        }
        .css-1d391kg .stTextArea textarea {
            background-color: #333333;
            color: #ffffff;
        }
        .css-1d391kg .stTextInput input {
            background-color: #333333;
            color: #ffffff;
        }
        .css-1d391kg .stSelectbox select {
            background-color: #333333;
            color: #ffffff;
        }
        .css-1d391kg .stCheckbox div {
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

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
    return sel_values, latest_file

def update_sel_values(filepath, updated_sel_values):
    rows = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['FRP'] in updated_sel_values:
                row['SEL'] = updated_sel_values[row['FRP']]
            rows.append(row)
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ["DIR", "FN", "FNE", "FRP", "SEL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def update_temp_list(directory, index, new_sel):
    for dir_name, files in st.session_state.temp_list:
        if dir_name == directory:
            files[index] = (files[index][0], new_sel)
            break
    st.session_state.temp_list = st.session_state.temp_list

st.title("Directory File Lister")

tab1, tab2, tab3 = st.tabs(["List Files", "Manage Selections", "Selected Files"])

with tab1:
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
        sel_values, latest_file = get_latest_file_sel_values('e1func/workfiles')
        for file in file_list:
            file['SEL'] = sel_values.get(file['FRP'], 'N')
        
        # Save the file list to a new file with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_file_list(file_list, f'e1func/workfiles/filst{timestamp}.csv')

with tab2:
    if 'temp_list' not in st.session_state:
        sel_values, latest_file = get_latest_file_sel_values('e1func/workfiles')
        directories = {}
        for frp, sel in sel_values.items():
            directory = os.path.dirname(frp)
            if directory not in directories:
                directories[directory] = []
            directories[directory].append((os.path.basename(frp), sel))
        
        st.session_state.temp_list = [(directory, files) for directory, files in directories.items()]
    
    temp_list = st.session_state.temp_list
    
    for directory, files in temp_list:
        st.subheader(directory)
        for i, (filename, sel) in enumerate(files):
            selected = st.checkbox(filename, value=(sel == 'Y'), 
                                   on_change=update_temp_list, args=(directory, i, 'Y' if sel == 'N' else 'N'))
        
        col1, col2, col3 = st.columns(3)
        if col1.button(f"Select All in {directory}"):
            for i, (filename, _) in enumerate(files):
                files[i] = (filename, 'Y')
            st.session_state.temp_list = temp_list
            st.rerun()
        if col2.button(f"Deselect All in {directory}"):
            for i, (filename, _) in enumerate(files):
                files[i] = (filename, 'N')
            st.session_state.temp_list = temp_list
            st.rerun()
        if col3.button(f"Invert Selection in {directory}"):
            for i, (filename, sel) in enumerate(files):
                files[i] = (filename, 'N' if sel == 'Y' else 'Y')
            st.session_state.temp_list = temp_list
            st.rerun()
    
    if st.button("Update Selections"):
        updated_sel_values = {os.path.join(directory, filename): sel for directory, files in temp_list for filename, sel in files}
        sel_values, latest_file = get_latest_file_sel_values('e1func/workfiles')
        update_sel_values(os.path.join('e1func/workfiles', latest_file), updated_sel_values)
        st.success("Selections updated successfully!")
        st.rerun()  # Trigger a rerun

with tab3:
    sel_values, latest_file = get_latest_file_sel_values('e1func/workfiles')
    st.subheader(f"Selected Files from {latest_file}")
    
    selected_files = [frp for frp, sel in sel_values.items() if sel == 'Y']
    
    if selected_files:
        combined_content = ""
        for frp in selected_files:
            st.write(frp)
            with open(frp, 'r') as file:
                combined_content += file.read() + "\n"
        st.text_area("Combined Content", value=combined_content, height=300)
        
        if st.button("Create Combined File"):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            combined_filepath = f'e1func/workfiles/func{timestamp}.sql'
            with open(combined_filepath, 'w') as combined_file:
                combined_file.write(combined_content)
            st.success(f"Combined file created: {combined_filepath}")
    else:
        st.write("No files selected.")
