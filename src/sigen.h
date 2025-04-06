#ifndef SIGEN_H
#define SIGEN_H

#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <cstdint> // added for uint8_t, uint32_t, etc.
#define _USE_MATH_DEFINES
#include <cmath>   // added for M_PI, sin()
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif


#define S_RATE 44100
#define BPM 100
// Amplitudes defined for constant RMS
#define SIN_AMP 2828
#define SQR_AMP 2000
#define TRI_AMP 3464
#define SAW_AMP 3464
// cut off frequency of LPF
#define LPF_FC 10000

enum class shape_t: uint8_t {none, sine, square, triangle, saw};
typedef std::unordered_map<std::string, float> f_lut_t;

class note_t {
private:
    // build frequency look-up table
    static f_lut_t construct_lut();

public:
    shape_t      shape;
    int          length;
    std::string  name;
    int          octave;
    float        freq;

    note_t(shape_t s, int l, std::string n, int o);
};

#ifdef DEBUG
std::ostream &operator<<(std::ostream &os, shape_t shape);
std::ostream &operator<<(std::ostream &os, note_t const &note);
std::ostream &operator<<(std::ostream &os, std::vector<note_t> const &stave);
std::ostream &operator<<(std::ostream &os, std::vector<std::vector<note_t>> const &score);
#endif

std::vector<int16_t> lowpass(std::vector<int16_t> &pcm_data);
float filter(int i, int s_len);
void play(std::vector<int16_t> &pcm_data, int &ptr, note_t note, bool first);
void play(std::vector<int16_t> &pcm_data, int &ptr, shape_t shape, int length,
          float freq, bool first);

#endif
