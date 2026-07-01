import trig
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

def denoise(x, quietness):
    N = len(x)
    mag, phase = fft(x)
    mean = 0
    for i in mag:
        mean += i
    mean /= N
    thresh = mean * quietness
    for i in range(N):
        if mag[i] < thresh:
            mag[i], phase[i] = 0, 0
    cleanx = ift(mag, phase)[:N]
    return cleanx
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

length = 50
quiet = 6
sin = []
cos = []
square = []

for b in range(1, 10):
    dummy = []
    for i in range(length):
        dummy.append(trig.sine(i, b, length, 0, 25))
    sin.append(dummy)
for b in range(1, 10):
    dummy = []
    for i in range(length):
        dummy.append(trig.cosine(i, b, length, 0, 25))
    cos.append(dummy)
for b in range(1, 10):
    dummy = []
    for i in range(length):
        dummy.append(trig.square(i, b, length, 0, 25))
    square.append(dummy)

errors = []
for freq1 in range(0, 9, 3):
    for freq2 in range(0, 9, 3):
        for freq3 in range(0, 9, 3):
            x = []
            for i in range(length):
                x.append(sin[freq1][i] + cos[freq2][i] + square[freq3][i])

            noisy = noise(x, .1)

            lo = 0.1
            hi = 50
            for _ in range(15):
                third = (hi - lo) / 3
                m1 = lo + third
                m2 = hi - third

                e1 = 0
                e2 = 0
                y1 = denoise(noisy, m1)
                y2 = denoise(noisy, m2)
                for i in range(len(x)):
                    e1 += abs(x[i] - y1[i])
                    e2 += abs(x[i] - y2[i])

                if e1 < e2:
                    hi = m2
                else:
                    lo = m1
            errors.append((lo + hi) / 2)
avg = 0
for r in errors:
    avg += r
avg /= len(errors)
real_errors = []
for r in errors:
    if r < 40:
        real_errors.append(r)

avg = 0
for r in real_errors:
    avg += r
avg /= len(real_errors)
print("filtered avg:", avg)
print("hit ceiling:", len(errors) - len(real_errors), "out of", len(errors))
print(errors)