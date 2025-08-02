from backend import *

if __name__ == "__main__":
    input_file, quality, output_file_name, audio_path = check_input()
    color = input("What color should the text be?").strip().upper()
    dir_name = check_input(color, quality)
    process_video(input_file, color, output_file_name, quality, dir_name, audio_path)

