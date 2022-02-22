import numpy as np

import utils


#############################################################################
### Tuning systems

### PYT = Pythagorean tuning
### EQ{N} = N-Tone Equal Temperament
### JI  = Just intonation
### CHINA = Shi-er-lu
### The rest are sourced from Rechberger, Herman

PYT_INTS = np.array([0., 90.2, 203.9, 294.1, 407.8, 498.1, 611.7, 702., 792.2, 905., 996.1, 1109.8, 1200.])
EQ5_INTS = np.linspace(0, 1200, num=6, endpoint=True, dtype=float)
JI_INTS = np.array([0., 111.7, 203.9, 315.6, 386.3, 498.1, 590.2, 702., 813.7, 884.4, 1017.6, 1088.3, 1200.])
DASTGAH = np.array([0., 90., 133.23, 204., 294.14, 337.14, 407.82, 498., 568.72, 631.28, 702., 792.18, 835.2, 906., 996., 1039.1, 1109.77, 1200.])
TURKISH = {'T':203.8, 'K':181.1, 'S':113.2, 'B':90.6, 'F':22.6, 'A':271, 'E':67.9}
VIET    = np.array([0., 175., 200., 300., 338., 375., 500., 520., 700., 869., 900., 1000., 1020., 1200.])
CHINA   = np.array([0., 113.67291609,  203.91000173,  317.73848174,  407.83554758, 520.68758457,  611.71791523,  701.95500087,  815.62791696, 905.8650026 , 1019.47514332, 1109.76982292, 1201.27828039])


#############################################################################
### Functions for matching theory scales to tuning systems

def map_to_tuning_system(intervals, tonic, tuning_system):
    N = tuning_system.size
    # Convert interval string to list of type int
    intervals = utils.str_to_ints(intervals)

    # Convert interval array to scale indices
    scale_idx = np.cumsum([0] + intervals)

    # Shift according to which note is the tonic,
    # and make sure that all indices fit within the tuning system
    scale_idx = (scale_idx - (tonic - 1))
    scale_idx = np.array([i if 0 <= i <= N else i % N for i in scale_idx])
    scale = tuning_system[scale_idx]
    return scale


def map_to_turkish_system(intervals, tonic, tuning_system):
    scale = np.cumsum([0] + [tuning_system[i] for i in intervals.split(';')])
    scale = scale - scale[tonic -1]
    return scale


def get_equal_temperament_tuning_system(tuning):
    N = int(tuning.split('-')[0])
    return np.linspace(0, 1200, N+1)


def get_precomputed_tuning_system(tuning):
    tuning_systems = {'Pythagorean':PYT_INTS,
                      'Just':JI_INTS,
                      'Dastgah-ha':DASTGAH,
                      'Vietnamese':VIET,
                      'Chinese':CHINA,
                      'Turkish':TURKISH}
    return tuning_systems[tuning]


def get_tuning_system(tuning):
    if '-tet' in tuning.lower():
        return get_equal_temperament_tuning_system(tuning)
    else:
        return get_precomputed_tuning_system(tuning)


def get_theory_scale_in_cents(intervals, tonic, tuning):
    for tun in tuning.split(';'):
        try:
            if tun == 'Cents':
                yield np.cumsum([0] + utils.str_to_ints(intervals))
            else:
                tuning_system = get_tuning_system(tun)
                if tuning == 'Turkish':
                    yield np.round(map_to_turkish_system(intervals, tonic, tuning_system), 0).astype(int)
                else:
                    yield np.round(map_to_tuning_system(intervals, tonic, tuning_system), 0).astype(int)
        except Exception as e:
            print(f"Error for intervals: {intervals}\n{e}")



