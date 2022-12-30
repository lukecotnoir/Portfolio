import os
import struct

import matplotlib.pyplot as plt
import numpy as np

from given.fft import FFT


def read_binary(file_path):
    print(f"Reading data from {file_path}")
    with open(file_path, "rb") as fin:
        byte_array = fin.read()

        format_string = ">iid"
        chunk_size = struct.calcsize(format_string)
        num_chunks = len(byte_array) // chunk_size

        seconds = []
        nanoseconds = []
        signal = []
        for i in range(num_chunks):
            data = struct.unpack(format_string, byte_array[i * chunk_size:(i + 1) * chunk_size])
            seconds.append(data[0])
            nanoseconds.append(data[1])
            signal.append(data[2])

        return np.array(seconds) - seconds[0] + 1.0e-9 * np.array(nanoseconds), np.array(signal)


if __name__ == '__main__':

    base_name = "signal_7"
    file_path = os.path.join("data", "noisy_"+base_name+".dat")

    time, signal = read_binary(file_path)

    print(time[:10])
    print(signal[:10])

    fft = FFT(time, signal)
    fourier_series_components = fft.get_fourier_components(7)
    print(fourier_series_components)

    fig = plt.figure(1)
    plt.plot(time, signal, 'b-', label="signal", linewidth=2)
    plt.legend()
    plt.xlabel('time (s)')
    plt.ylabel('signal')
    plt.title('Signal Data (first.last.yy)')

    fourier_series = np.zeros(fft._time.shape)
    dt = time[1] - time[0]
    print("Fourier Components:")
    for components in fourier_series_components:
        mag, freq, phase = components
        print(f"{mag:8.3f}, {freq / dt:8.3f}, {phase:8.3f}")

        # Be sure to convert sample frequency to time domain
        fourier_series += mag * np.cos((freq / dt) * fft._time + phase)

    plt.plot(time, fourier_series, '-', label="Fourier Series")

    plt.legend()
    plt.show()
