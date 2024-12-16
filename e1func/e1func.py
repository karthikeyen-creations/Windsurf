import streamlit as st
import os
import csv
from datetime import datetime

# Set the app layout to wide and apply a colorful, professional theme suitable for dark mode
st.set_page_config(
    layout="wide",
    page_title="Functions Consolidator",
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
            background-color: #006400;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-size: 16px;
            cursor: pointer;
        }
        .css-1d391kg .stButton button:hover {
            background-color: #228B22;
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
        .stTabs [role="tab"] {
            background-color: #4B0082;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-size: 16px;
            cursor: pointer;
        }
        .stTabs [role="tab"]:hover {
            background-color: #551A8B;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #8A2BE2;
            color: #ffffff;
        }
        .stTabs [role="tab"][aria-selected="true"]:hover {
            background-color: #7B68EE;
        }
        .stTabs [role="tab"]:focus {
            outline: none;
        }
    </style>
""", unsafe_allow_html=True)

def get_directories_from_csv(filepath):
    directories = []
    with open(filepath, 'r') as file:
        csv_file = file.read().strip().split('\n')
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

def list_directories(directory):
    all_directories = []
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            all_directories.append(os.path.relpath(os.path.join(root, d), directory))
    return all_directories

def get_function_name(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip().startswith("CREATE OR REPLACE FUNCTION"):
                return line.strip().split()[4].split('(')[0]
    return ""

def check_grant_execute(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if "GRANT EXECUTE" in line:
                return True
    return False

st.title("Directory File Lister")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["List Directories", "List Files", "Manage Selections", "Generate Combined File", "Grant Access"])

with tab1:
    base_directory = st.text_input("Base Directory", value=".")
    if st.button("List Directories"):
        directories = list_directories(base_directory)
        if directories:
            st.write("Directories:")
            for directory in directories:
                st.write(os.path.join(base_directory, directory))
        else:
            st.write("No directories found.")

with tab2:
    csv_content = get_directories_from_csv('e1func/workfiles/dirlst.csv')
    
    edited_directories = st.text_area("Edit Directories", value="\n".join(csv_content), height=100)
    
    if st.button("List Files"):
        directories = edited_directories.strip().split('\n')
        
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

with tab3:
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

with tab4:
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

with tab5:
    sel_values, latest_file = get_latest_file_sel_values('e1func/workfiles')
    st.subheader(f"Grant Access for Selected Files from {latest_file}")
    
    selected_files = [frp for frp, sel in sel_values.items() if sel == 'Y']
    
    if selected_files:
        grant_access_list = []
        for frp in selected_files:
            function_name = get_function_name(frp)
            has_grant_execute = check_grant_execute(frp)
            grant_access_list.append((frp, function_name, has_grant_execute))
        
        st.write("Selected Files with Grant Access Information:")
        for frp, function_name, has_grant_execute in grant_access_list:
            st.write(f"{frp} | {function_name} | {'Yes' if has_grant_execute else 'No'}")
    else:
        st.write("No files selected.")
