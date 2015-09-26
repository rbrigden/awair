import urllib.request

def test():
    x=urllib.request.urlopen('http://audio2.broadcastify.com/505577348.mp3')
 #   x=urllib.request.urlopen('file:/Users/Matthew/Downloads/test_recording_cut.wav')
    print(x.read(10))
    print(x.read(10))
    print(x.read(10))


test()