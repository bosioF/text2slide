import os
import subprocess
import shutil
import sys
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

def generate_scene_code(__slides):
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

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("""\
Usage: python text2slide.py input.txt <Quality> <OutputFileName>

Quality flags:
-ql\t480p 15fps
-qm\t720p 60fps
-qh\t1080p 60fps
-qp\t1440p 60fps
-qk\t2160p 60fps

Available colors:

Basic:
    BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PINK, PURPLE, TEAL, GOLD, MAROON, GRAY, GREY

Variants (use with base names):
    *_A, *_B, *_C, *_D, *_E
    Example: RED_A, GREEN_E, BLUE_C, GOLD_D

Shades:
    DARK_GRAY, DARK_GREY, DARKER_GRAY, DARKER_GREY, DARK_BLUE, DARK_BROWN,
    LIGHT_GRAY, LIGHT_GREY, LIGHTER_GRAY, LIGHTER_GREY, LIGHT_BROWN, LIGHT_PINK

Grays:
    GRAY_A, GRAY_B, GRAY_C, GRAY_D, GRAY_E, GRAY_BROWN,
    GREY_A, GREY_B, GREY_C, GREY_D, GREY_E, GREY_BROWN

Logo colors:
    LOGO_BLACK, LOGO_WHITE, LOGO_RED, LOGO_GREEN, LOGO_BLUE

Pure RGB:
    PURE_RED (#FF0000), PURE_GREEN (#00FF00), PURE_BLUE (#0000FF)

Use any color name as shown above. Names are case-sensitive.""")
        sys.exit(0)

    if len(sys.argv) != 4:
        print("Usage: python text2slide.py input.txt <Quality> <OutputFileName> OR --help")
        sys.exit(1)

    input_file = sys.argv[1]
    quality = sys.argv[2]
    output_file_name = sys.argv[3]

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

    color = input("What color should the text be?")
    color_names = [
        "BLACK",
        "BLUE",
        "BLUE_A",
        "BLUE_B",
        "BLUE_C",
        "BLUE_D",
        "BLUE_E",
        "DARKER_GRAY",
        "DARKER_GREY",
        "DARK_BLUE",
        "DARK_BROWN",
        "DARK_GRAY",
        "DARK_GREY",
        "GOLD",
        "GOLD_A",
        "GOLD_B",
        "GOLD_C",
        "GOLD_D",
        "GOLD_E",
        "GRAY",
        "GRAY_A",
        "GRAY_B",
        "GRAY_BROWN",
        "GRAY_C",
        "GRAY_D",
        "GRAY_E",
        "GREEN",
        "GREEN_A",
        "GREEN_B",
        "GREEN_C",
        "GREEN_D",
        "GREEN_E",
        "GREY",
        "GREY_A",
        "GREY_B",
        "GREY_BROWN",
        "GREY_C",
        "GREY_D",
        "GREY_E",
        "LIGHTER_GRAY",
        "LIGHTER_GREY",
        "LIGHT_BROWN",
        "LIGHT_GRAY",
        "LIGHT_GREY",
        "LIGHT_PINK",
        "LOGO_BLACK",
        "LOGO_BLUE",
        "LOGO_GREEN",
        "LOGO_RED",
        "LOGO_WHITE",
        "MAROON",
        "MAROON_A",
        "MAROON_B",
        "MAROON_C",
        "MAROON_D",
        "MAROON_E",
        "ORANGE",
        "PINK",
        "PURE_BLUE",
        "PURE_GREEN",
        "PURE_RED",
        "PURPLE",
        "PURPLE_A",
        "PURPLE_B",
        "PURPLE_C",
        "PURPLE_D",
        "PURPLE_E",
        "RED",
        "RED_A",
        "RED_B",
        "RED_C",
        "RED_D",
        "RED_E",
        "TEAL",
        "TEAL_A",
        "TEAL_B",
        "TEAL_C",
        "TEAL_D",
        "TEAL_E",
        "WHITE",
        "YELLOW",
        "YELLOW_A",
        "YELLOW_B",
        "YELLOW_C",
        "YELLOW_D",
        "YELLOW_E"
    ]

    if color.strip() not in color_names:
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
    scene_file = generate_scene_code(slides)
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
    print(f"\nVideo generated at: {final_path}")
