#include <iostream>
#include <fstream>
#include <string>
#include <cassert>
#include <vector>
#include <regex>

#include "sigen.h"

#define FILE_NAME "m.wav"

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

int main(void) {
    static_assert(sizeof(wav_hdr_t) == 44, "wav_hdr_t size error");

    // write file
    wav_hdr_t wav_hdr;
    uint32_t data_size;
    std::vector<uint16_t> pcm_data;
    unsigned int ptr;

    std::ofstream f;
    f.open(FILE_NAME, std::ios::binary);
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

    shape_t s = none;
    unsigned int l;
    std::string n;
    int o = 4;

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
    #ifdef DEBUG
    std::cout << score;
    #endif

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

    // play wav with system call
    bool played = false;
    int rvalue = -1;
    #ifdef __APPLE__
    rvalue = system("afplay " FILE_NAME " &");
    if(rvalue == 0) { played = true; }

    #elif __linux__
    // check if aplay exists
    rvalue = system("command -v aplay > /dev/null");
    if (rvalue == 0) {
        rvalue = system("aplay " FILE_NAME " &");
        if(rvalue == 0) { played = true; }
    }

    #endif

    if (!played) {
        std::cout << "unsupported OS, please manually start playback of m.wav" << std::endl;
    }

    return 0;
}
