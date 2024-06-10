import pyaudio
import numpy as np
import serial
import time


ser = serial.Serial('COM3', 9600)
time.sleep(2)  


CHUNK = 1024  
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening...")

def get_rms(data):
    """Obter o valor RMS do áudio"""
    count = len(data) / 2
    format = "%dh" % count
    shorts = np.frombuffer(data, dtype=np.int16)
    rms = np.sqrt(np.mean(np.square(shorts)))
    return rms

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = get_rms(data)
        print(f'RMS Value: {rms}')

        
        if rms > 10:  
            ser.write(b'1') 
        else:
            ser.write(b'0') 
except KeyboardInterrupt:
    print("Interrompido pelo usuário")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    ser.close()
