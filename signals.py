import trig
import matplotlib.pyplot as plt

def DFT(x):
    xvalues = []
    N = len(x)

    #defines sampling rate to be one for simplicity
    smp = 1

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
            a += x[j] * trig.sin(2 * trig.pi * j * i * 1/N)
            b += x[j] * trig.cos(2 * trig.pi * j * i * 1/N)
        
        #saves our thingies
        freqa.append(a)
        freqb.append(b)

    #uses our thingies
    for i in range(N):
        stren.append(((freqa[i])**2 + (freqb[i])**2) ** .5)
        phase.append(trig.arctan(freqa[i], freqb[i]))

    #starts plotting our DFT
    for i in range(N // 2):
        xvalues.append(float(i * smp))

    plt.plot(xvalues, stren[:N//2], linestyle = '-')
    plt.xlabel('Frequency (hz)')
    plt.grid(True)
    plt.show()

    return stren, phase

k = 250
test = []
for i in range(k):
    test.append(trig.sine(i, 10, k, 1, 10) + trig.sine(i, 14, k, 5.3, 2) + trig.cosine(i, 28.9, k, 25.3, 30))

x,y = DFT(test)
