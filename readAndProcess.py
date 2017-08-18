#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import wave
import struct
import numpy
import csv
import sys
import os


def moments(x):
    mean = x.mean()
    std = x.var() ** 0.5
    skewness = ((x - mean) ** 3).mean() / std ** 3
    kurtosis = ((x - mean) ** 4).mean() / std ** 4
    return [mean, std, skewness, kurtosis]


def fftfeatures(wavdata):
    f = numpy.fft.fft(wavdata)
    f = f[2:f.size / 2 + 1]
    f = abs(f)
    total_power = f.sum()
    f = numpy.array_split(f, 10)
    return [e.sum() / total_power for e in f]


def features(x):
    x = numpy.array(x)
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))
    return f


def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""

    w = wave.open(wav_file)
    n = 60 * 10000
    if w.getnframes() < n * 2:
        raise ValueError('Wave file too short')
    frames = w.readframes(n)
    wav_data1 = struct.unpack('%dh' % n, frames)
    frames = w.readframes(n)
    wav_data2 = struct.unpack('%dh' % n, frames)
    return (wav_data1, wav_data2)


def compute_chunk_features(mp3_file):
    """Return feature vectors for two chunks of an MP3 file."""

    # Extract MP3 file to a mono, 10kHz WAV file

    mpg123_command = 'mpg123 -w "%s" -r 10000 -m "%s"'
    out_file = 'temp.wav'
    cmd = mpg123_command % (out_file, mp3_file)
    subprocess.call(cmd, shell=True)

    # Read in chunks of data from WAV file and remove temporary file

    (wav_data1, wav_data2) = read_wav(out_file)
    subprocess.call('rm ' + out_file, shell=True)
    return (features(wav_data1), features(wav_data2))


if __name__ == '__main__':
    cwd = os.getcwd()

    writer = csv.writer(open(cwd + '/featureOutput.csv', 'w'),
                        dialect='excel')
    csv_file = []

    csv_file.append([
        'name',
        'amp1mean',
        'amp1std',
        'amp1skew',
        'amp1kurt',
        'amp1dmean',
        'amp1dstd',
        'amp1dskew',
        'amp1dkurt',
        'amp10mean',
        'amp10std',
        'amp10skew',
        'amp10kurt',
        'amp10dmean',
        'amp10dstd',
        'amp10dskew',
        'amp10dkurt',
        'amp100mean',
        'amp100std',
        'amp100skew',
        'amp100kurt',
        'amp100dmean',
        'amp100dstd',
        'amp100dskew',
        'amp100dkurt',
        'amp1000mean',
        'amp1000std',
        'amp1000skew',
        'amp1000kurt',
        'amp1000dmean',
        'amp1000dstd',
        'amp1000dskew',
        'amp1000dkurt',
        'power1',
        'power2',
        'Power3',
        'power4',
        'power5',
        'power6',
        'power7',
        'power8',
        'power9',
        'power10',
        ])

    for (path, dirs, files) in os.walk(cwd + '/audio_files/'):
        for file in files:
            if not file.endswith('.mp3'):
                continue
            print 'Processing file :[%s]' % file
            mp3_file = os.path.join(path, file)

            # Extract the track name (i.e. the file name) plus the names
            # of the two preceding directories. This will be useful
            # later for plotting.

            (tail, track) = os.path.split(mp3_file)
            (tail, dir1) = os.path.split(tail)
            (tail, dir2) = os.path.split(tail)

            # Compute features. feature_vec1 and feature_vec2 are lists of floating
            # point numbers representing the statistical features we have extracted
            # from the raw sound data.

            (feature_vec1, feature_vec2) = \
                compute_chunk_features(mp3_file)

            feature_vec1.insert(0, file)
            csv_file.append(feature_vec1)

    writer.writerows(csv_file)
