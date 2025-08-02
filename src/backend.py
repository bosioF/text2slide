import subprocess
import sys
from audio import *
from help import *
import string

def parse_slides(filename):
    _slides = []
    current_slide = None
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Slide"):
                if current_slide:
                    _slides.append(current_slide)
                title = line.split(":", 1)[1].strip() if ":" in line else line
                current_slide = {"Title": title, "Content": ""}
            else:
                if current_slide:
                    current_slide["Content"] += line + "\n"
        if current_slide:
            _slides.append(current_slide)
    return _slides

def generate_scene_code(__slides, color):
    code = f"""
from manim import *

class ToAnim(Scene):
    def construct(self):
"""
    for i, slide in enumerate(__slides):
        title = __slides[i]['Title'].replace('"', '\\"')
        content = __slides[i]['Content'].replace('"', '\\"').replace('\n', '\\n')
        code += f"""
        title = Text("{title}", color={color}).to_edge(UP)
        content = Text("{content}", color={color}).next_to(title, DOWN)
        self.play(Write(title))
        self.wait(1)
        self.play(Write(content))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(content))
"""
    with open("temp_scene.py", "w", encoding="utf-8") as f:
        f.write(code)

    return "temp_scene.py"

def render_with_manim(_scene_file, output_name, qual):
    cmd = [
        "manim",
        f"{qual}",
        "--disable_caching",
        "--media_dir", "manim_files",
        "--output_file", output_name,
        _scene_file,
        "ToAnim"
    ]
    subprocess.run(cmd)

def process_video(input_file, color, output_file_name, quality, dir_name, audio_path):
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

def check_input(color='', res=''):
    if not color:
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

        return input_file, quality, output_file_name, audio_path
    elif color:
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

        dir_name = quality_to_dirName.get(res)

        if not os.path.exists("manim_files"):
            os.mkdir("manim_files")
        if not os.path.exists("output"):
            os.mkdir("output")

        return dir_name
    return None

