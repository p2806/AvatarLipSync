from flask import Flask, request, send_file
import subprocess
import os
from gtts import gTTS

app = Flask(__name__)

def text_to_speech(text, filename="output.wav"):
    tts = gTTS(text)
    tts.save(filename)

# Function to run Wav2Lip inference
def generate_lipsync_video(face_path, audio_path, output_path=r"C:\Users\Rajesh\Desktop\Avatarify\results\result_voice.mp4"):
    face_path = f'"{face_path}"'
    audio_path = f'"{audio_path}"'
    command = [
        "py", "-3.8",r"C:\Users\Rajesh\Desktop\Avatarify\Wav2Lip\inference.py",
        "--checkpoint_path", r"C:\Users\Rajesh\Desktop\Avatarify\Wav2Lip\checkpoints\wav2lip_gan.pth",
        "--face", r"C:\Users\Rajesh\Desktop\Avatarify\avatar_image.png",
        "--audio", r"C:\Users\Rajesh\Desktop\Avatarify\output.wav"
    ]
    print("Command:", " ".join(command))
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Lipsync video generated successfully!")
        return output_path
    else:
        print("Error generating video:", result.stderr)
        return None

@app.route('/generate-video', methods=['POST'])
def generate_video():
    if 'text' not in request.json:
        return {"error": "Text input is required."}, 400
    
    text_input = request.json['text']
    print(text_input)
    text_to_speech(text_input)
    
    # Save the face and audio files
    face_path = r"C:\Users\Rajesh\Desktop\Avatarify\avatar_image.png"
    audio_path = r"C:\Users\Rajesh\Desktop\Avatarify\output.wav"
    
    # Generate lipsync video
    output_video = generate_lipsync_video(face_path, audio_path)
    
    if output_video:
        return send_file(output_video, mimetype='video/mp4', as_attachment=True)
    else:
        return {"error": "Failed to generate video"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
