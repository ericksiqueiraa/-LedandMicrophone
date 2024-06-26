---
# Controle de LED com Arduino e Som

## Visão Geral

Este projeto demonstra como acender e apagar um LED conectado a um Arduino com base no nível de som captado por um microfone conectado ao computador. Um script Python processa o áudio do microfone e envia comandos ao Arduino para controlar o LED.

## Componentes

### Hardware

- Arduino (ex.: Uno)
- LED
- Resistor de 220Ω
- Cabo USB para conectar o Arduino ao computador
- Microfone conectado ao computador (ex.: microfone USB)
- Breadboard e fios jumper

### Software

- PlatformIO
- Python 3
- Bibliotecas Python: `pyaudio`, `numpy`, `pyserial`

## Montagem do Circuito

1. Conecte o anodo (perna maior) do LED ao pino digital 9 do Arduino.
2. Conecte o catodo (perna menor) do LED ao GND através de um resistor de 220Ω.
3. Conecte o Arduino ao computador via cabo USB.

## Configuração e Execução

### 1. Carregar o Código no Arduino

Use o PlatformIO para carregar o seguinte código no Arduino:

```cpp
#include <Arduino.h>
#define led 3

void setup()
{
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop()
{
  while (Serial.available())
  {
    char command = Serial.read();

    if (command == '1')
    {
      digitalWrite(led, HIGH);
    }
    else if (command == '0')
    {
      digitalWrite(led, LOW);
    }
  }
}
```

### 2. Configurar o Ambiente Python

Instale as bibliotecas necessárias:

```bash
pip install pyaudio numpy pyserial
```

### 3. Executar o Script Python

Crie e execute o seguinte script Python para capturar o som e controlar o LED:

```python
import pyaudio
import numpy as np
import serial
import time

ser = serial.Serial('COM4', 9600)
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

        
        if rms > 500: 
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
```

### Ajustes e Calibragem

- **Limiar de Som**: O valor do limiar (`500` no exemplo) pode precisar ser ajustado com base no ambiente e na sensibilidade do microfone.
- **Porta Serial**: Verifique a porta serial correta (`COM4` no exemplo) para o seu Arduino e ajuste conforme necessário.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
---