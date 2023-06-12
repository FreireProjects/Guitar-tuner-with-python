# Importando as bibliotecas utilizadas para auxiliar no programa
import numpy as np
import pyaudio
from scipy import signal
import matplotlib.pyplot as plt
import time

import os
#.................................................................

# Constantes de formatação da captação do audio do microfone
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 10000
CHUNK_SIZE = 4096
THRESHOLD = 90000

# Parâmetros do filtro a ser lido
FILTER_ORDER = 4
CUTOFF_FREQUENCY = 1000

# Desenvolvimento do filtro passa-baixa
b, a = signal.butter(FILTER_ORDER, CUTOFF_FREQUENCY / (RATE / 2), 'low')

# Usando biblioteca para captação do audio
audio = pyaudio.PyAudio()

# Inicio da captacao do audio ao vivo
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

#Variáveis Vetor para armazenar os valores referentes a frequência do sinal e o valor que o sinal será amostrado
freq_values = []
time_values = []

#Definições e configurações para plotagem do gráfico 1
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.set_title("Dominant Frequency")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Frequency (Hz)")
line, = ax1.plot([], [], color = 'r')

#Definições e configurações para plotagem do gráfico 2
ax2.set_title("FFT")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Amplitude")
fft_line, = ax2.plot([], [], color = 'b')

#Plotagem de ambos os gráficos em tempo real 
plt.ion()
plt.show()

#Função utilizada para desenvolver todo o tratamento e captação do audio
def capitacao():
    # Variavel para escolha da corda a ser afinada
    corda = input('Digite o número da corda [1,2,3,4,5,6] que você deseja afinar: ')
    # Variavel auxiliar para repetição
    afinado = True
    print("Esperando nota ser tocada...")
    #Função try usada para continuar tentando enquanto não der erro na condição
    try:
        #While usado para loopar a captação do audio
        while afinado:
    # Leitura do valor do audio captado pelo microfone
            audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
    # Aplicação do filtro no audio lido pelo microfone
            audio_filtro = signal.lfilter(b, a, audio_data)
    # Calculando a FFT no sinal filtrado
            fft_data = np.fft.fft(audio_filtro)
            fft_data_f  = np.where(fft_data > THRESHOLD, fft_data, 0)
    # Calculando as frequencias correspondentes da FFT
            freqs = np.fft.fftfreq(len(fft_data_f), 1.0 / RATE)
    # Achando o valor de maior amplitude no valor de audio aplicado a FFT
            max_amp_index = np.argmax(np.abs(fft_data_f))
    # Armazenando o valor de frequência correspondente
            max_freq = freqs[max_amp_index]

            freq_values.append(max_freq)
            time_values.append(len(freq_values) * CHUNK_SIZE / RATE)
    
            # Atualizando os valores de plotagem do gráfico 1
            line.set_data(time_values, freq_values)
    
            # Ajustando os limites de plotagem do gráfico 1
            ax1.relim()
            ax1.autoscale_view()
            
            # Redesenhando a plotagem no gráfico 1
            fig.canvas.draw()

            # Plotando e setando as configurações do gráfico 2
            ax2.clear()  # Limpando os valores do suplot do gráfico 2
            ax2.set_title("FFT") #Definindo o título do gráfico 2
            ax2.set_xlabel("Frequency (Hz)") #Definindo o título do eixo X do gráfico 2
            ax2.set_ylabel("Amplitude") #Definindo o título do eixo Y do gráfico 2
            ax2.plot(freqs, np.abs(fft_data_f), color='b')
            ax2.set_ylim([0, 500000])  # Ajustando os limites do eixo Y conforme necessário
            ax2.set_xlim([0, 500])  # Ajustando os limites do eixo X conforme necessário
            ax2.set_xticks(range(0, 500, 20)) #Definindo os valores em um range entre 0 e 500, com um passo de 20
    
            # Pequeno intervalo de tempo para permitir que os gráficos sejam atualizados
            plt.pause(0.001)

            # Após o tratamento do aúdio do microfone:
            if(max_freq>0):
                #printar o valor obtido 
                print("A corda se encontra na frequência: ", max_freq)

                #Switch case para afinação de cada acorde conforme corda selecionada no inicio do programa
                match corda:
                    #Aqui levamos em conta a posição de cada acorde, sendo a seguinte sequência: 1(Mizinha), 2(Si), 3(Sol), 4(Ré), 5(Lá), 6(Mizona)

                    #Case para afinação da corda Mizinha
                    case '1':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Mizinha
                        if (max_freq >= 329 and max_freq <= 331) or (max_freq >= 163 and max_freq <= 165):                                
                            #Quando afinado, altera o valor da variável afinado para False e quebra o loop while
                            afinado = False
                            print('A corda Mizinha está afinada!')
                        else:
                                #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                                afinacao = 330 - max_freq
                                #Se o resultado da conta for <0, a corda precisa ser afrouxada
                                if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                                #Se o resultado da conta for >0, a corda precisa ser apertada
                                else:
                                    print('Violão desafinado, aperte a corda!')
                    #Case para afinação da corda Si
                    case '2':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Si
                        if (max_freq >= 246 and max_freq <= 248) or (max_freq >= 122 and max_freq <= 125) or (max_freq >= 492 and max_freq <= 495):
                            afinado = False
                            print('A corda Si está afinada!')
                        else:
                            #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                            afinacao = 247 - max_freq
                            #Se o resultado da conta for <0, a corda precisa ser afrouxada
                            if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                            #Se o resultado da conta for >0, a corda precisa ser apertada
                            else:
                                    print('Violão desafinado, aperte a corda!')
                    #Case para afinação da corda Sol
                    case '3':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Sol
                        if (max_freq >= 195 and max_freq <= 197) or (max_freq >= 47 and max_freq <= 50) or (max_freq >= 96 and max_freq <= 99) or (max_freq >= 390 and max_freq <= 393): 
                            afinado = False
                            print('A corda Sol está afinada!')
                        else:
                            #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                            afinacao = 196 - max_freq
                            #Se o resultado da conta for <0, a corda precisa ser afrouxada
                            if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                            #Se o resultado da conta for >0, a corda precisa ser apertada
                            else:
                                    print('Violão desafinado, aperte a corda!')
                    #Case para afinação da corda Ré
                    case '4':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Ré
                        if (max_freq >= 145 and max_freq <= 147.8) or (max_freq >=72 and max_freq <= 74) or (max_freq >= 292 and max_freq <= 295):
                            afinado = False
                            print('A corda Ré está afinada!')
                        else:
                            #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                            afinacao = 146 - max_freq
                            #Se o resultado da conta for <0, a corda precisa ser afrouxada
                            if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                            #Se o resultado da conta for >0, a corda precisa ser apertada
                            else:
                                    print('Violão desafinado, aperte a corda!')  
                    #Case para afinação da corda Lá
                    case '5':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Lá
                        if (max_freq >= 109 and max_freq <= 111) or (max_freq >= 54 and max_freq <= 56) or (max_freq >= 219 and max_freq <= 221) or (max_freq >= 439 and max_freq <= 441):
                            afinado = False
                            print('A corda Lá está afinada!')
                        else:
                            #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                            afinacao = 110 - max_freq
                            #Se o resultado da conta for <0, a corda precisa ser afrouxada
                            if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                            #Se o resultado da conta for >0, a corda precisa ser apertada
                            else:
                                    print('Violão desafinado, aperte a corda!')
                    #Case para afinação da corda Mizona
                    case '6':
                        #If para checar se o valor da frequência está correspondente com o valor padrão (e variações) da corda Mizona
                        if max_freq >= 82 and max_freq <= 83.5:
                            afinado = False
                            print('A corda Mizona está afinada!')
                        else:
                            #Conta usada para saber se será necessário apertar ou afrouxar a corda para afinar o violão
                            afinacao = 82.5 - max_freq  
                            #Se o resultado da conta for <0, a corda precisa ser afrouxada
                            if afinacao < 0:
                                    print('Violão desafinado, afrouxe a corda!')
                            #Se o resultado da conta for >0, a corda precisa ser apertada
                            else:
                                    print('Violão desafinado, aperte a corda!')                        
            else:
                 #Pequeno tempo de delay para conseguir se ler a mensagem do valor da frequência e se precisa afrouxar ou apertar a corda antes de apaga-lá do terminal
                 time.sleep(0.5)
                 # Limpando a tela após a leitura
                 os.system('cls')
                 print("Esperando nota ser tocada...")
    
    #Acompanhamento da função Try, caso algo de errado, será redirecionado ao Except e mostrará na tela qual o erro encontrado
    except Exception as e:
            print(e)
    
    #Após o while ser concluido e o Try acabar, será redirecionado para o finally, que irá ficar responsável pelo loop e questionar se deseja afinar outra corda
    finally:
        lup = input('Deseja afinar outra corda?: ')
        if lup.lower() == 's' or lup.lower() == 'sim':
            capitacao()
        elif lup.lower() == 'n' or lup.lower() == 'nao':
            print('Ok!')

#Chamando a função capitacao para ser executada
capitacao()
