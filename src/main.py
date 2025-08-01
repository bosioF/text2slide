import string
import sys
from help import *
from backend import *
from audio import *

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print(HELP_MSG)
        sys.exit(0)

    if len(sys.argv) not in [4, 5]:
        print(USAGE_MSG)
        print("\nOptionally, provide an MP3 path as a 4th argument.")
        sys.exit(1)

    input_file = sys.argv[1]
    quality = sys.argv[2]
    output_file_name = sys.argv[3]
    audio_path = sys.argv[4] if len(sys.argv) == 5 else None

    if quality not in ['-ql', '-qm', '-qh', '-qp', '-qk']:
        print('Quality options: -ql (low), -qm (medium), -qh (high), -qp (2K), -qk (4K)')
        sys.exit(1)

    if output_file_name.startswith('.'):
        print('Invalid output file name')
        sys.exit(1)

    allowed_chars = string.ascii_letters + string.digits + "-_"
    if any(c not in allowed_chars for c in output_file_name):
        print("Invalid output file name. Only letters, digits, '-' and '_' allowed.")
        sys.exit(1)

    color = input("What color should the text be?").strip().upper()

    if color not in COLOR_NAMES:
        print(f'{color} is not an available color')
        sys.exit(1)

    quality_to_dirName = {
    "-ql": "480p15",  # 854x480 15FPS
    "-qm": "720p60",  # 1280x720 30FPS
    "-qh": "1080p60",  # 1920x1080 60FPS
    "-qp": "1440p60",  # 2560x1440 60FPS
    "-qk": "2160p60"   # 3840x2160 60FPS
    }

    dir_name = quality_to_dirName.get(quality)

    if not os.path.exists("manim_files"):
        os.mkdir("manim_files")

    if not os.path.exists("output"):
        os.mkdir("output")

    slides = parse_slides(input_file)
    scene_file = generate_scene_code(slides, color)
    render_with_manim(scene_file, output_file_name, quality)
    video_dir = f"manim_files/videos/temp_scene/{dir_name}/{output_file_name}.mp4"
    if not os.path.exists(video_dir):
        print(f"Error: {video_dir} doesn't exist. Rendering may have failed.")
        sys.exit(1)
    final_path = f"output/{output_file_name}.mp4"
    shutil.move(video_dir, final_path)
    temp_scene_dir = f"manim_files/videos/temp_scene"
    if os.path.exists(temp_scene_dir):
        shutil.rmtree(temp_scene_dir)  
    os.remove(scene_file)
    add_audio_to_video(final_path, audio_path)
    print(f"\nVideo generated at: {final_path}")
