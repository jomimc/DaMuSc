
import numpy as np
import pandas as pd

### Default value for octave cutoff
OCT_CUT = 50


#############################################################################
### Functions to be used in reformatting the data

def get_cents_from_ratio(ratio):
    return 1200.*np.log2(ratio)


def str_to_ints(st, delim=';'):
    return [int(s) for s in st.split(delim) if len(s)]


def ints_to_str(i):
    return ';'.join([str(x) for x in i])



#############################################################################
### Functions for extracting and reformatting the raw data


def get_all_variants(scale):
    step_ints = np.diff(scale).astype(int)
    for i in range(len(step_ints)):
        yield np.cumsum(np.append([0], np.roll(step_ints, -i)))


def process_scale(scale):
    step_ints = np.diff(scale).astype(int)
    N = len(step_ints)
    tonic_ints = scale[1:] - scale[0]
    all_ints = np.array([i for j in range(len(step_ints)) for i in np.cumsum(np.roll(step_ints, j))])
    return N, step_ints, tonic_ints, all_ints


def extract_scale_using_tonic(ints, tonic, oct_cut):
    # If in str or list format, there are explicit instructions
    # for each interval
    # Otherwise, there is simply a starting note, and it should
    # not go beyond a single octave
    try:
        tonic = eval(tonic)
    except Exception as e:
        pass

    if isinstance(tonic, str):
        tonic = np.array(str_to_ints(tonic))
        tmin, tmax = min(tonic), max(tonic)

    elif isinstance(tonic, (list, np.ndarray)):
        tmin, tmax = min(tonic), max(tonic)

    elif isinstance(tonic, (int, float)):
        i_tonic = int(tonic) - 1
        tonic = np.zeros(len(ints)+1)
        tonic[i_tonic] = 1
        tonic[-1] = 2
        tmin, tmax = 1, 2

    scale = []
    for i, t1, t2 in zip(ints, tonic[:-1], tonic[1:]):
        if t1 == tmin:
            if len(scale):
                yield np.array(scale)
            scale = [0, i]

        elif len(scale):
            scale.append(i + scale[-1])

    if scale[-1] > (1200 - oct_cut):
        yield np.array(scale)


def extract_specific_variants(ints, tonic, variants, oct_cut=OCT_CUT):
    if isinstance(tonic, str):
        tonic = np.array(str_to_ints(tonic), int)
    for v in variants.split(','):
        v = str_to_ints(v)
        extra = 0
        scale = []
        for i, t in zip(ints, tonic[:-1]):
            if t == v[0]:
                if len(scale):
                    if scale[-1] > (1200 - oct_cut):
                        yield np.array(scale)
                scale = [0, i]
            elif len(scale) and t in v:
                scale.append(scale[-1] + i)
            elif len(scale):
                scale[-1] = scale[-1] + i
                
    if scale[-1] > (1200 - OCT_CUT):
        yield np.array(scale)


def eval_tonic(tonic):
    if isinstance(tonic, str):
        return tonic != 'N/A'
    elif isinstance(tonic, (int, float)):
        return not np.isnan(tonic)


def extract_scale_from_measurement(row, oct_cut=OCT_CUT, use_specified_variants=True, use_all_variants=False):
    ints = np.array(row.Intervals)

    # This column exists only for this instruction;
    # If 'Y', then add the final interval needed for the scale
    # to add up to an octave;
    # This exists because some the final interval is sometimes not
    # reported in papers simply because it is redundant if your analysis assumes the octave.
    # The column should only equal 'Y' if the source indicates that
    # the octave is actually used in the relevant source.
    if row.Octave_modified == 'Y':
        final_int = 1200 - sum(ints)
        yield np.array([0.] + list(np.cumsum(list(ints) + [final_int])))
        # There can only be one possible scale in this case
        return


    # STILL CONFUSION OVER THE TERM MODE!!!
    # Some sources provide an instrument tuning, and specify in which
    # ways subsets of the notes are used as scales ('variants').
    # In this case, the information is available under the column 'Variants',
    # and multiple scales can be extracted from a single tuning.
    if use_specified_variants:
        # If row.Variants is not null, this should produce some scales
        try:
            for scale in extract_specific_variants(ints, row.Tonic, row.Variants):
                yield scale
            # If not extracting all possible variants, then we can exit now
            if not use_all_variants:
                return
        except AttributeError:
            pass

    # If the entry includes information on tonality, and if
    # not using all possible variants, follow the instructions given.
    # This avoids double-counting in case use_all_variant == True
    if not use_all_variants:
        if eval_tonic(row.Tonic):
            for scale in extract_scale_using_tonic(ints, row.Tonic, oct_cut):
                if abs(1200 - scale[-1]) <= oct_cut:
                    yield scale
            return


    if sum(ints) >= (1200 - oct_cut):
        start_from = 0
        for i in range(len(ints)):
            if i < start_from:
                continue
            sum_ints = np.cumsum(ints[i:], dtype=int)
            # If the total sum of ints is less than the cutoff, ignore this entry
            if sum_ints[-1] < (1200 - oct_cut):
                break
            # Find the scale degree by finding the note closest to 1200
            idx_oct = np.argmin(np.abs(sum_ints-1200))
            oct_val = sum_ints[idx_oct]
            # If the total sum of ints is greater than the cutoff, move
            # on to the next potential scale
            if abs(oct_val - 1200) > OCT_CUT:
                continue
            
            # If all variants are not being used (i.e., if each interval is only
            # allowed to be counted in a scale once) then start looking
            # for new scales from this index 
            if not use_all_variants:
                start_from = idx_oct + i + 1

            yield np.array([0.] + list(sum_ints[:idx_oct+1]))




