from demo import load_checkpoints, make_animation
import imageio
import numpy as np
import torch
import cv2

# Function to read and resize video frames using OpenCV
def read_video_frames(video_path, size=(255, 255)):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame_resized = cv2.resize(frame_rgb, size)  # Resize frame
        frames.append(frame_resized)
    cap.release()
    return frames

# Function to read and resize the source image
def read_image(image_path, size=(255, 255)):
    image = imageio.imread(image_path)
    image_resized = cv2.resize(image, size)  # Resize image
    return image_resized

# Hard-coded parameters
config_path = 'config/vox-256.yaml'
driving_video_path = 'test-video2.mp4'
source_image_path = 'kathir_2.jpeg'
checkpoint_path = 'checkpoints/vox-cpk.pth'
relative = True
adapt_scale = True
use_cpu = True  # Set to False if you want to use GPU

# Read and resize source image
source_image = read_image(source_image_path)
# Read and resize driving video frames
driving_video = read_video_frames(driving_video_path)

# Ensure numpy arrays
source_image = np.array(source_image)
driving_video = [np.array(frame) for frame in driving_video]

# Normalize images
source_image = (source_image / 255.0).astype(np.float32)
driving_video = [(frame / 255.0).astype(np.float32) for frame in driving_video]

# Set device
device = 'cpu' if use_cpu else 'cuda'
generator, kp_detector = load_checkpoints(config_path=config_path, 
                                          checkpoint_path=checkpoint_path,
                                          cpu=use_cpu)

# Generate the animation
predictions = make_animation(source_image, driving_video, generator, kp_detector, 
                             relative=relative, adapt_movement_scale=adapt_scale)

# Save the resulting video
imageio.mimsave('result3.mp4', predictions)
