import os
import threading
import subprocess
import tkinter as tk
from gtts import gTTS
from PIL import Image, ImageTk
import cv2
import pygame

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to play video using OpenCV and display in Tkinter
def play_video(video_path, label, stop_event=None):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)  # Calculate the delay in milliseconds

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_image = frame_image.resize((640, 360), Image.LANCZOS)  # Use Image.LANCZOS for resizing
        frame_photo = ImageTk.PhotoImage(frame_image)
        label.config(image=frame_photo)
        label.image = frame_photo  # Store reference to avoid garbage collection
        label.update()

        if stop_event and stop_event.is_set():
            break

        cv2.waitKey(delay)  # Add delay to match the original FPS

    cap.release()

# Generate speech from text
def generate_speech(text, audio_path="response.mp3", language='en'):
    try:
        print("Generating speech...")
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_path)
        print(f"Speech saved to {audio_path}")
    except Exception as e:
        print("Error generating speech:", e)

# Perform lip-sync using Wav2Lip
def lip_sync(checkpoint_path, face_path, audio_path, output_path):
    try:
        print("Running Wav2Lip inference...")
        subprocess.run([
            "python", "inference.py",
            "--checkpoint_path", checkpoint_path,
            "--face", face_path,
            "--audio", audio_path,
            "--outfile", output_path
        ])
        print(f"Lip-sync video saved to {output_path}")
    except Exception as e:
        print("Error during lip-sync process:", e)

# Basic chatbot response logic
def chatbot_response(user_input):
    if "name" in user_input.lower():
        return "My name is Thara."
    elif "age" in user_input.lower():
        return "I am 22 years old."
    elif "how are you" in user_input.lower():
        return "I'm just a program, but I'm here to help!"
    elif "what can you do" in user_input.lower():
        return "I can chat with you, and even lip-sync to my responses!"
    else:
        return "I'm not sure how to respond to that, but I'm learning!"

# Function to handle user input and generate a response
def process_input(text, label, checkpoint_path, loop_video_path, stop_event):
    response_text = chatbot_response(text)
    generate_speech(response_text, audio_path="response.mp3")

    # Check if response.mp3 was successfully created
    if not os.path.exists("response.mp3"):
        print("response.mp3 was not created. Skipping lip-sync.")
        return

    lip_sync(checkpoint_path, loop_video_path, 'response.mp3', 'lip_synced_output.mp4')

    # Check if the lip-sync video was successfully created
    if not os.path.exists("lip_synced_output.mp4"):
        print("lip_synced_output.mp4 was not created. Skipping playback.")
        return

    # Stop the loop video
    stop_event.set()

    # Play the audio using pygame mixer
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    # Play the generated lip-synced video
    cap = cv2.VideoCapture('lip_synced_output.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_image = frame_image.resize((640, 360), Image.LANCZOS)
        frame_photo = ImageTk.PhotoImage(frame_image)
        label.config(image=frame_photo)
        label.image = frame_photo
        label.update()
        
        cv2.waitKey(delay)
    
    cap.release()
    
    print("Lip-synced video finished playing.")

    # Stop the audio
    pygame.mixer.music.stop()

    # Reset the stop event to resume the loop video
    stop_event.clear()
    play_video(loop_video_path, label, stop_event=stop_event)

# Main function to setup Tkinter GUI and run the loop
def run_application(loop_video_path, checkpoint_path):
    root = tk.Tk()
    root.title("Virtual Girlfriend")
    
    # Video display label
    video_label = tk.Label(root)
    video_label.pack()

    # Text input area
    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    chat_input = tk.Entry(input_frame, font=("Helvetica", 14))
    chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

    stop_event = threading.Event()

    # Play the loop video in a separate thread
    video_thread = threading.Thread(target=play_video, args=(loop_video_path, video_label, stop_event))
    video_thread.start()

    def on_enter(event=None):
        text = chat_input.get()
        if text:
            print(f"Received input: {text}")
            chat_input.delete(0, tk.END)

            # Process the input and generate a response
            process_thread = threading.Thread(target=process_input, args=(text, video_label, checkpoint_path, loop_video_path, stop_event))
            process_thread.start()

    chat_input.bind("<Return>", on_enter)

    root.mainloop()

# Hard-coded parameters
checkpoint_path = 'C:\\Users\\sethu\\Downloads\\first-order-model-master\\checkpoints\\wav2lip_gan.pth'
loop_video_path = 'result_main.mp4'

# Start the application
run_application(loop_video_path, checkpoint_path)
