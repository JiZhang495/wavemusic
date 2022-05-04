#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <cmath>
#include <cassert>
#include <vector>

#define S_RATE 44100
#define BPM 100
#define SIN_AMP 6000
#define SQR_AMP 2000
#define SAW_AMP 3000

// Forward declarations
typedef struct Wav_Header wav_hdr_t;
enum shape_t: uint8_t;
class note_t;
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, note_t note, bool first);
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, shape_t shape,
          unsigned int length, float freq, int octave, bool first);
float filter(int i, unsigned int s_len);

typedef struct Wav_Header {
    uint8_t  riff[4]       = {'R', 'I', 'F', 'F'};
    uint32_t file_size     = 0;                  // calculate and fill in later
    uint8_t  wave[4]       = {'W', 'A', 'V', 'E'};
    uint8_t  fmt[4]        = {'f', 'm', 't', ' '};
    uint32_t fmt_size      = 16;
    uint16_t wav_format    = 1;                  // PCM
    uint16_t channel_cnt   = 1;
    uint32_t sample_freq   = S_RATE;
    uint32_t data_rate     = S_RATE * 2;         // 2 bytes per sample
    uint16_t block_align   = 2;                  // 16-bit mono
    uint16_t bits_per_samp = 16;
    uint8_t  data[4]       = {'d', 'a', 't', 'a'};
    uint32_t data_size     = 0;                  // calculate and fill in later
} wav_hdr_t;

enum shape_t: uint8_t {none, sine, square, triangle, saw};

class note_t {
private:
    // build frequency look-up table
    typedef std::unordered_map<std::string, float> f_lut_t;
    static f_lut_t construct_lut() {
        f_lut_t f_lut = {
            {"C-", -10}, {"C", -9}, {"C+", -8},
            {"D-",  -8}, {"D", -7}, {"D+", -6},
            {"E-",  -6}, {"E", -5}, {"E+", -4},
            {"F-",  -5}, {"F", -4}, {"F+", -3},
            {"G-",  -3}, {"G", -2}, {"G+", -1},
            {"A-",  -1}, {"A",  0}, {"A+", 1},
            {"B-",   1}, {"B",  2}, {"B+", 3},
        };

        for (auto &i: f_lut) { i.second = 440.0 * pow(2.0, i.second/12); }

        return f_lut;
    }

public:
    shape_t      shape;
    unsigned int length;
    std::string  name;
    int          octave;
    float        freq;

    note_t(shape_t s, unsigned int l, std::string n = "X", int o = 0) {
        static f_lut_t f_lut = construct_lut();
        shape  = s;
        length = l;
        name   = n;
        octave = o;
        freq   = f_lut[n];
    }
};

// TODO: separate sustain section where gain = 1 to avoid exp calculation at every sample
float filter(int i, unsigned int s_len) {
    // assume 99% volume reduction by 0.02s
    // k = -0.02/ln(0.01) = 0.004343
    static float k = -(0.02*S_RATE/log(0.01));
    int rel_start = s_len - (int)(0.02*S_RATE);
    float gain;
    if (i > rel_start) {
        // release curve in seconds
        // y = e^(-(t-0.02)/k)
        gain = exp((rel_start-i)/k);
    } else {
        // attack and sustain curve
        // y = 1 - e^(-t/k)
        gain = 1.0-exp(-i/k);
    }
    return gain;
}

// write one note with note_t
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, note_t note, bool first) {
    play(pcm_data, ptr, note.shape, note.length, note.freq, note.octave, first);
}

// write one note with note parameters
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, shape_t shape,
          unsigned int length, float freq = 0.0, int octave = 4, bool first = false) {

    assert(length != 0);
    if (shape != none) { assert(freq != 0.0 && octave != 0); }

    freq = freq * pow(2.0, octave-4);
    float wave;
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
            gain = filter((int)i, s_len);
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

int main(void) {
    static_assert(sizeof(wav_hdr_t) == 44, "wav_hdr_t size error");

    // write file
    wav_hdr_t wav_hdr;
    uint32_t data_size;
    std::vector<uint16_t> pcm_data;
    unsigned int ptr;

    std::ofstream f;
    f.open("m.wav", std::ios::binary);
    f.write(reinterpret_cast<const char *>(&wav_hdr), sizeof(wav_hdr_t));

    std::vector<std::vector<note_t>> score = {
        // stave 1
        { {square, 4,  "B",  3},
          {square, 2,  "C+", 4},
          {square, 2,  "E",  4},
          {square, 4,  "F+", 4},
          {square, 4,  "G+", 4},

          {square, 16, "G+", 4},

          {square, 4,  "B",  3},
          {square, 2,  "C+", 4},
          {square, 2,  "E",  4},
          {square, 4,  "F+", 4},
          {square, 4,  "G+", 4},

          {square, 6,  "G+", 4},
          {square, 2,  "F+", 4},
          {square, 4,  "F+", 4},
          {square, 2,  "B",  3},
          {square, 2,  "B",  3},
        },

        // stave 2
        { {saw, 4,  "B",  2},
          {saw, 4,  "E",  3},
          {saw, 4,  "F+", 3},
          {saw, 4,  "G+", 3},

          {saw, 4,  "B",  3},
          {saw, 4,  "C+", 4},
          {saw, 4,  "E",  4},
          {saw, 4,  "F+", 4},

          {saw, 4,  "E",  4},
          {saw, 4,  "C+", 4}, // overlaps with C+ in stave 1, sounds a bit weird
          {saw, 4,  "B",  3},
          {saw, 4,  "G+", 3},

          {saw, 4,  "E",  3},
          {saw, 4,  "C+", 3},
          {saw, 4,  "B",  2},
          {saw, 4,  "A",  2},
        },

        // stave 3
        { {sine, 8, "E",  2},
          {sine, 8, "B",  2},

          {sine, 8, "C+", 2},
          {sine, 8, "G+", 2},

          {sine, 8, "A",  2},
          {sine, 8, "G+", 2},

          {sine, 8, "F+", 2},
          {sine, 8, "B",  2},
        }
    };

    // data_size depends on length of first stave
    // NOTE: dangerous if first stave isn't the longest. fix
    bool first = true;
    for (const auto &stave: score) {
        for (const auto &note: stave) {
            play(pcm_data, ptr, note, first);
        }
        first = false;
        ptr = 0;
    }

    for (const auto &sample: pcm_data) {
        f.write(reinterpret_cast<const char *>(&sample), sizeof(uint16_t));
    }
    data_size = pcm_data.size() * sizeof(uint16_t);

    // calculate header and overwrite with correct size bits
    wav_hdr.data_size = data_size;
    wav_hdr.file_size = data_size + 32;
    f.seekp(0);
    f.write(reinterpret_cast<const char *>(&wav_hdr), sizeof(wav_hdr_t));
    f.close();

    return 0;
}

