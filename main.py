from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError


OUTPUT_FORMATS = {
    "1": ("PNG", ".png"),
    "2": ("JPEG", ".jpg"),
    "3": ("WEBP", ".webp"),
}

WELCOME_BANNER = r"""
  .-----------------------------------------------.
  |                                               |
  |       _____                       _           |
  |      / ____|                     ( )          |
  |     | |  __ __      _____ _ __   |/ ___       |
  |     | | |_ |\ \ /\ / / _ \ '_ \    / __|      |
  |     | |__| |\ V  V /  __/ | | |   \__ \       |
  |      \_____| \_/\_/ \___|_| |_|   |___/       |
  |                                               |
  |        I M A G E   C O N V E R T E R          |
  |                                               |
  |         [ PNG ] -> [ JPG ] -> [ WEBP ]        |
  |                                               |
  '-----------------------------------------------'
"""


def prepare_for_jpeg(image):
    """Flatten transparency and return an RGB image suitable for JPEG."""
    has_alpha = image.mode in ("RGBA", "LA") or "transparency" in image.info

    if has_alpha:
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        return background

    return image.convert("RGB")


def get_existing_directory(prompt):
    while True:
        path = Path(input(prompt).strip()).expanduser()
        if path.is_dir():
            return path
        print(f"Folder does not exist: {path}")


def convert_image(infile, outfile, output_format):
    with Image.open(infile) as image:
        if getattr(image, "is_animated", False):
            print(f"Note: {infile.name} is animated; only its first frame will be saved.")
            image.seek(0)

        icc_profile = image.info.get("icc_profile")
        image = ImageOps.exif_transpose(image)
        save_options = {}

        exif = image.getexif()
        if exif:
            save_options["exif"] = exif.tobytes()
        if icc_profile:
            save_options["icc_profile"] = icc_profile

        if output_format == "JPEG":
            image = prepare_for_jpeg(image)
            save_options.update(quality=90, optimize=True)

        image.save(outfile, format=output_format, **save_options)


def main():
    print(WELCOME_BANNER)
    print("ctrl+c to exit at any time.")
    print("Please choose which file type you would like to convert your image to:")
    print("---------------------------------------------------")
    print("1. PNG")
    print("2. JPEG")
    print("3. WEBP")

    while True:
        user_choice = input("Enter the number of your choice: ").strip()
        if user_choice in OUTPUT_FORMATS:
            break
        print("Please enter 1, 2, or 3.")

    folder_path = get_existing_directory(
        "Enter the path to the folder containing the images: "
    )
    output_folder = Path(
        input("Enter the path to the output folder: ").strip()
    ).expanduser()
    output_folder.mkdir(parents=True, exist_ok=True)

    output_format, extension = OUTPUT_FORMATS[user_choice]

    supported_extensions = {
        suffix.lower() for suffix in Image.registered_extensions()
    }
    input_files = sorted(
        path
        for path in folder_path.iterdir()
        if path.is_file() and path.suffix.lower() in supported_extensions
    )
    total_files = len(input_files)

    if not input_files:
        print("No files found in the input folder.")
        return

    for file_number, infile in enumerate(input_files, start=1):
        percent_done = file_number / total_files * 100
        progress = f"[{percent_done:6.2f}%]"

        outfile = output_folder / f"{infile.stem}{extension}"
        if outfile.exists():
            print(f"{progress} Skipping {infile.name}: {outfile.name} already exists.")
            continue

        try:
            convert_image(infile, outfile, output_format)
            print(f"{progress} Converted {infile.name} -> {outfile}")
        except (OSError, UnidentifiedImageError) as error:
            print(f"{progress} Cannot convert {infile}: {error}")


if __name__ == "__main__":
    main()
