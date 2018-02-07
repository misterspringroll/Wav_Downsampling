import os,wave, audioop
def downsampleWav(src, dst, inrate=44100, outrate=16000, inchannels=2, outchannels=1):
    if not os.path.exists(src):
        print('Source not found!')
        return False

    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except:
        print('Failed to open files!')
        return False

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if inchannels != 1 and outchannels == 1:
            converted = audioop.tomono(converted[0], 2, 1, 0)
        else:
            converted = converted[0]
    except:
        print('Failed to downsample wav')
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted)
    except:
        print('Failed to write wav')
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print('Failed to close wav files')
        return False
    return True
os.chdir("animal")
for temp_file in os.listdir():
    temp_read = wave.open(temp_file,"r")
    num_channels = temp_read.getnchannels()
    sampling_rate = temp_read.getframerate()
    downsampleWav(temp_file,"../outputs/" + temp_file,sampling_rate, 16000, num_channels, 1)
