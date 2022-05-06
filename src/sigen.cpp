#ifdef DEBUG
#include <iomanip>
#endif
#include <cmath>
#include <cassert>

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

note_t::note_t(shape_t s, unsigned int l, std::string n, int o) {
    static f_lut_t f_lut = construct_lut();
    shape  = s;
    length = l;
    name   = n;
    octave = o;
    freq   = f_lut[n] * pow(2.0, octave-4);
}

float filter(unsigned int i, unsigned int s_len) {
    // assume 99% volume change by 0.02s
    // k = -0.02/ln(0.01) = 0.004343
    static float k = -(0.02*S_RATE/log(0.01));
    static unsigned int atk_start  = 0.02*S_RATE;
    assert(s_len > 2*atk_start);
    unsigned int rel_start = s_len - atk_start;
    int j = i; // cast to signed int
    float gain;
    if (i < atk_start) {
        // attack curve
        // y = 1 - e^(-t/k)
        gain = 1.0-exp(-j/k);
    } else if (i > rel_start) {
        // release curve in seconds
        // y = e^(-(t-0.02)/k)
        gain = exp((rel_start-j)/k);
    } else {
        // flat sustain
        gain = 1.0;
    }
    return gain;
}

// write one note with note_t
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, note_t note, bool first) {
    play(pcm_data, ptr, note.shape, note.length, note.freq, note.octave, first);
}

// write one note with note parameters
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, shape_t shape,
          unsigned int length, float freq, int octave, bool first) {

    assert(length != 0);
    if (shape != none) { assert(freq != 0.0 && octave != 0); }

    float wave = 0.0; // can remove this initialisation after trig wave done
    float gain;
    int16_t pcm_out;
    static float smqvr = 15.0/BPM;
    unsigned int s_len = rint(smqvr*length*S_RATE); // length in number of samples

    bool sign;
    float period;
    float count;
    float gradient;
    // initialise variables
    switch (shape) {
        case none:
        case sine:
            break;
        case square:
            sign = true;
            period = S_RATE/freq/2.0;
            count = 0.0;
            break;
        case triangle:
            // TODO
            break;
        case saw:
            period = S_RATE/freq;
            gradient = 2.0*(float)SAW_AMP/period;
            count = 0.0;
            break;
    }

    assert(first || ((ptr + s_len - 1) < pcm_data.size()));
    for (unsigned int i = 0; i < s_len; ++i) {
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

                count += 1.0;
                if (count > period) {
                    count = 0.0;
                    sign = !sign;
                }
                break;

            case triangle:
                // TODO
                break;

            case saw:
                wave = count * gradient - SAW_AMP;
                count += 1.0;
                if (count > period) {
                    count = 0.0;
                }
                break;
        }
        if (shape == none) {
            gain = 0;
        } else {
            gain = filter(i, s_len);
        }

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
