# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt #入力波形を表示させる用
import glob  # ファイルを取得
import graphviz  # dotファイルを表示
import os
import librosa  # MFCC
from time import sleep
from sklearn.externals import joblib #モデルを保存・呼び出し


###########正解ラベル###########
cls_dic = {'single_tap': 0, 'double_tap': 1, 'single_swipe': 2, 'double_swipe': 3}
##############################


# MFCCに通して特徴量を返す
def getMfcc(filename):
    y, sr = librosa.load(filename)
    return librosa.feature.mfcc(y=y, sr=sr)


##Arduinoに信号を送信
import serial
ser = serial.Serial()
ser.baudrate = 9600
for file in os.listdir('/dev'):
    if "tty.usbmodem" in file:
        ser.port = '/dev/'+file
        ser.open() #シリアルモニタを開く(開いてから信号を送信するまで2秒待つ必要があるから音声入力の前に配置)


##音声の入力##
import pyaudio  # 音声入力
import wave
from datetime import datetime

FORMAT = pyaudio.paInt16
CHANNELS = 1  # モノラル
RATE = 44100  # サンプルレート
CHUNK = 2**10  # データ点数
RECORD_SECONDS = 2  # 録音する時間の長さ
#WAVE_OUTPUT_FILENAME = "input_audio.wav"
THRESHHOLD = 0.5

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

sleep(1) #マイクを開いたときに入るノイズを回避
print('Recording...')

while True: #double_tapが来るまで回し続ける
    data = stream.read(CHUNK, exception_on_overflow = False)
    x = np.frombuffer(data, dtype="int16") / 32768.0

    if x.max() > THRESHHOLD: #ある音以上の大きさを入力と認識する
        print('==Start==')
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"

        all = []
        all.append(data)
        for i in range(0, int(RATE / CHUNK * int(RECORD_SECONDS))):
            data = stream.read(CHUNK, exception_on_overflow = False)
            all.append(data)
        data = b''.join(all)
        #ファイルを保存
        out = wave.open(filename,'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data)
        out.close()

        print('==End==')

        # MFCCにかけて特徴量抽出
        sound = filename
        feature = getMfcc(sound)  # MFCCにより特徴量を抽出
        x_test =feature.reshape(1, -1)  # 特徴量の次元を規格化
        os.remove(sound)
        # print(x_test.shape)

        # 決定木のモデルを呼び出し
        tree = joblib.load('decisiontree_mfcc.pkl')
        first_signal = tree.predict(x_test)[0]  # 作成したモデルを用いて予測を実行
        print('Signal: ' + first_signal)

        if first_signal.astype(np.int64) == 1: #double_tapが来たら終了
            print('-*-Quit-*-')
            break
        else:
            #Arduinoに信号'0'などを送信
            ser.write(str(first_signal).encode()) # 0=off, 2=RED on, 3=GREENon
            print('--next input\n↓\n')

#マイクをオフ
stream.close()
audio.terminate()

#ArduinoのLEDをオフ
ser.write('0'.encode())
ser.close()
