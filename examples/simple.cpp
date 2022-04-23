#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <cmath>

#define S_RATE 44100
#define BPM 100

typedef struct WAV_HEADER {
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

// make a square wave
void square(std::ofstream& fout, uint32_t& data_size,
            unsigned int length, unsigned int freq) {
    uint16_t pcm_data;
    bool sign = true;
    float half_period = S_RATE/(freq/2.0);
    float count = half_period;
    float smqvr = 15.0/BPM;
    float s_len = smqvr*length*S_RATE; // length in number of samples

    for(unsigned int i = 0; i < round(s_len); ++i) {
        if (sign) {
            pcm_data = 2000;
        } else {
            pcm_data = -2000;
        }
        fout.write(reinterpret_cast<char *>(&pcm_data), sizeof(uint16_t));
        data_size += sizeof(uint16_t);

        count -= 1.0;
        if (count < 0) {
            count += half_period;
            sign = !sign;
        }
    }
}

int main(void) {
    static_assert(sizeof(wav_hdr_t) == 44, "wav_hdr_t size error");

    // build frequency look-up table
    std::unordered_map<std::string, float> freq_lut = {
        {"C", -9}, {"Cs", -8}, {"Db", -8}, {"D", -7}, {"Ds", -6}, {"Eb", -6},
        {"E", -5}, {"F", -4}, {"Fs", -3}, {"Gb", -3}, {"G", -2}, {"Gs", -1},
        {"Ab", -1}, {"A", 0}, {"As", 1}, {"Bb", 1}, {"B", 2}
    };

    for(auto& i : freq_lut) {
        i.second = 440.0 * pow(2.0, i.second/12);
    }

    wav_hdr_t wav_hdr;
    uint32_t data_size = 0;

    // write file
    std::ofstream fout;
    fout.open("m.wav", std::ios::binary);
    fout.write(reinterpret_cast<const char *>(&wav_hdr), sizeof(wav_hdr_t));

    square(fout, data_size, 2, freq_lut["C"]);
    square(fout, data_size, 2, freq_lut["Eb"]);
    square(fout, data_size, 2, freq_lut["F"]);
    square(fout, data_size, 2, freq_lut["G"]);
    square(fout, data_size, 2, freq_lut["A"]);
    square(fout, data_size, 4, freq_lut["C"]);

    // calculate header and overwrite with correct size bits
    wav_hdr.data_size = data_size;
    wav_hdr.file_size = data_size + 32;
    fout.seekp(0);
    fout.write(reinterpret_cast<const char *>(&wav_hdr), sizeof(wav_hdr_t));
    fout.close();

    return 0;
}
