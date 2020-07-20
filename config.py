import pyaudio
import wave
import speech_recognition as sr
import http.client
from array import array
from datetime import datetime


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

def record():

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

	print("Start recording")

	frames = []

	try:
		initial_time = datetime.now()
		while (True):
			data = stream.read(CHUNK)
			frames.append(data)
			data_chunk=array('h',data)
			if (max(data_chunk) > 9000 ) :
				initial_time = datetime.now()
			current_time = datetime.now()
			print(max(data_chunk), datetime.now(), current_time.second - initial_time.second)
			if (max(data_chunk) < 9000 and current_time.second - initial_time.second > 5) :
				break
	except KeyboardInterrupt:
		print("Done recording")
	except Exception as e:
		print(str(e))

	sample_width = p.get_sample_size(FORMAT)
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	return sample_width, frames	

def record_to_file(file_path):
	wf = wave.open(file_path, 'wb')
	wf.setnchannels(CHANNELS)
	sample_width, frames = record()
	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

def convert_to_text(file_path):
	filename = file_path
	f = open('text.txt', 'w')
	r = sr.Recognizer()
	with sr.AudioFile(filename) as source:
		audio_data = r.record(source)
		text = r.recognize_google(audio_data)
		f.write(text)
	f.close()

def create_card():
	conn = http.client.HTTPConnection('localhost',8000)
	conn.request('GET', '/api/trello/searchCard')
	r = conn.getresponse()
	print(r.read())

if __name__ == '__main__':
	print('#' * 80)
	create_card()
	print('Please select the input method\n1. Record voice\n2. Pass recorded file\n3. Exit')
	choice = int(input())
	print (type(choice))
	if choice == 3:
		exit()
	if choice == 2:
		print('Please specify the file path with .wav extention')
		file_path = 'G:\Working\output.wav'#input()
	else :
		print("Please speak word(s) into the microphone")
		print('Press Ctrl+C to stop the recording')
		record_to_file('output.wav')	
		print("Result written to output.wav")
		file_path = './output.wav'
	convert_to_text(file_path)
	print('#' * 80)