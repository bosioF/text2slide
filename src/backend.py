import subprocess
import sys
import string
from audio import *
from help import *

sys.tracebacklimit = 0
QUALITY_FLAGS = ['-ql', '-qm', '-qh', '-qp', '-qk']

quality_to_dirName = {
    "-ql": "480p15",
    "-qm": "720p60",
    "-qh": "1080p60",
    "-qp": "1440p60",
    "-qk": "2160p60"
}

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

    if not _slides:
        raise ValueError("No slides found in the input file.")
    for i, slide in enumerate(_slides):
        if not slide["Title"].strip():
            raise ValueError(f"Slide {i + 1} is missing a title.")
        if not slide["Content"].strip():
            raise ValueError(f"Slide {i + 1} is missing content.")
    return _slides

def generate_scene_code(__slides, color):
    code = f"""
from manim import *

class ToAnim(Scene):
    def construct(self):
"""
    for slide in __slides:
        title = slide['Title'].replace('"', '\\"')
        content = slide['Content'].replace('"', '\\"').replace('\n', '\\n')
        code += f"""
        title = Text(\"{title}\", color={color}).to_edge(UP)
        content = Text(\"{content}\", color={color}).next_to(title, DOWN)
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
    prepare_output_dirs()
    scene_file = generate_scene_code(slides, color)
    render_with_manim(scene_file, output_file_name, quality)
    video_dir = f"manim_files/videos/temp_scene/{dir_name}/{output_file_name}.mp4"
    if not os.path.exists(video_dir):
        raise FileNotFoundError(f"Error: {video_dir} doesn't exist. Rendering may have failed.")
    final_path = f"output/{output_file_name}.mp4"
    shutil.move(video_dir, final_path)
    temp_scene_dir = f"manim_files/videos/temp_scene"
    if os.path.exists(temp_scene_dir):
        shutil.rmtree(temp_scene_dir)
    os.remove(scene_file)
    add_audio_to_video(final_path, audio_path)
    print(f"\nVideo generated at: {final_path}")

def parse_cli_args():
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
    check_args(input_file, quality, output_file_name)
    return input_file, quality, output_file_name, audio_path

def check_args(input_file, quality, output_file_name):
    if not os.path.isfile(input_file):
        raise ValueError("Input file does not exist")
    if quality not in QUALITY_FLAGS:
        raise ValueError(f"Invalid quality. Use one of: {', '.join(QUALITY_FLAGS)}")
    allowed_chars = string.ascii_letters + string.digits + "-_"
    if output_file_name.startswith('.') or any(c not in allowed_chars for c in output_file_name):
        raise ValueError("Invalid output file name. Use only letters, digits, '-' and '_'.")

def prepare_output_dirs():
    os.makedirs("manim_files", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def get_dir_name(quality):
    return quality_to_dirName.get(quality)

def validate_color(color):
    if color not in COLOR_NAMES:
        raise ValueError(f"{color} is not an available color")