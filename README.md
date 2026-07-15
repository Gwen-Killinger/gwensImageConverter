# Gwen's Image Converter

Gwen's Image Converter is a small, interactive command-line app for converting
images between PNG, JPEG, and WebP. It processes every supported image in a
folder and places the converted files in an output folder of your choice.

## Features

- Converts a folder of images to PNG, JPEG, or WebP
- Creates the output folder when it does not exist
- Shows conversion progress as a percentage
- Skips existing output files instead of overwriting them
- Corrects image orientation using EXIF metadata
- Preserves EXIF and color-profile metadata when supported
- Converts transparent images to JPEG by placing them on a white background
- Uses JPEG quality 90 with optimization enabled
- Ignores files that are not recognized image types

Animated images are currently converted using only their first frame.

## Running the Linux executable

The prebuilt Linux executable is located at `dist/GwensImageConverter`.

Open a terminal in the project folder and run:

```bash
chmod +x dist/GwensImageConverter
./dist/GwensImageConverter
```

The executable includes Python and Pillow, so they do not need to be installed
separately.

## How to use the app

1. Choose the desired output format:
   - `1` for PNG
   - `2` for JPEG
   - `3` for WebP
2. Enter the path to the folder containing the source images.
3. Enter the path where converted images should be saved.
4. Wait for the progress display to reach 100%.

Example paths on Linux:

```text
Enter the path to the folder containing the images: /home/gwen/Pictures/input
Enter the path to the output folder: /home/gwen/Pictures/converted
```

Example progress output:

```text
[ 50.00%] Converted photo-one.png -> /home/gwen/Pictures/converted/photo-one.jpg
[100.00%] Converted photo-two.png -> /home/gwen/Pictures/converted/photo-two.jpg
```

If an output file already exists, the app skips it to avoid replacing it.

## Running from Python source

The source version requires Python 3 and Pillow. With `main.py` in the project
folder, create a virtual environment and install Pillow:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install Pillow
python3 main.py
```

## Building an executable

Install PyInstaller in the virtual environment and build a single-file app:

```bash
python3 -m pip install PyInstaller
python3 -m PyInstaller --onefile --name GwensImageConverter main.py
```

The resulting executable will be placed in `dist/`.

PyInstaller executables are platform-specific. A Linux build runs on compatible
Linux systems; it does not become a Windows program simply by giving it an
`.exe` extension. To create `GwensImageConverter.exe`, run the PyInstaller build
on Windows (or use a Windows virtual machine or Windows CI runner).

## Notes

- JPEG does not support transparency. Transparent areas are filled with white.
- The sending and receiving computers must use compatible operating systems and
  CPU architectures.
- Windows may show a SmartScreen warning for an unsigned personal executable.
- Keep backups of important images, even though the app avoids overwriting
  existing output files.
