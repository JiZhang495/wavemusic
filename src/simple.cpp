#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <unordered_map>
#include <cmath>
#include <cassert>
#include <vector>
#include <regex>

#define S_RATE 44100
#define BPM 100
#define SIN_AMP 6000
#define SQR_AMP 2000
#define SAW_AMP 3000

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

    note_t(shape_t s, unsigned int l, std::string n, int o) {
        static f_lut_t f_lut = construct_lut();
        shape  = s;
        length = l;
        name   = n;
        octave = o;
        freq   = f_lut[n] * pow(2.0, octave-4);
    }
};

// debug code, use if DEBUG in the future
std::ostream &operator<<(std::ostream& os, shape_t shape) {
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

// write one note with note parameters
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, shape_t shape,
          unsigned int length, float freq, int octave, bool first) {

    assert(length != 0);
    if (shape != none) { assert(freq != 0.0 && octave != 0); }

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

// write one note with note_t
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, note_t note, bool first) {
    play(pcm_data, ptr, note.shape, note.length, note.freq, note.octave, first);
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

    // No guards against these bad inputs, won't fix just git gud plz
    //   - first note without octave value
    //   - invalid instrument/note name
    //   - first stave not longest
    //   - bad barline positions (parser ignores barlines)
    // TODO: add persistent length settings
    std::string str_in =                                 "\
    square:                                             \n\
        4b3 2c+4 2E 4f+ 4g+    | 16G+4                  \n\
        4b3 2c+4 2e 4f+ 4g+    | 6g+ 2f+ 4f+ 2b3 2b     \n\
    saw:                                                \n\
        4b2 4e3      4f+3 4g+3 | 4b3 4c+4  4E   4F+     \n\
        4e4 2r  2c+4 4b3  4g+  | 4e3 4c+3  4b2  4a2     \n\
    sine:                                               \n\
        8e2          8b        | 8c+3      8g+2         \n\
        8a2          8g+       | 8F+2      8b2          \n\
    ";

    std::regex rgx_delim("[\\s|\\|]+");
    std::regex rgx_note("(\\d+)([A-Ga-gRr][+-]?)(\\d+)?");
    std::smatch matches;
    std::vector<note_t> stave;
    std::vector<std::vector<note_t>> score;

    std::sregex_token_iterator iter(str_in.begin(), str_in.end(), rgx_delim, -1);
    std::sregex_token_iterator end;

    shape_t s;
    unsigned int l;
    std::string n;
    int o;

    for (; iter != end; ++iter) {
        std::string token = *iter;
        // instrument headers
        if (token.back() == ':') {
            if (token == "sine:") {
                s = sine;
            } else if (token == "square:") {
                s = square;
            } else if (token == "triangle:") {
                s = triangle;
            } else if (token == "saw:") {
                s = saw;
            }
            if (!stave.empty()) {
                score.push_back(stave);
                stave.clear();
            }
        // notes
        } else {
            if (std::regex_match(token, matches, rgx_note)) {
                l = std::stoi(matches[1]);
                n = matches[2];
                for (auto &c: n) {
                    c = std::toupper(c);
                }
                // why cannot use .empty()?
                if (matches[3] == "") {
                    // rests
                    if (matches[2] == "r") {
                        stave.push_back({none, l, n, 0});
                        continue;
                    }
                    // keep octave
                } else {
                    o = std::stoi(matches[3]);
                }
                stave.push_back({s, l, n, o});
            }
        }
    }
    if (!stave.empty()) {
        score.push_back(stave);
        stave.clear();
    }
    std::cout << score;

    // data_size depends on length of first stave
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
