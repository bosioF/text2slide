import subprocess

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