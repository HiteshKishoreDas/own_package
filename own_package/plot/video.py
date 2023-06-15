import os


# Creates video using the image_path at video_path
def make_video(image_path, video_path, framerate=5, zfill_n=5, theme="bright"):
    video_command = f"ffmpeg -framerate {framerate} -i "
    video_command += f"{image_path}_%0{zfill_n}d.png "

    if theme == "bright":
        video_command += f'-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2, fps=25, format=yuv420p" '
    elif theme == "dark":
        video_command += f"-c copy "

    video_command += f"{video_path}.mp4"

    print(f"Command: {video_command}")

    os.system(video_command)
