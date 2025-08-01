from backend import *
from audio import *

if __name__ == "__main__":
    input_file, quality, output_file_name, audio_path = check_input()

    color = input("What color should the text be?").strip().upper()

    if color not in COLOR_NAMES:
        print(f'{color} is not an available color')
        sys.exit(1)

    quality_to_dirName = {
        "-ql": "480p15",
        "-qm": "720p60",
        "-qh": "1080p60",
        "-qp": "1440p60",
        "-qk": "2160p60"
    }

    dir_name = quality_to_dirName.get(quality)

    if not os.path.exists("manim_files"):
        os.mkdir("manim_files")
    if not os.path.exists("output"):
        os.mkdir("output")

    process_video(input_file, color, output_file_name, quality, dir_name, audio_path)

