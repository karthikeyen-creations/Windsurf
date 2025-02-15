import streamlit as st
import os
from bs4 import BeautifulSoup

st.title('HTML Stitcher')

directory = st.text_input('Enter the directory name:')

if st.button('Start Stitching'):
    if not os.path.isdir(directory):
        st.error('The provided directory does not exist.')
    else:
        combined_html = ''
        first_file = True
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    if first_file:
                        combined_html += str(soup.find('style'))
                        combined_html += str(soup.find('script'))
                        first_file = False
                    combined_html += str(soup.find('body').decode_contents())
        combined_html = f'<html><head>{combined_html}</head><body>{combined_html}</body></html>'
        output_path = os.path.join(directory, 'combined.html')
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(combined_html)
        st.success(f'HTML files have been stitched together and saved to {output_path}')
