import trig
from signals import fft, ift, noise
import matplotlib.pyplot as plt

#iteratively finds a noise threshold and zeros all magnitudes below that and then subtracts average noise magnitude from existing signals
def spectral(x):

    #defines variables
    N = len(x)
    mean = 0

    #finds magnitd
    mag, phase = fft(x)

    #finds average magnitude
    mean = 0
    for i in mag:
        mean += i
    mean /= len(mag)

    #finds standard deviation and defines threshold
    sd = trig.sd(mag)
    thresh = mean * 7


    #finds average noise magntidue and standard deivation
    noise = []
    count = 0
    for i in mag:
        if i <= thresh:
            noise.append(i)
    noisesd = trig.sd(noise)
    noisemean = sum(noise) / len(noise)

    thresh = noisemean + 3 * noisesd

    #continues to find average noise magnitude with recrusive threshold
    iterations = 5
    for j in range(iterations):
        
        #creates threshold
        thresh = mean * 7
        mean = 0

        #creates variable for average magnitude of noise
        count = 0

        #cycles through all points, adds them to mean noise magnitude
        for i in range(N):
            if mag[i] < thresh:
                mean += mag[i]
                count += 1
        if count != 0:       
            mean /= count

    #subtracts mean noise magnitude from all frequencies remaining
    for i in range(N):
        if mag[i] > mean:
            mag[i] -= mean
        else:
            mag[i] = 0

    #runs cleaned frequency and phase list through an IFT to find signal
    cleanx = ift(mag, phase)[:N]
    return cleanx

#multiplies magnitudes by a confidence coefficient based off of a logistic curve based off of distance from a threshold
def confidence(x):

    #fetches frequency list
    mag, phase = fft(x)

    #calculates generous noise threshold
    mean = 0
    for i in mag:
        mean += i
    mean /= len(mag)
    sd = trig.sd(mag)
    thresh = mean + 5 * sd

    #calculates mean and standard deviation below that threshold (noise)
    noise = []
    count = 0
    for i in mag:
        if i <= thresh:
            noise.append(i)
    noisesd = trig.sd(noise)
    noisemean = sum(noise) / len(noise)

    #recalculates the noise threshold only counting values below the previous threshold iteratively
    iterations = max(2, round(2 * noisemean / noisesd))
    for j in range(iterations):
        noisemean = 0
        count = 0
        for i in mag:
            if i <= thresh:
                noisemean += i
                count += 1
        noisemean /= count
        noisesd = 0
        count = 0
        for i in mag:
            if i <= thresh:
                noisesd += (i - noisemean) ** 2
                count += 1
        noisesd = (noisesd / count) ** 0.5
        thresh = noisemean + 2 * noisesd
    # thresh += sd

    #uses a logistic plot to multiply all frequencies by a confidence value based on how certain we are that the frequency is primarily noise
    for i in range(len(mag)):
        factor = ((thresh) - mag[i]) / (noisesd)
        mag[i] *= ( 1 )/ (1 + trig.e ** (factor))

    #runs cleaned magnitude and phase lists through an ift to get signal
    cleanx = ift(mag, phase)
    return cleanx[:len(x)]

#orders frequencies by strength, finds the largest drop off, and removes all after said drop off
def sort(x):

    #defines variables
    N = len(x)
    mag, phase = fft(x)

    #sorts magnitude while preserving old list
    originalmag = list(mag)
    mag = sorted(mag, reverse = True)

    #finds differences between each magnitude
    differences = []
    for i in range(1, len(mag)):
        k = mag[i -1] - mag[i]
        differences.append(k)


    remove = 1
    sd = trig.sd(mag)
    #finds last large drop off in magnitude
    diff = 2 * sd
    for i in range(len(differences)):
        if differences[i] > diff:
            remove = i + 1

    if remove == 1:
        diff = 0
        for i in range(len(differences)):
            if differences[i] > diff:
                diff = differences[i]
                remove = i
    #removes all frequencies after big drop off
    for i in range(remove, N):
        mag[i] = 0

    #unsorts magnitude list by mapping saved magnitudes onto old list
    for i in range(len(originalmag)):
        if originalmag[i] not in mag:
            originalmag[i] = 0

    #runs cleaned magnitude list through an IFT
    cleanx = ift(originalmag, phase)[:N]
    return cleanx[:len(x)]

x = []
k = 200
for i in range(k):
    x.append(trig.sine(i, 3, k, 0, .8) + trig.cosine(i, 7, k, 0, .6) + trig.cosine(i, 20, k, 0, .6) + trig.sine(i, 2, k, 0, .6))

y = noise(x, .5)
z = spectral(y)
a = confidence(y)
b = sort(y)
c = spectral(a)
d = confidence(spectral(a))
e = confidence(b)
variations = [y, z, a, b, c, d, e]
for i in variations:
    rsquared = trig.correlation(x, i)
    print(rsquared)

plt.figure(1)
plt.plot(x)
plt.plot(c)
plt.grid(True)

plt.figure(2)
plt.plot(x)
plt.plot(y)
plt.grid(True)

plt.show()