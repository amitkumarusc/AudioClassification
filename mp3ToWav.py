import os
import subprocess
from os.path import basename

def shellquote(s):
	return "'" + s.replace("'", "'\\''") + "'"

for path,dirs,files in os.walk('/Users/amit/work/experimental/python-stuff/AudioClassification/audio_files'):
	for file in files:
		if file.lower().endswith('.mp3'):
			song_name = os.path.splitext(basename(file))[0]
			input_file = os.path.join(path, file)
			wav_file_name = os.path.join(path, song_name) + '.wav'
			cmd = 'mpg123 -w ' + shellquote(wav_file_name) + ' -r 10000 -m ' + shellquote(input_file)
			p = subprocess.Popen(cmd, shell=True)

