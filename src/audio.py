import os
import shutil
import time
from moviepy.editor import VideoFileClip, AudioFileClip

def add_audio_to_video(final_path, audio_path):
    if not audio_path:
        return False

    for _ in range(10):
        if os.path.exists(final_path) and os.path.getsize(final_path) > 1000:
            break
        time.sleep(0.5)

    try:
        video = VideoFileClip(final_path)
        audio = AudioFileClip(audio_path)

        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)

        final = video.set_audio(audio)
        final_with_audio_path = final_path.replace(".mp4", "_with_audio.mp4")
        final.write_videofile(final_with_audio_path, codec="libx264", audio_codec="aac")

        os.remove(final_path)
        shutil.move(final_with_audio_path, final_path)
        print("Audio added successfully.")
        return True

    except Exception as e:
        print(f"Failed to add audio: {e}")
        return False