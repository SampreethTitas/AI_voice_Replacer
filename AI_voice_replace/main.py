import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import speech
from google.cloud import texttospeech
import openai
from dotenv import load_dotenv


load_dotenv()





speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()


def main():
    st.title("Audio Replacement PoC")

    
    uploaded_file = st.file_uploader("Upload a video file")

    if uploaded_file is not None:

        video_clip = VideoFileClip(uploaded_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile("temp_audio.wav")


        with open("temp_audio.wav", "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
        )

        response = speech_client.recognize(config=config, audio=audio)

        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript


        prompt = f"Correct the following transcription: {transcription}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        corrected_transcription = response.choices[0].text


        synthesis_input = texttospeech.SynthesisInput(text=corrected_transcription)
        voice = texttospeech.VoiceSelectionParams(
            name="en-US-Standard-A",
            language_code="en-US",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open("temp_ai_audio.mp3", "wb") as out_file:
            out_file.write(response.audio_content)


        new_audio = AudioFileClip("temp_ai_audio.mp3")
        final_video = video_clip.set_audio(new_audio)
        final_video.write_videofile("output_video.mp4")

        st.success("Audio replaced successfully!")
        st.video("output_video.mp4")

if __name__ == "__main__":
    main()