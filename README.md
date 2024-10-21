# AI_voice_Replacer
PoC in Python using Streamlit which takes a Video file and replace its audio with an AI Generated voice


1. The POC that takes a video file with audio that is not proper (grammatical mistakes, lot of umms...and hmms etc.)
2. Transcribe this audio using Google's Speech-To-Text model.
3. Pass the above text to GPT-4o model, and correct the transcription removing any grammatical mistakes.
4. The transcription you get back should be passed to Text-to-Speech model of Google.
5. Finally, AI Generated audio will be replaced in original video file
