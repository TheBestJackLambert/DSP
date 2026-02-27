pi = 3.14159265359159
e = 2.718281828459045

#standard deviation function
def sd(x):
  mean = 0
  for i in x:
    mean += i
  mean /= len(x)
  deviation = 0
  for i in x:
    deviation += (i - mean) ** 2
  deviation /= len(x)
  return deviation ** .5

def correlation(x, y):
  meanx = 0
  meany = 0
  N = len(x)
  squaresum = 0
  residual = 0
  for i in range(N):
    meanx += x[i]
    meany += y[i]
  meanx /= N
  meany /= N
  for i in range(N):
    squaresum += (x[i] - meanx) ** 2
    residual += (x[i] - y[i]) ** 2
  fraction = residual / squaresum
  if squaresum == 0:
    return 0
  return 1 - fraction

#defines amount of iterations (recommended 25)
iterations = 25

#factorial
def fac(x):
  y = 1
  for i in range(1, x+1):
    y *= i
  return y

#cosine function
def cos(x):
  global iterations 
  x = wrap(x)
  y = 0
  for i in range(iterations):
    y += 1/(fac(2*i)) * x ** (2*i) * (-1)**i
  return y

#sine function
def sin(x):
  global iterations
  x = wrap(x)
  y = 0
  for i in range(iterations):
    y += 1/(fac(1 + 2*i)) * x ** (2*i + 1) * (-1)**i
  return y

#tan function
def tan(x):
  y = sin(x)/cos(x)
  return y

#arccos function
def arccos(x, y):
  b = abs((x**2-y**2))**.5/y
  c = arctan(y, b)
  return c

#mod along pi
def wrap(a):
  a = (a + pi) % (2 * pi) - pi
  return a

#inverse tangent
def arctan(x, y):
  global iterations
  #if denominator is zero returns corresponding angle
  if x == 0:
    if y > 0: return (pi/2)
    if y < 0: return (-pi/2)
    return 0.0
  u = y / x

  #determines sign of angle
  sgn = 1.0 if u >= 0 else -1.0
  t = abs(u)
  inv = False

  #if y>x flips it or easier compute and signals for unflip later on
  if t > 1.0:
    inv = True
    t = 1.0 / t
  a = 0.0

  #does taylor series 20 times
  for i in range(iterations):
    a += ((-1)**i) * (t**(2*i + 1)) / (2*i + 1)

  #adjusts for sign
  a = sgn * ( (pi/2) - a ) if inv else sgn * a

  #puts in correct quadrant
  if x < 0 and y >= 0: a += pi
  elif x < 0 and y < 0: a -= pi
  return a


def sine(x, freq, N, phase, amp):
    return sin(x * 2 * pi * freq / N + phase) * amp

def cosine(x, freq, N, phase, amp):
    return cos(x * 2 * pi * freq / N + phase) * amp

def square(x, freq, N, phase, amp):
  a = 0
  global iterations
  for i in range(1, 10 * iterations):
    a += sin(2 * pi * (2 * i - 1) * freq * x / N) / (2 * i - 1)
  return a * 4 * amp / pi

def saw(x, freq, N, phase, amp):
  global iterations
  a = 0
  for i in range(1, 10 * iterations):
    if i % 2 == 0:
      a -= sin(2 * pi * x * i * freq / N) / (i)
    elif i % 2 == 1:
      a += sin(2 * pi * x * i * freq / N) / (i)
  return a * 2 * amp / pi


