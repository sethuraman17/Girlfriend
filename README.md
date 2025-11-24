# Demo INTRO

https://github.com/user-attachments/assets/ad0a27cb-5f67-4f98-b558-0f29be118b18

# AI-Powered Lip-Sync Chatbot

This project is an AI-powered chatbot that generates realistic lip-synced animations from a static image. It combines text-to-speech, deep learning-based lip-syncing, and a graphical user interface to create an interactive and engaging user experience.

## Features

*   **AI-Powered Text-to-Speech**: Converts user text input into natural-sounding speech.
*   **Realistic Lip-Syncing**: Animates a static photo to match the generated audio using the Wav2Lip model.
*   **Chatbot Interface**: Provides a simple and intuitive graphical user interface for interacting with the application.
*   **Customizable**: Easily modify the input image and chatbot responses to create your own unique virtual assistant.

## How It Works

The application follows a simple yet powerful workflow:

1.  **User Input**: The user types a message into the chatbot's graphical user interface (GUI).
2.  **Text-to-Speech**: The input text is converted into an audio file using Google's Text-to-Speech (gTTS) library.
3.  **Lip-Sync Animation**: The generated audio and a static input image are passed to the Wav2Lip model, which creates a video file with the image's lips animated in sync with the audio.
4.  **Video Playback**: The resulting video is played back in the GUI, creating the illusion of a talking character.

# Test Image

![test2](https://github.com/user-attachments/assets/45797274-9cdf-407f-b4df-15d7648b71c4)

# After it gets life

https://github.com/user-attachments/assets/0fd98dc0-d63b-45b9-8fc0-9c9a3ef90e6d

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.6 or higher
*   pip
*   FFmpeg

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the pre-trained model:**

    Download the `Wav2Lip + GAN` pre-trained model from the official [Wav2Lip repository](https://github.com/Rudrabha/Wav2Lip). Place the downloaded checkpoint file (e.g., `wav2lip_gan.pth`) in a directory of your choice.

4.  **Update the checkpoint path:**

    Open `chatbot.py` and update the `checkpoint_path` variable to point to the location of your downloaded model.

## Usage

To run the chatbot, execute the following command in your terminal:

```bash
python chatbot.py
```

This will open a window with the chatbot's video feed and a text input field. Type your message and press Enter to see the chatbot respond.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is built upon the excellent work of the [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) researchers.
