#include <iostream>
#include <fstream>

typedef struct WAV_HEADER {
    uint8_t  riff[4]       = {'R', 'I', 'F', 'F'};
    uint32_t file_size;                          // calculate and fill in later
    uint8_t  wave[4]       = {'W', 'A', 'V', 'E'};
    uint8_t  fmt[4]        = {'f', 'm', 't', ' '};
    uint32_t fmt_size      = 16;
    uint16_t wav_format    = 1;                  // PCM
    uint16_t channel_cnt   = 1;
    uint32_t sample_freq   = 44100;
    uint32_t data_rate     = 44100 * 2;          // 2 bytes per sample
    uint16_t block_align   = 2;                  // 16-bit mono
    uint16_t bits_per_samp = 16;
    uint8_t  data[4]       = {'d', 'a', 't', 'a'};
    uint32_t data_size;                          // calculate and fill in later
} wav_hdr_t;

int main(void) {
    static_assert(sizeof(wav_hdr_t) == 44, "wav_hdr_t size error");

    // construct pcm raw data
    wav_hdr_t wav_hdr;
    unsigned int sr = wav_hdr.sample_freq;

    unsigned int length = 2 * sr; // length in number of samples
    uint16_t pcm_data[length];

    // make a square wave
    bool sign = true;
    float half_period = sr/440/2;
    float count = half_period;

    for(int i = 0; i < length; ++i) {
        if (sign) {
            pcm_data[i] = 2000;
        } else {
            pcm_data[i] = -2000;
        }

        count -= 1.0;
        if (count < 0) {
            count += half_period;
            sign = !sign;
        }
    }

    // calculate header
    wav_hdr.data_size = length*2;  // 2 bytes per sample
    wav_hdr.file_size = length*2 + 36;

    // write file
    std::ofstream fout;
    fout.open("m.wav", std::ios::binary);
    fout.write(reinterpret_cast<const char *>(&wav_hdr), sizeof(wav_hdr));
    for (int i = 0; i < length; ++i) {
        fout.write(reinterpret_cast<char *>(&pcm_data[i]), sizeof(uint16_t));
    }

    fout.close();

    return 0;
}
