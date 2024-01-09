
# Magnetizer

Magnetizer is a Python script that generates magnet links from `.torrent` files. It can process both individual torrent files and directories containing multiple torrent files. For a single file, it outputs the magnet link directly in the command line interface. For a directory, it saves the magnet links to both a `.txt` and a `.csv` file.

## Requirements

- Python 3.x
- bencodepy
- tkinter (usually comes pre-installed with Python)

## Install bencodepy

Install the `bencodepy` package. You can install it using pip:

```bash
pip install bencodepy
```

## Usage

1. Run the script using Python:

   ```bash
   python Magnetizer.py
   ```

2. The script will prompt you to choose between processing a single file or a folder:
    - Type `file` to select an individual `.torrent` file.
    - Type `folder` to select a folder containing multiple `.torrent` files.

3. Depending on your choice, a file dialog window will open. Select the file or folder as required.

4. If you selected:
    - A single file, the magnet link will be displayed in the CLI.
    - A folder, the magnet links for all `.torrent` files in the folder will be saved in `magnet_links.txt` and `magnet_links.csv`.
