import trig

#random noise
def noise(signal, loudness):

    #defines noise parameters
    seed = 51925
    a = 987325234
    c = 40871212
    m = 1767174
    noise = [seed]
    noisy = []

    #creates noise function itself
    for i in range(1, len(signal)):
        b = ((noise[-1] * a + c) % m )
        noise.append(b)
    for i in range(len(noise)):
        noise[i] -= m/2

    #adjusts noise to not overpower signal
    #finds average signal strength
    mean = 0
    for i in signal:
        mean += i
    mean = mean/len(signal)

    #finds average distance from mean signal
    nice= 0
    for i in signal:
        nice += abs(i - mean)
    nice = nice/len(signal)

    #finds average magnitude of noise
    mean = 0
    for i in noise:
        mean += abs(i)
    mean = mean/len(noise)

    #normalizes noise magnitude based on requested loudness
    factor = loudness * nice / mean
    for i in range(len(noise)):
        noise[i] *= factor

    #applies noise to signal and returns
    for i in range(len(signal)):
        noisy.append(signal[i] + noise[i])
    return noisy

#Discrete Fourier Transform
def dft(x):
    N = len(x)

    #creates frequency strength lists
    freqa = []
    freqb = []
    stren = []
    phase = []

    #cycles the frequencies
    for i in range(N):

        #defines our reals and imaginaries
        a = 0
        b = 0

        #cycles the points
        for j in range(N):
            a += x[j] * trig.cos(2 * trig.pi * j * i * 1/N)
            b -= x[j] * trig.sin(2 * trig.pi * j * i * 1/N)
            
        
        #saves our thingies
        freqa.append(a)
        freqb.append(b)

    #uses our thingies
    for i in range(N):
        stren.append(((freqa[i])**2 + (freqb[i])**2) ** .5)
        phase.append(trig.arctan(freqa[i], freqb[i]))

    #starts plotting our DFT
    return stren, phase

#Discrete Fourier Transform BUT FAST

#Wrapper function for me to call
def fft(x):

    #defining our variables
    x = list(x)
    strength = []
    phase = []
    N = len(x)
    b = 2

    #changes x to a power of 2 to make it work with an fft
    while N > b:
        b *= 2
    for i in range(N, b):
        x.append(0)

    #calling complex function
    a = fftorganize(x)

    #organizing data into strength and phase
    for i in range(b):
        strength.append(((a[0][i])**2 + (a[1][i])**2) ** .5)
        phase.append(trig.arctan(a[1][i], a[0][i]))
    return strength, phase

#function that makes me sad
def fftorganize(x):

    #defining our variables
    even = []
    odd = []
    counter = 0
    neven = []
    nodd = []
    a = []
    b = []
    N = len(x)

    #if length is 1 gives simple a,b
    if N == 1:
        return [[0], [x[0]]]
    
    #breaks large chunk of signal (x) into even and odd components
    for i in x:
        a.append(0)
        b.append(0)
        neven.append([0])
        nodd.append([0])
        if counter == 0:
            even.append(i)
            counter = 1
        else:
            odd.append(i)
            counter = 0

    #recurses until it gets broken into smallest possible buckets
    neven = (fftorganize(even))
    nodd = (fftorganize(odd))

    #recombines even and odd components
    for i in range(N // 2):
        phased = 2 * trig.pi * i / N
        temp1 = nodd[0][i] * trig.cos(phased) - nodd[1][i] * trig.sin(phased)
        temp2 = nodd[1][i] * trig.cos(phased) + nodd[0][i] * trig.sin(phased)
        a[i] = neven[0][i] + temp1
        b[i] = neven[1][i] + temp2
        a[i + N // 2] = neven[0][i] - temp1
        b[i + N // 2] = neven[1][i] - temp2
    return [a, b]

def ift(mag, phase):
    signal = []
    length = len(mag)
    for j in range(length):
        x = 0
        for i in range(len(mag)):
            x += mag[i] * trig.cos(i * j * 2 * trig.pi / length + phase[i])
        signal.append(x / length)
    return signal

def denoise(x):
    N = len(x)
    mag, phase = fft(x)
    mean = 0
    for i in mag:
        mean += i
    mean /= N
    thresh = mean * 7
    meanmag = 0
    meanphase = 0
    count = 0
    for i in range(N):
        if mag[i] < thresh:
            meanmag += mag[i]
            count += 1
            mag[i], phase[i] = 0, 0
    meanmag /= count
    for i in range(N):
        if mag[i] > meanmag:
            mag[i] -= meanmag
    cleanx = ift(mag, phase)[:N]
    return cleanx

length = 200
x = []
for i in range(length):
    x.append(trig.sine(i, 3, length, 0, 25) + trig.cosine(i, 7, length, 0, 15))

noisy = noise(x, .5)
y = denoise(noisy)
z = denoise(y)

raw_error = 0
clean_error = 0
for i in range(len(x)):
    raw_error += abs(y[i] - noisy[i])
    clean_error += abs(z[i] - y[i])
print("noisy:", raw_error)
print("denoised:", clean_error)