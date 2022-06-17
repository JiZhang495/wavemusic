#include <cmath>
#ifdef DEBUG
#include <iomanip>
#include <cassert>
#endif

#include "sigen.h"

f_lut_t note_t::construct_lut() {
    f_lut_t f_lut = {
        {"C-", -10}, {"C", -9}, {"C+", -8},
        {"D-",  -8}, {"D", -7}, {"D+", -6},
        {"E-",  -6}, {"E", -5}, {"E+", -4},
        {"F-",  -5}, {"F", -4}, {"F+", -3},
        {"G-",  -3}, {"G", -2}, {"G+", -1},
        {"A-",  -1}, {"A",  0}, {"A+",  1},
        {"B-",   1}, {"B",  2}, {"B+",  3},
    };

    for (auto &i: f_lut) { i.second = 440.0 * pow(2.0, i.second/12); }

    return f_lut;
}

// TODO: remove octave from class and calculate frequency before construction?
note_t::note_t(shape_t s, int l, std::string n, int o) {
    static f_lut_t f_lut = construct_lut();
    shape  = s;
    length = l;
    name   = n;
    octave = o;
    freq   = f_lut[n] * pow(2.0, octave-4);
}

// TODO: pass in 2 data points instead of the whole piece if that's faster?
std::vector<int16_t> lowpass(std::vector<int16_t> &pcm_data) {
    std::vector<int16_t> pcm_out;
    // time constant RC = 1/(2πf)
    const float RC = 1/(2*M_PI*LPF_FC);
    // smoothing factor α = dt/(RC+dt)
    const float alpha = 1 / (RC*S_RATE + 1);
    int16_t prev_out = 0;
    // y[i] = α * x[i] + (1-α) * y[i-1]
    for (const auto &sample: pcm_data) {
        pcm_out.push_back((alpha * sample) + ((1-alpha) * prev_out));
        prev_out = pcm_out.back();
    }
    return pcm_out;
}

// TODO: add decay and sustain and rename to ADSR
float filter(int i, int s_len) {
    // assume 99% volume change by 0.02s
    // k = -0.02/ln(0.01) = 0.004343
    static float k = -(0.02*S_RATE/log(0.01));
    static int atk_start  = 0.02*S_RATE;
    #ifdef DEBUG
    assert(s_len > 2*atk_start);
    #endif
    int rel_start = s_len - atk_start;
    int j = i; // cast to signed int
    float gain;
    if (i < atk_start) {
        // attack curve
        // y = 1 - e^(-t/k)
        gain = 1.0-exp(-j/k);
    } else if (i > rel_start) {
        // release curve in seconds
        // y = e^(-((t-0.02)/k))
        gain = exp(-((j-rel_start)/k));
    } else {
        // flat sustain
        gain = 1.0;
    }
    return gain;
}

// write one note with note_t
void play(std::vector<int16_t> &pcm_data, int &ptr, note_t note, bool first) {
    play(pcm_data, ptr, note.shape, note.length, note.freq, first);
}

// write one note with note parameters
// signal generator -> attack/release gain filter -> output
void play(std::vector<int16_t> &pcm_data, int &ptr, shape_t shape,
          int length, float freq, bool first) {

    #ifdef DEBUG
    assert(length != 0);
    if (shape != none) { assert(freq != 0.0); }
    #endif

    float wave = 0.0;
    float gain;
    int16_t pcm_out;
    static float smqvr = 15.0/BPM;
    int s_len      = rint(smqvr*length*S_RATE); // length in number of samples
    bool sign      = true;
    float period   = S_RATE/freq;
    float gradient = 2.0/period;
    float count    = 0.0;

    #ifdef DEBUG
    assert(first || ((ptr + s_len - 1) < pcm_data.size()));
    #endif
    for (int i = 0; i < s_len; ++i) {
        // generate base signal
        switch (shape) {
            case none:
                wave = 0;
                break;

            case sine:
                wave = (float)SIN_AMP * sin(2.0*M_PI*freq*i/S_RATE);
                break;

            case square:
                if (sign) {
                    wave = SQR_AMP;
                } else {
                    wave = -SQR_AMP;
                }

                count += 2.0;
                if (count > period) {
                    count = 0.0;
                    sign = !sign;
                }
                break;

            case triangle:
                wave = count * gradient * TRI_AMP - TRI_AMP;
                if (!sign) {
                    wave = -wave;
                }

                count += 2.0;
                if (count > period) {
                    count = 0.0;
                    sign = !sign;
                }
                break;

            case saw:
                wave = count * gradient * SAW_AMP - SAW_AMP;
                count += 1.0;
                if (count > period) {
                    count = 0.0;
                }
                break;
        }

        // apply attack/release filter
        if (shape == none) {
            gain = 0;
        } else {
            gain = filter(i, s_len);
        }

        // write or overwrite data depending on if its first stave
        pcm_out = gain * wave;
        if (first) {
            pcm_data.push_back(pcm_out);
        } else {
            pcm_data[ptr + i] += pcm_out;
        }
    }
    ptr += s_len;
}

#ifdef DEBUG
std::ostream &operator<<(std::ostream &os, shape_t shape) {
    switch (shape) {
        case none:     return os << "rest";
        case sine:     return os << "sine" ;
        case square:   return os << "square";
        case triangle: return os << "triangle";
        case saw:      return os << "saw";
    };
    return os << "error";
}

std::ostream &operator<<(std::ostream &os, note_t const &note) {
    os << std::setw(8) << note.shape
       << std::setw(3) << note.length << ' '
       << std::left << std::setw(2) << note.name << std::right
       << std::setw(7) << std::fixed << std::setprecision(1) << note.freq
       << std::setw(2) << note.octave << std::endl;
    return os;
}

std::ostream &operator<<(std::ostream &os, std::vector<note_t> const &stave) {
    for (const auto &note: stave) {
        os << note;
    }
    return os;
}

std::ostream &operator<<(std::ostream &os, std::vector<std::vector<note_t>> const &score) {
    for (const auto &stave: score) {
        os << "=== stave break ===" << std::endl;
        os << stave << std::endl;
    }
    return os;
}
#endif
