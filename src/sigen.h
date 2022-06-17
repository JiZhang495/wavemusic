#ifndef SIGEN_H
#define SIGEN_H

#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

#define S_RATE 44100
#define BPM 100
// Amplitudes defined for constant RMS
#define SIN_AMP 2828
#define SQR_AMP 2000
#define TRI_AMP 3464
#define SAW_AMP 3464

enum shape_t: uint8_t {none, sine, square, triangle, saw};
typedef std::unordered_map<std::string, float> f_lut_t;

class note_t {
private:
    // build frequency look-up table
    static f_lut_t construct_lut();

public:
    shape_t      shape;
    unsigned int length;
    std::string  name;
    int          octave;
    float        freq;

    note_t(shape_t s, unsigned int l, std::string n, int o);
};

#ifdef DEBUG
std::ostream &operator<<(std::ostream &os, shape_t shape);
std::ostream &operator<<(std::ostream &os, note_t const &note);
std::ostream &operator<<(std::ostream &os, std::vector<note_t> const &stave);
std::ostream &operator<<(std::ostream &os, std::vector<std::vector<note_t>> const &score);
#endif

float filter(unsigned int i, unsigned int s_len);
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, note_t note, bool first);
void play(std::vector<uint16_t> &pcm_data, unsigned int &ptr, shape_t shape,
          unsigned int length, float freq, bool first);

#endif
