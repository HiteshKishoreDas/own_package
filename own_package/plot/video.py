import os

# Creates video using the image_path at video_path
def make_video(image_path, video_path):

    video_command  = f'ffmpeg -framerate 5 -i '
    video_command += f'{image_path}_%05d.png'
    video_command += f'-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2, fps=25, format=yuv420p"'
    video_command += f'{video_path}.mp4'
    
    os.system(video_command)