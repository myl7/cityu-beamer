#!/usr/bin/env python3

import os
import argparse
import shutil
from pathlib import Path

def rename_images_by_creation_date(image_dir='images'):
    """
    Rename all files in the given directory by their creation date.
    New names will be in the format image1.ext, image2.ext, etc.
    
    Args:
        image_dir (str): Path to the directory containing images. Defaults to 'images'.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        print(f"Created directory: {image_dir}")
        return
    
    # Get all files in the directory
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
             if os.path.isfile(os.path.join(image_dir, f))]
    
    if not files:
        print(f"No files found in {image_dir}")
        return
    
    # Sort files by creation time
    files.sort(key=lambda x: os.path.getctime(x))
    
    # Rename files
    for i, file_path in enumerate(files, 1):
        # Get file extension
        _, ext = os.path.splitext(file_path)
        
        # Create new file name
        new_name = os.path.join(image_dir, f"image{i}{ext}")
        
        # Skip if the file already has the target name
        if file_path == new_name:
            continue
        
        # Check if target file already exists
        if os.path.exists(new_name):
            print(f"Warning: {new_name} already exists, skipping rename of {file_path}")
            continue
        
        # Rename file
        try:
            shutil.move(file_path, new_name)
            print(f"Renamed: {os.path.basename(file_path)} -> {os.path.basename(new_name)}")
        except Exception as e:
            print(f"Error renaming {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Rename image files by creation date.')
    parser.add_argument('--image_dir', type=str, default='images',
                        help='Directory containing image files (default: images)')
    
    args = parser.parse_args()
    
    rename_images_by_creation_date(args.image_dir)
    
if __name__ == "__main__":
    main()

