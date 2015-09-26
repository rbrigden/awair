import urllib.request
from pydub.silence import split_on_silence
from pydub import AudioSegment
import os
from OxfordTranscription import transcribeAndWriteToFile
from threading import Thread



def scan(streamUrl):
    if not os.path.exists("Segs/"):
        os.mkdir("Segs/")

    x=urllib.request.urlopen(streamUrl)
    currChunk=open("currChunk.mp3", 'wb')
    currChunk.truncate(0)
    currChunk.write(x.read(60000))

    silenceLen=3000
    threshhold=-30
    padding=300
    seg=AudioSegment.from_file("currChunk.mp3")
    a=split_on_silence(seg, silenceLen, threshhold, padding)
    countFile=open("count.txt","r")
    count=int(countFile.read())
    countFile.close
    countFile=open("count.txt","w")
    while(True):
        print()
        print("next chunk size", len(a))
        print()
        for i in range(len(a)):
            a[i].apply_gain(+10.0)
            a[i].export(("Segs/seg%d.wav"%count), format="wav")

            print("Starting ID", count)
            Thread(target=transcribeAndWriteToFile, args=("Segs/seg%d.wav"%count, count)).start()

            count+=1
            countFile=open("count.txt","w")    
            countFile.write(str(count))
            countFile.close()

        currChunk.truncate(0)
        currChunk.write(x.read(60000))

        seg=AudioSegment.from_file("currChunk.mp3")
        a=split_on_silence(seg, silenceLen, threshhold, padding)
        


scan('http://audio2.broadcastify.com/505577348.mp3')



