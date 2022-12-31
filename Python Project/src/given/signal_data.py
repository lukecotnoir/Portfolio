"""
Script for generating data for Lab10
"""
import os
import random
import struct
import time
import matplotlib.pyplot as plt
import numpy as np
import csv

formats = ['<iid', '>iid']
format_string = random.choice(formats)  # Secret format - do some detective work on file!

def write_data_as_binary(sample_times, signal_clean, signal_noisy, signal_id, folder_name="data"):
    try:
        #print(f"Writing signal {signal_id} data to files ... ")

        fractional, whole = np.modf(sample_times)
        now = int(time.time())

        #print(" set whole secs ...")
        time_sec = now + whole
        #print(time_sec)

        #print(" set nanoseconds ...")
        time_ns = fractional * 10**9

        #print("write clean ...")
        byte_array = bytearray()
        for i in range(len(sample_times)):
            byte_array.extend(struct.pack(format_string,
                                          int(time_sec[i]), int(time_ns[i]), signal_clean[i]))

        with open(os.path.join(folder_name, f'clean_signal_{signal_id:d}.dat'), "wb") as fout:
            fout.write(byte_array)

        #print("write noisy ...")
        byte_array = bytearray()
        for i in range(len(sample_times)):
            byte_array.extend(struct.pack(format_string,
                                          int(time_sec[i]), int(time_ns[i]), signal_noisy[i]))

        with open(os.path.join(folder_name, f'noisy_signal_{signal_id:d}.dat'), "wb") as fout:
            fout.write(byte_array)

        #print("Success!")
        return True

    except Exception as e:
        print(" Failed to write the signal data to file!")
        print(e)
        return False

def write_data_as_csv(sample_times, signal_clean, signal_noisy, signal_id, folder_name="data"):
    try:
        #print(f"Writing signal {signal_id} data to files ... ")

        fractional, whole = np.modf(sample_times)
        now = int(time.time())

        #print(" set whole secs ...")
        time_sec = now + whole
        #print(time_sec)

        #print(" set nanoseconds ...")
        time_ns = fractional * 10**9

        #print("write clean ...")

        with open(os.path.join(folder_name, f'clean_signal_{signal_id:d}.csv'), "wt") as fout:
            writer = csv.writer(fout, delimiter=",")
            for i in range(len(sample_times)):
                writer.writerow([int(time_sec[i]), int(time_ns[i]), signal_clean[i]])

        #print("write noisy ...")
        with open(os.path.join(folder_name, f'noisy_signal_{signal_id:d}.csv'), "wt") as fout:
            writer = csv.writer(fout, delimiter=",")
            for i in range(len(sample_times)):
                writer.writerow([int(time_sec[i]), int(time_ns[i]), signal_noisy[i]])

        #print("Success!")
        return True

    except Exception as e:
        print(" Failed to write the signal data to file!")
        print(e)
        return False

def generate_signals(amp, freq, phase, end_time, num_samples=1024, noise_level=1.0):
    tv = np.linspace(0.0, end_time, num_samples)

    print(" Signal:")
    print("  Amp  : ", [f"{a:.4f}" for a in amp])
    print("  Freq : ", [f"{f:.4f}" for f in freq])
    print("  Phase: ", [f"{p:.4f}" for p in phase])

    signal = np.zeros(tv.shape)
    for i, amp in enumerate(amp):
        signal += amp * np.cos(freq[i] * tv + phase[i])

    noise = noise_level * (2.0 * np.random.random(signal.shape) - 1.0)

    return tv, signal, signal + noise


def generate_triangle_wave(num_terms, period):
    """
    Generate amplitude and frequency terms for a
    https://mathworld.wolfram.com/FourierSeriesTriangleWave.html

    :param num_terms: Number of terms in series
    :param period: time of one cycle
    :return : list of tuples of (amplitude and frequency)
    """

    av = []
    fv = []
    for n in range(1, 2*num_terms+1, 2):
        amp = (-1)**((n-1)/2) * 8./(np.pi**2 * n**2)
        freq = n*np.pi/period

        av.append(amp)
        fv.append(freq)
    return np.array(av), np.array(fv)


def generate_square_wave(num_terms, period):
    """
    Generate amplitude and frequency terms for a
    https://mathworld.wolfram.com/FourierSeriesSquareWave.html

    :param num_terms: Number of terms in series
    :param period: time of one cycle
    :return : list of tuples of (amplitude and frequency)
    """

    av = []
    fv = []
    for n in range(1, 2*num_terms+1, 2):
        amp = 4./(np.pi * n)
        freq = n*np.pi/period
        av.append(amp)
        fv.append(freq)
    return np.array(av), np.array(fv)


def generate_sawtooth_wave(num_terms, period):
    """
    Generate amplitude and frequency terms for a
    https://mathworld.wolfram.com/FourierSeriesSawtoothWave.html

    :param num_terms: Number of terms in series
    :param period: time of one cycle
    :return : list of tuples of (amplitude, frequency)
    """

    av = []
    fv = []
    for n in range(1, num_terms+1):
        av.append(1./(np.pi*n))
        fv.append(n*np.pi/period)
    return np.array(av), np.array(fv)


if __name__ == '__main__':
    signals = {}

    L = 5.0
    nv = range(1, 10, 2)
    fv = np.array([(n*2.0*np.pi/L)   for n in nv])
    av = np.array([(4.0/(n * np.pi)) for n in nv])
    signals[0] = [av, fv, 0*fv, 4*L, 1024, 1.0]  # amp, freq, phase, end_time, num_samples, noise
    signals[1] = [av, fv, 0*fv, 4*L, 1024, 3.0]  # amp, freq, phase, end_time, num_samples, noise

    # square
    L = 8.0
    av, fv = generate_square_wave(8, L)
    signals[2] = [av, fv, 0*fv, 2*L, 1024, 2.0*av[0]]
    signals[3] = [av, fv, 0*fv, 2*L, 1024, 8.0*av[0]]

    # triangle
    L = 6.0
    av, fv = generate_triangle_wave(6, L)
    signals[3] = [av, fv, 0*fv, 2.2*L, 1033, 0.25*av[0]]
    signals[4] = [av, fv, 0*fv, 2.2*L, 1033, av[0]]

    # sawtooth
    L = 7.0
    av, fv = generate_sawtooth_wave(7, L)
    signals[5] = [av, fv, 0*fv, 4.2*L, 1043, 1.25*av[0]]
    signals[6] = [av, fv, 0*fv, 4.2*L, 1043,  4.0*av[0]]

    # square w/ bias
    L = 5.0
    av, fv = generate_square_wave(6, L)
    av = [5.0] + av
    fv = [0.0] + fv
    signals[7] = [av, fv, 0*fv, 4*L, 1024, 5.0]
    signals[8] = [av, fv, 0*fv, 4*L, 1024, 15.0]

    for signal_id, signal_params in signals.items():
        print(f"Signal {signal_id} :")
        times, signal, noisy_signal = generate_signals(*signal_params)
        write_data_as_binary(times, signal, noisy_signal, signal_id)
        write_data_as_csv(times, signal, noisy_signal, signal_id)


#         fig = plt.figure()
#         plt.plot(times, noisy_signal, label="noisy")
#         plt.plot(times, signal, label='clean')
#         plt.title(f"Signal {signal_id} with {len(signal_params[0])} terms")
#         plt.legend()
#         fig.savefig(os.path.join("data", f"signal_{signal_id}.png"))
#
#
# plt.show()
