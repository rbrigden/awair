import urllib.request
import threading
from pydub import AudioSegment
import inspect

def capture(url):
    file_path='/Users/Matthew/Documents/'+url.split('/')[-1]
    urllib.request.urlretrieve(url, file_path)

def timeIt(t):
    counter=0
    while(counter<=t):
        print(counter,end="...")
        counter+=1
        time.sleep(1)

def test():
    x=urllib.request.urlopen('http://audio2.broadcastify.com/505577348.mp3')   


    list=inspect.getmembers(AudioSegment)
    for each in list:
        print(each[0])

    #x=urllib.request.urlopen('file:/Users/Matthew/Downloads/test_recording_cut.wav')
#    print(x.read(10))
#    print(x.read(10))
#    print(x.read(10))
#    urllib.request.urlretrieve('http://audio2.broadcastify.com/505577348.mp3', "/Users/Matthew/Documents/test1.mp3")
#    t=threading.Thread(target=capture, args=('http://audio2.broadcastify.com/505577348.mp3',))
    writing=True
    numSilent=0
    fileNum=1
    numInRow=0
    segFile = open('/Users/Matthew/Documents/segFile.mp3', 'wb')
    currentPath="/Users/Matthew/Documents/file1.mp3"
    currSeg = AudioSegment.empty()
    while (fileNum<4):
        segFile.write(x.read(1000))
        seg = AudioSegment.from_file('/Users/Matthew/Documents/segFile.mp3')

        print(seg.dBFS, end="  ")
        numInRow+=1
        if(numInRow>4):
            print()
            numInRow=0


        if(seg.dBFS>-30): writing,numSilent=True,0
        if(writing):
            currSeg.append(seg)
        if(seg.dBFS<=-30):
            numSilent+=1
            if(numSilent>5):
                writing=False
                currentSeg.export(currentPath, format="mp3")
                currentSeg=AudioSegment.empty()
                fileNum+=1
                currentPath="/Users/Matthew/Docmuents/file%d.mp3"%fileNum



    '''   t.start()
    time.sleep(10)
    t.stop()'''


test()









