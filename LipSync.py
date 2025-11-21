import subprocess
import os

# Define the paths to your files and checkpoint
checkpoint_path = "C:\\Users\\sethu\\Downloads\\first-order-model-master\\checkpoints\\wav2lip_gan.pth"
face_video_path = "result_main.mp4"
audio_path = "response.wav"
output_video_path = "results\\result_voice.mp4"

# Ensure the results directory exists
os.makedirs("results", exist_ok=True)

# Step 1: Run the inference
inference_command = [
    "python", "inference.py",
    "--checkpoint_path", checkpoint_path,
    "--face", face_video_path,
    "--audio", audio_path
]

# Run the inference
subprocess.run(inference_command)

# Step 2: Adjust the audio volume
adjust_volume_command = [
    "ffmpeg", "-i", output_video_path,
    "-filter:a", "volume=2.0",
]


# Step 3: Re-encode the video and audio
reencode_command = [
    "ffmpeg", "-i",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    
]

print("Inference and video processing completed successfully.")
