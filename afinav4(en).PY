# import the used librarys in this program
import numpy as np
import pyaudio
from scipy import signal
import matplotlib.pyplot as plt
import time
import os
#.................................................................

# Constants for audio settings
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 10000
CHUNK_SIZE = 4096
THRESHOLD = 90000

#filter parameters
FILTER_ORDER = 4
CUTOFF_FREQUENCY = 1000

#Desing the low-pass filter
b, a = signal.butter(FILTER_ORDER, CUTOFF_FREQUENCY / (RATE / 2), 'low')

# Create PyAudio object
audio = pyaudio.PyAudio()

# Open microphone stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

#Vector variables to showing us the frequency values and time values
freq_values = []
time_values = []

#Definitions and settings to plot about graph 1
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.set_title("Dominant Frequency")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Frequency (Hz)")
line, = ax1.plot([], [], color = 'r')

#Definitions and settings to plot about graph 2
ax2.set_title("FFT")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Amplitude")
fft_line, = ax2.plot([], [], color = 'b')

#Plot both graphs in real-time 
plt.ion()
plt.show()

#Function used to develop the audio captation and treatment
def capitacao():
    # Variable to select the guitar string to tune
    corda = input('Choose the string number [1,2,3,4,5,6] than you want to tune: ')
    # Variable to loop
    afinado = True
    print("Waiting the note to be played...")
    #Try function
    try:
        #While used to loop the audio captation
        while afinado:
    # Read audio data from the stream
            audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
    # Apply the filter on the input audio read
            audio_filtro = signal.lfilter(b, a, audio_data)
    # Compute the FFT of the audio signal filter
            fft_data = np.fft.fft(audio_filtro)
            fft_data_f  = np.where(fft_data > THRESHOLD, fft_data, 0)
    # Compute the frequencies corresponding to the FFT bins
            freqs = np.fft.fftfreq(len(fft_data_f), 1.0 / RATE)
    # Find the index of the maximum amplitude in the FFT data
            max_amp_index = np.argmax(np.abs(fft_data_f))
    # Retrieve the corresponding frequency
            max_freq = freqs[max_amp_index]

    # Append the frequency and time values to the lists
            freq_values.append(max_freq)
            time_values.append(len(freq_values) * CHUNK_SIZE / RATE)
    
            # Update the plot data graph 1
            line.set_data(time_values, freq_values)
    
            # Adjust the plot limits graph 1
            ax1.relim()
            ax1.autoscale_view()
            
            # Redraw the plot graph 1
            fig.canvas.draw()

            # Plot and configure the settings about the graph 2
            ax2.clear()  # Clean the values about the graph 2
            ax2.set_title("FFT") #Title define in graph 2
            ax2.set_xlabel("Frequency (Hz)") #Title define the x axis about the graph 2
            ax2.set_ylabel("Amplitude") #Title define the y axis about the graph 2 
            ax2.plot(freqs, np.abs(fft_data_f), color='b')
            ax2.set_ylim([0, 500000])  # Adjust the limits from y axis
            ax2.set_xlim([0, 500])  # Adjust the limits from x axis
            ax2.set_xticks(range(0, 500, 20)) #Define the grange values (0-500) with a step of the 20
    
            # Pause for a short time to allow the plot to refresh
            plt.pause(0.001)

            # After the mic treatment:
            if(max_freq>0):
                #print the frequency value
                print("The string frequency is: ", max_freq)

                #Switch case to tune the guitar strings according to select string
                match corda:
                    #We can to consider the guitar string position, it's the sequency: 1(E), 2(B), 3(G), 4(D), 5(A), 6(E)

                    #Case to tune E string
                    case '1':
                        #If to check the standart frequency value
                        if (max_freq >= 329 and max_freq <= 331) or (max_freq >= 163 and max_freq <= 165):                                
                            #When tune, stopped the while loop
                            afinado = False
                            print('The E string is tune!')
                        else:
                                #Here, we can know if we needed to press or to loosen the string
                                afinacao = 330 - max_freq
                                #If the result is <0, the string need to be loosen
                                if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                                #If the result is >0, the string need to be press
                                else:
                                    print('Guitar tuneless, to press the string!')
                    #Case to tune B string
                    case '2':
                        #If to check the standart frequency value
                        if (max_freq >= 246 and max_freq <= 248) or (max_freq >= 122 and max_freq <= 125) or (max_freq >= 492 and max_freq <= 495):
                            afinado = False
                            print('The B string is tune!')
                        else:
                            #Here, we can know if we needed to press or to loosen the string
                            afinacao = 247 - max_freq
                            #If the result is <0, the string need to be loosen
                            if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                            #If the result is >0, the string need to be press
                            else:
                                    print('Guitar tuneless, to press the string!')
                    #Case to tune G string
                    case '3':
                        #If to check the standart frequency value
                        if (max_freq >= 195 and max_freq <= 197) or (max_freq >= 47 and max_freq <= 50) or (max_freq >= 96 and max_freq <= 99) or (max_freq >= 390 and max_freq <= 393): 
                            afinado = False
                            print('The G string is tune!')
                        else:
                            #Here, we can know if we needed to press or to loosen the string
                            afinacao = 196 - max_freq
                            #If the result is <0, the string need to be loosen
                            if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                            #If the result is >0, the string need to be press
                            else:
                                    print('Guitar tuneless, to press the string!')
                    #Case to tune D string
                    case '4':
                        #If to check the standart frequency value
                        if (max_freq >= 145 and max_freq <= 147.8) or (max_freq >=72 and max_freq <= 74) or (max_freq >= 292 and max_freq <= 295):
                            afinado = False
                            print('The D string is tune!')
                        else:
                            #Here, we can know if we needed to press or to loosen the string
                            afinacao = 146 - max_freq
                            #If the result is <0, the string need to be loosen
                            if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                            #If the result is >0, the string need to be press
                            else:
                                    print('Guitar tuneless, to press the string!')  
                    #Case to tune A string
                    case '5':
                        #If to check the standart frequency value
                        if (max_freq >= 109 and max_freq <= 111) or (max_freq >= 54 and max_freq <= 56) or (max_freq >= 219 and max_freq <= 221) or (max_freq >= 439 and max_freq <= 441):
                            afinado = False
                            print('The A string is tune!')
                        else:
                            #Here, we can know if we needed to press or to loosen the string
                            afinacao = 110 - max_freq
                             #If the result is <0, the string need to be loosen
                            if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                            #If the result is >0, the string need to be press
                            else:
                                    print('Guitar tuneless, to press the string!')
                    #Case to tune E string
                    case '6':
                        #If to check the standart frequency value
                        if max_freq >= 82 and max_freq <= 83.5:
                            afinado = False
                            print('The E string is tune!')
                        else:
                            #Here, we can know if we needed to press or to loosen the string
                            afinacao = 82.5 - max_freq  
                             #If the result is <0, the string need to be loosen
                            if afinacao < 0:
                                    print('Guitar tuneless, to loosen the string!')
                            #If the result is >0, the string need to be press
                            else:
                                    print('Guitar tuneless, to press the string!')                        
            else:
                 #delay to show the frequency value in VSC terminal
                 time.sleep(0.5)
                 # Clean the terminal after the frequency reading
                 os.system('cls')
                 print("Waiting the note to be played...")
    
    #Except function used to show what's the error
    except Exception as e:
            print(e)
    
    #Finally function used when the while loop is stopped
    finally:
        lup = input('Do you want to tune other string?: ')
        if lup.lower() == 'y' or lup.lower() == 'yes':
            capitacao()
        elif lup.lower() == 'n' or lup.lower() == 'not':
            print('Ok!')

#Call the function 'capitacao' to be executed
capitacao()
