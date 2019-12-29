import speech_recognition as sr
import speech_to_text as st


r = sr.Recognizer()
with sr.WavFile(R"E:\workspace\Automatically-Build-Corpora\v-corpus\Baidu\test-audio.wav") as source:
    audio = r.record(source)

IBM_USERNAME = "5bc637d4-4966-420a-a5cf-9bc07d7b2212"
IBM_PASSWORD = "rRLoEAUttTSb"

text = st.recognize_speech(IBM_USERNAME,IBM_PASSWORD,audio,None)
print(text)
old_text = open('test-sentences', 'r', encoding="utf-8")
with open('Voice-Corpus', 'a', encoding='utf8') as file:
    if text!=old_text and len(text)==len(old_text):
        file.write(text)


