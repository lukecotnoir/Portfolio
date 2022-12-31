"""
A class to handle calculating FFT data for given signals

"""
import cmath #complex math
import math
import time
import numpy as np


class FFT:
    """
    Class handling some standard FFT implementations with timing
    """
    def __init__(self, sample_times=None, signal=None):
        print("  Calling __init__ for FFT")

        # Use assert to limit allowable data types
        assert isinstance(sample_times, np.ndarray), "Only Numpy arrays allowed for time"
        assert isinstance(signal, np.ndarray), "Only Numpy arrays allowed for signal"
        assert len(sample_times.shape)==1, "Only 1D time arrays allowed"
        assert len(signal.shape)==1, "Only 1D signal arrays allowed"
        assert sample_times.dtype == np.float64, "Only double precision (float64) allowed"
        assert signal.dtype == np.float64, "Only double precision (float64) allowed"
        assert sample_times.shape[0] == signal.shape[0], "time and signal must be same shape"

        self._time = sample_times
        self._signal = signal

    def __len__(self):
        """
        Return the length of signal vector
        """
        return self._time.shape[0]

    def get_fourier_components(self, num_terms=6):
        """
        Get the most significant components from Fourier Transform
        :param num_terms: Number of terms to consider
        """

        num_samples = 2**int(math.log2(len(self))) # largest power of two
        all_components, _ = self.numpy_fft(num_samples)

        print("num samples = ", num_samples)
        print(all_components[:6])

        # Only get the first N//2 terms to consider (due to symmetry)
        selected_components = all_components[:len(all_components) // 2]  # create copy

        # Sort a list of tuples by the first element of each (by default)
        # reverse so biggest to smallest
        selected_components.sort(reverse=True)  # Sort list of tuples by first element by default
        selected_components = selected_components[:num_terms]
        print(selected_components)
        return selected_components

    def naive_dft(self, num_samples=64):
        """
        Naive Discrete Fourier Transform
        :param: num_samples - Number of samples to consider from signal (power of 2)
        :return: list of (amplitude, frequency, phase) tuples, and timing data
        """


        # get rid of pylint warn
        print(f"Need to overload this with num_samples={num_samples} {len(self._time)}")
        return None, None  # You need to handle this one!

    def numpy_fft(self, num_samples=64):
        """
        fft implementation from Numpy (with timing goodness and consistent data format)
        :param: num_samples - Number of samples to consider from signal (power of 2)
        :return: list of (amplitude, frequency, phase) tuples, and timing data
        """
        assert num_samples <= len(self), "Must not request too many samples"

        # Setup num samples is constant, so keep outside timing loop
        xd = self._signal[:num_samples]
        n = len(xd)
        assert FFT.__is_pow2(len(xd))  # This only defined for power of 2 data size

        start_time = time.perf_counter()  # Grab time when we start FFT calc
        complex_val = np.fft.fft(xd)
        end_time = time.perf_counter() # Grab time at end of FFT calc

        # This extraction should be constant, so keep outside timing loop
        mag = [abs(c) * 2.0 / n for c in complex_val[:num_samples]]  # Scale according
        wr = [2*np.pi*r/num_samples for r in range(num_samples)]
        ph = [cmath.phase(c) for c in complex_val[:num_samples]]
        ph = [math.atan2(c.imag, c.real) for c in complex_val[:num_samples]]
        all_components = [(mag[i], wr[i], ph[i]) for i in range(num_samples)]

        return all_components, end_time-start_time

    def cooley_turkey_fft(self, num_samples=64):
        """
        Cooley-Turkey fft implementation
        :param: num_samples - Number of samples to consider from signal (power of 2)
        :return: list of (amplitude, frequency, phase) tuples, and timing data
        """
        assert num_samples <= len(self), "Must not request too many samples"

        # Setup num samples is constant, so keep outside timing loop
        xd = self._signal[:num_samples]
        n = len(xd)
        assert FFT.__is_pow2(len(xd))  # This only defined for power of 2 data size

        start_time = time.perf_counter() # Grab time when we start FFT calc
        rs = FFT.__fft_(xd, len(xd))

        end_time = time.perf_counter() # Grab time at end of FFT calc

        # This extraction should be constant, so keep outside timing loop
        mag = [abs(c) * 2.0 / n for c in rs[:num_samples]]  # Scale according to sample period
        wr = [2*np.pi*r/num_samples for r in range(num_samples)]
        ph = [cmath.phase(c) for c in rs[:num_samples]]
        all_components = [(mag[i], wr[i], ph[i]) for i in range(num_samples)]

        return all_components, end_time-start_time



    def simple_dft(self, num_samples=64):
        """
        Simple dFT
        :param: num_samples - Number of samples to consider from signal (power of 2)
        :return: list of (amplitude, frequency, phase) tuples, and timing data
        """
        assert num_samples <= len(self), "Must not request too many samples"

        # Setup num samples is constant, so keep outside timing loop
        xd = self._signal[:num_samples]
        n = len(xd)
        assert FFT.__is_pow2(len(xd))  # This only defined for power of 2 data size

        start_time = time.perf_counter()  # Grab time when we start FFT calc
        dft2 = [sum((xd[k] * FFT.__iexp(-2*math.pi*i*k/n) for k in range(n))) for i in range(n)]
        end_time = time.perf_counter()  # Grab time at end of FFT calc

        # This extraction should be constant, so keep outside timing loop
        mag  = [abs(c)*2.0/n for c in dft2] # Scale according to sample period
        ph   = [cmath.phase(c) for c in dft2]
        wr = [2 * np.pi * r / num_samples for r in range(num_samples)]
        all_components = [(mag[i], wr[i], ph[i]) for i in range(num_samples)]

        return all_components, end_time - start_time


    ## The below code works, and is based on
    ## https://gist.github.com/bellbind/1505153
    ## These are helper methods and provided to support above implementations
    ## ----------------------------------------------------------------------
    @staticmethod
    def __iexp(n):
        return complex(math.cos(n), math.sin(n))

    @staticmethod
    def __is_pow2(n):
        return n > 0 and not (n & n-1) # Bitwise check

    @staticmethod
    def __fft_(xs, n, start=0, stride=1):
        """
        cooley-turkey fft recursive helper method
        NOTE: More about recursion later in CPSC 250 or 255
        """
        if n == 1:
            return [xs[start]]
        hn, sd = n // 2, stride * 2

        # This is making a recursive call (more on recursion later in semester)
        rs = FFT.__fft_(xs, hn, start, sd) + FFT.__fft_(xs, hn, start + stride, sd)

        for i in range(hn):
            e = FFT.__iexp(-2 * math.pi * i / n)
            rs[i], rs[i + hn] = rs[i] + e * rs[i + hn], rs[i] - e * rs[i + hn]

        return rs
