# DSP From Scratch

A signal processing library built from the ground up in Python. No NumPy, no SciPy, no external math libraries. Every trig function is computed from Taylor series, every algorithm is written by hand.

## Why

Most DSP libraries treat core algorithms like black boxes — you call `np.fft.fft()` and get an answer. I wanted to understand what's actually happening under the hood, so I built the whole thing myself. The trig functions, the transforms, the signal generators, all of it.

## What's In Here

### trig.py — Math Library
All the trig functions computed from Taylor series. No `math.sin`, no `math.cos`. Just power series and basic arithmetic.
- `sin`, `cos`, `tan` — Taylor series, 25 terms
- `arctan`, `arccos` — inverse trig with quadrant handling
- `wrap` — angle normalization to [-π, π]
- `sine`, `cosine`, `square`, `saw` — signal generators for testing

### signals.py — DSP Algorithms
- **DFT** — O(N²) Discrete Fourier Transform using real-valued sine and cosine correlations. No complex numbers.
- **FFT** — O(N log N) Cooley-Tukey recursive implementation. Same real-valued approach, with automatic zero-padding to the next power of 2.
- **Noise Generator** — pseudorandom noise using a linear congruential generator. Also built from scratch.

## How It Works

Most implementations of the DFT use complex exponentials. This one doesn't. Instead, each frequency bin is computed by correlating the input signal against a sine and a cosine separately, giving two real values per bin. Amplitude is recovered with the Pythagorean theorem, phase with arctangent. Same math, no imaginary numbers.

The FFT splits the signal into even and odd indexed samples, recurses on each half, and recombines them using twiddle factors computed from the trig library. The combination step adjusts the odd half's sine/cosine pair by a rotation angle before adding/subtracting from the even half.


## What's Next
- FIR / IIR filter design
- Windowing functions (Hamming, Hann, Blackman)
- Convolution
- AM/FM modulation and demodulation
- Inverse FFT

## Interactive Demo
The portfolio page has a live DFT calculator where you can build signals and watch the frequency spectrum update in real time. Check it out [here](https://thebestjacklambert.github.io/Project10/Project10.html).
