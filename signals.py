import trig
print(trig.__file__)
print(dir(trig))

def DFT(x):
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
            a += x[j] * trig.sin(2 * trig.pi * j * i * 1/N)
            b += x[j] * trig.cos(2 * trig.pi * j * i * 1/N)
        
        #saves our thingies
        freqa.append(a)
        freqb.append(b)

    #uses our thingies
    for i in range(N):
        stren.append(((freqa[i])**2 + (freqb[i])**2) ** .5)
        phase.append(trig.arctan(freqa[i], freqb[i]))

    return stren, phase

sin = []
for i in range(100):
    sin.append(trig.sine(i, 5, 1, 10))

x,y = DFT(sin)

print(x,y)