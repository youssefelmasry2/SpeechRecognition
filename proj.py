from scipy.signal import butter, lfilter
import pyaudio
import numpy as np
import wave
import speech_recognition as sr

def record():
    #open dy btftahlena audio stream ne2dar nsagel bih audio
    stream= p.open(format= format,  #format el data storing zai (16 bit aw 32 bit w keda)
                channels= channels, #mono wala stereo
                rate= fs,  #kam piece of data byt3amalaha save per second
                input= True,        #to capture audio
                frames_per_buffer= frames_per_buffer)   #by read kam frame mara wahda

    print("Start Recording")
    for i in range(0, int(fs / frames_per_buffer * seconds)): #el range 3obara 3an ehna han3ml kam itteration fel 5 seconds
        data = stream.read(frames_per_buffer)#read 3200 frame at each iteration
        frames.append(data)     #bt save el data fel array el esmo frames

    print("Finished Recording")

    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    # wb write binarry
    wf = wave.open("output.wave", "wb")  # open dy btftahlena audio stream ne2dar nsagel bih audio
    # bnhot kol el values zai el recorded audio
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(fs)
    # write all frames in binary string, combine all frames into binary string .
    wf.writeframes(b''.join(frames))  # akeno bylaza2 el binary frames f ba3d 3ashan yeb2o string wahed
    wf.close()

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs      #el maximum freq el heya nos el sampling rate
    low = lowcut / nyquist  #normalized value 3ashan tshtaghal 3ala ay sampling rate
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band') #this function returns the numerator and denominator
    y = lfilter(b, a, data)     #applies a linear filter to the input signal using the provided coefficients
    return y
def speech_recognition():
    audio_file = sr.AudioFile("filtered_output.wav")  #by creat audio file
    recognizer= sr.Recognizer() #bnakhod object men el class da
    recognizer.energy_threshold=300  #ay sound taht el 300 han3tbrha noise
    #recognize_google must have audio of type audio data,
    #our audio is a type of audio file
    with audio_file as source:
        audio_file_data= recognizer.record(source) #bt record el data el fel audio file bt7awelha l haga esmaha audio data
    text= recognizer.recognize_google(audio_data=audio_file_data, language="en-US") #el methode el bet recogize el sound
    print(text)
p = pyaudio.PyAudio()
seconds = 5
frames = []
frames_per_buffer = 3200
format = pyaudio.paInt16
channels = 2
order = 5
fs = 44100  # sample rate
lowcut = 500  # lower cutoff frequency of the bandpass filter
highcut = 3000  # upper cutoff frequency of the bandpass filter

# Record audio
record()
input_file = "output.wave"      #el file el et3amalo creat fel record
output_file = "filtered_output.wav"     #el file el hayt3amal ba3d el filter

# Open the original WAV file for reading
with wave.open(input_file, 'rb') as wf:
    # Read audio data from the file
    original_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    #np.frombuffer(...): Converts the binary data (frames) read from the file into a NumPy array.

# bn3mel el bandpass filter
filtered_data = apply_bandpass_filter(original_data, lowcut, highcut, fs, order)

#bn creat el file el fih el filter
with wave.open(output_file, 'wb') as wf_filtered:
    wf_filtered.setnchannels(channels)
    wf_filtered.setsampwidth(p.get_sample_size(format))
    wf_filtered.setframerate(fs)
    wf_filtered.writeframes(np.int16(filtered_data).tobytes())

print(f"Filtered audio saved to {output_file}")
speech_recognition() 
