import picamera
import datetime
camera = picamera.PiCamera()
camera.resolution = (640, 480)

import time
import RPi.GPIO as GPIO
import pyaudio
import wave
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 2 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = datetime.datetime.now().strftime('%d-%m-%Y%H-%M-%S')+'.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("Audio  + Video recording")
frames = []
t = 0
camera.start_recording(datetime.datetime.now().strftime('%d-%m-%Y%H:%M:%S')+'.h264')
c = time.time()
f = 1
#GPIO.output(12, False)
#time.sleep(10000000)

# loop through stream and append audio chunks to frame array
while True:
#    camera.wait_recording(record_secs)
    t = t + 1
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk, False)
        frames.append(data)
        if ii<1:
            print('Motor running')
            GPIO.output(12, True)
        else:
            GPIO.output(12, False)
    if t > 10:
        break
#GPIO.output(12, False)
camera.stop_recording()
print('Finished video recording')

while True:
    t = t+1
    for ii in range(0, int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk, False)
        frames.append(data)
        if ii<1:
            GPIO.output(12, True)
            print('Motor Running')
        else:
            GPIO.output(12, False)
    if t > 20:
        break
    #GPIO.output(12, True)
    #time.sleep(0.1)
    #GPIO.output(12, False)
    #time.sleep(0.7)

print("Finished audio recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
GPIO.cleanup()
