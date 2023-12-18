import numpy as np
import matplotlib.pyplot as plt
import imageio as img
import glob
from PIL import Image, ImageDraw, ImageFont

img_dir = "/afs/mpa/home/hitesh/remote/freya/rho_projection/backup_figs/Trial_5/"

# Use a wildcard pattern to match the input PNG images
image_HD_pattern = f"{img_dir}/HD/*.png"
image_MHD_pattern = f"{img_dir}/MHD/*.png"

# Output video file name
output_video = "combined_video.mp4"

# Frame duration (in seconds)
frame_duration = 0.12

image_HD_paths = sorted(glob.glob(image_HD_pattern))
image_MHD_paths = sorted(glob.glob(image_MHD_pattern))

# # Get the dimensions (height and width) of the images
# image1 = img.imread(image_HD_paths[0])
# height, width, _ = image1.shape

# Initialize an output video writer
writer = img.get_writer(output_video, fps=1.0 / frame_duration)

# Font settings for the text
font_size = 70
font_color = (255, 255, 255)  # White
# font_color = (0, 0, 0)  # White
font = ImageFont.truetype("arial.ttf", font_size)
font2 = ImageFont.truetype("arial.ttf", int(font_size * 0.8))

text_flag = False

# Loop through each image in the series and create a video
for i_mg, image_HD_path in enumerate(image_HD_paths):
    # for i in range(num_frames):
    # Combine the frames side by side

    if i_mg < 450:
        continue
    elif i_mg > 450:
        break

    image_HD = img.imread(image_HD_path)
    image_MHD = img.imread(image_MHD_paths[i_mg])

    for i in range(3):
        image_HD[:, :, i] *= image_HD[:, :, 3] > 5
        image_MHD[:, :, i] *= image_MHD[:, :, 3] > 5

    combined_frame = np.concatenate((image_HD, image_MHD), axis=1)

    # Add text to the top of the frame
    if text_flag:

        frame_pil = Image.fromarray(combined_frame)
        draw = ImageDraw.Draw(frame_pil)
        text = "Without magnetic fields"
        text_width, text_height = draw.textsize(text, font)
        text_position = (150, 10)  # Adjust text position as needed
        draw.text(text_position, text, font=font, fill=font_color)

        text = "With magnetic fields"
        text_width, text_height = draw.textsize(text, font)
        text_position = (1200, 10)  # Adjust text position as needed
        draw.text(text_position, text, font=font, fill=font_color)

        text = "Mixing of a cold dense cloud in a hot, turbulent environment"
        text_width, text_height = draw.textsize(text, font2)
        text_position = (250, 900)  # Adjust text position as needed
        draw.text(text_position, text, font=font2, fill=font_color)

        text = "Multiphase \nGas Group"
        text_width, text_height = draw.textsize(text, font2)
        text_position = (855, 650)  # Adjust text position as needed
        draw.text(text_position, text, font=font2, fill=(175, 175, 175))

        text = "Das et al. 2023"
        # text = "Das et al. 2023\narXiv:2307.06411"
        text_width, text_height = draw.textsize(text, font2)
        text_position = (805, 800)  # Adjust text position as needed
        draw.text(text_position, text, font=font2, fill=(175, 175, 175))

        combined_frame = np.array(frame_pil)

    fig, ax = plt.subplots()
    ax.imshow(combined_frame)
    ax.set_facecolor("k")
    fig.savefig("frame.png", dpi=1200)


    # # Add the combined frame to the video
    # writer.append_data(combined_frame)

    # print(i_mg, end="\t")



# Close the video writer
# writer.close()

print("Video creation complete. Saved as", output_video)
