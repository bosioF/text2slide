import sys
import os
import subprocess
from datetime import datetime
import string
import shutil

def parseslides(filename):
    slides = []
    current_slide = None
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Slide"):
                if current_slide:
                    slides.append(current_slide)
                title = line.split(":", 1)[1].strip() if ":" in line else line
                current_slide = {"Title": title, "Content": ""}
            else:
                if current_slide:
                    current_slide["Content"] += line + "\n"
        if current_slide:
            slides.append(current_slide)
    return slides

def generate_scene_code(slides, output_name):
    code = f"""
from manim import *

class ToAnim(Scene):
    def construct(self):
"""
    for i, slide in enumerate(slides):
        title = slides[i]['Title'].replace('"', '\\"')
        content = slides[i]['Content'].replace('"', '\\"').replace('\n', '\\n')
        code += f"""
        title = Text("{title}").to_edge(UP)
        content = Text("{content}").next_to(title, DOWN)
        self.play(Write(title))
        self.wait(1)
        self.play(Write(content))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(content))
"""
    with open("temp_scene.py", "w", encoding="utf-8") as f:
        f.write(code)

    return "temp_scene.py"

def render_with_manim(scene_file, output_file_name, quality):
    output_path = f"manim_files/{output_file_name}.mp4"
    cmd = [
        "manim",
        f"{quality}",               # quality: -ql (low), -qm (medium), -qk (4K)
        "--disable_caching",
        "--media_dir", "manim_files",
        "--output_file", output_file_name,
        scene_file,
        "ToAnim"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python text2slide.py input.txt <Quality> <OutputFileName>")
        sys.exit(1)
    if sys.argv[2] not in ['-ql', '-qm', '-qh', '-qp', '-qk']:
        print('Quality options: -ql (low), -qm (medium), -qh (high), -qp (2K), -qk (4K)')
        sys.exit(1)
    if sys.argv[3].startswith('.'):
        print('Invalid output file name')
        sys.exit(1)
    allowed_chars = string.ascii_letters + string.digits + "-_"
    if any(c not in allowed_chars for c in sys.argv[3]):
        print("Invalid output file name. Only letters, digits, '-' and '_' allowed.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file_name = sys.argv[3]
    quality = sys.argv[2]
    
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

    slides = parseslides(input_file)
    scene_file = generate_scene_code(slides, output_file_name)
    render_with_manim(scene_file, output_file_name, quality)
    video_dir = f"manim_files/videos/temp_scene/{dir_name}/{output_file_name}.mp4"
    if not os.path.exists(video_dir):
        print(f"Errore: Il file {video_dir} non esiste. Il rendering potrebbe essere fallito.")
        sys.exit(1)
    final_path = f"output/{output_file_name}.mp4"
    shutil.move(video_dir, final_path)
    temp_scene_dir = f"manim_files/videos/temp_scene"
    if os.path.exists(temp_scene_dir):
        shutil.rmtree(temp_scene_dir)  
    os.remove(scene_file)
    print(f"\nVideo generato in: {final_path}")
