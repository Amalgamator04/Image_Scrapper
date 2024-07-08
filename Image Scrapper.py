# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 08:19:50 2024

@author: HP
"""
import os
import zipfile
from PIL import Image
from icrawler.builtin import GoogleImageCrawler
import streamlit as st

def download_images(query, num_images, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    google_crawler.crawl(keyword=query, max_num=num_images)

def resize_images(output_dir, width, height):
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img = img.resize((width, height), Image.ANTIALIAS)
                    img.save(file_path)
            except Exception as e:
                print(f"Error resizing image {file_path}: {e}")

def create_zip_file(output_dir, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), output_dir))

def main():
    st.title("Image Downloader and Resizer")
    
    query = st.text_input("Enter the search term for the images:")
    num_images = st.number_input("Enter the number of images to download:", min_value=1, max_value=1000, value=10)
    width = st.number_input("Enter the desired width for the images:", min_value=1, value=300)
    height = st.number_input("Enter the desired height for the images:", min_value=1, value=300)
    zip_filename = st.text_input("Enter the desired name for the zip file (without .zip extension):") + '.zip'
    
    if st.button("Download and Process Images"):
        if query and zip_filename:
            base_output_dir = 'downloaded_images'
            specific_output_dir = os.path.join(base_output_dir, query.replace(' ', '_'))
            
            st.write(f"Downloading {num_images} images for the query '{query}'...")
            download_images(query, num_images, specific_output_dir)
            
            st.write(f"Resizing images to {width}x{height}...")
            resize_images(specific_output_dir, width, height)
            
            st.write(f"Creating zip file '{zip_filename}'...")
            create_zip_file(specific_output_dir, zip_filename)
            
            st.write(f"Zip file '{zip_filename}' created successfully.")
            
            # Provide a link to download the zip file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download Zip File",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )
            
            # Clean up the downloaded images directory if needed
            # import shutil
            # shutil.rmtree(specific_output_dir)
        else:
            st.write("Please provide both a search term and a zip file name.")

if __name__ == "__main__":
    main()


