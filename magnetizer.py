import os
import bencodepy
import hashlib
import base64
import tkinter as tk
from tkinter import filedialog
import csv


def is_torrent_file(filename):
    return filename.endswith(".torrent")

def make_magnet_from_file(file_path):
    try:
        metadata = bencodepy.decode_from_file(file_path)
        info = metadata.get(b'info') or metadata.get('info')
        if not info:
            raise ValueError("Missing 'info' in torrent metadata")

        hashcontents = bencodepy.encode(info)
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest).decode()

        magnet_link = 'magnet:?xt=urn:btih:' + b32hash

        name = info.get(b'name') or info.get('name', 'unknown')
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        magnet_link += '&dn=' + name

        announce_url = metadata.get(b'announce') or metadata.get('announce')
        if announce_url:
            if isinstance(announce_url, bytes):
                announce_url = announce_url.decode('utf-8')
            magnet_link += '&tr=' + announce_url

        # Handle both single file and multiple files cases for 'length'
        if b'length' in info or 'length' in info:
            length = info.get(b'length') or info.get('length')
            magnet_link += '&xl=' + str(length)
        elif b'files' in info or 'files' in info:
            files = info.get(b'files') or info.get('files', [])
            total_length = sum(file.get('length', 0) for file in files)
            magnet_link += '&xl=' + str(total_length)

        return magnet_link
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def process_files(file_paths):
    if len(file_paths) == 1:
        # If it's a single file, output the magnet link directly
        magnet_link = make_magnet_from_file(file_paths[0])
        if magnet_link:
            print("Magnet link:", magnet_link)
    else:
        # Process multiple files and write to .txt and .csv files
        txt_output_file = "magnet_links.txt"
        csv_output_file = "magnet_links.csv"

        with open(txt_output_file, "w") as txt_file, open(csv_output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "Magnet Link"])  # CSV Header

            for file_path in file_paths:
                magnet_link = make_magnet_from_file(file_path)
                if magnet_link:
                    filename = os.path.basename(file_path)
                    txt_file.write(magnet_link + "\n")
                    csv_writer.writerow([filename, magnet_link])

        print(f"Magnet links have been written to {txt_output_file} and {csv_output_file}")

def select_folder_or_file():
    root = tk.Tk()
    root.withdraw()  # Hides the main window

    # Ask the user whether to select a file or folder
    file_or_folder = input("Type 'file' to select a file, or 'folder' to select a folder: ").lower()
    if file_or_folder == 'file':
        file_path = filedialog.askopenfilename(filetypes=[("Torrent files", "*.torrent")])
        if file_path:
            return [file_path]
    elif file_or_folder == 'folder':
        folder_path = filedialog.askdirectory()
        if folder_path:
            return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if is_torrent_file(f)]

    root.destroy()
    return []

if __name__ == "__main__":
    paths = select_folder_or_file()
    if paths:
        process_files(paths)
    else:
        print("No file or folder selected.")