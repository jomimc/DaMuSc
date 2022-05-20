import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import tuning_system
import utils

PATH_BASE = [p for p in [Path.cwd()] + list(Path.cwd().parents) if p.name == 'ScalesDatabase'][0]
PATH_DATA = PATH_BASE.joinpath("Data")


### Parse user arguments when extracting octave scales
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_min", action="store", default=4,
                        help="Specify the minimum number of scale degrees")
    parser.add_argument("--n_max", action="store", default=9,
                        help="Specify the maximum number of scale degrees")
    parser.add_argument("--octave_cutoff", action="store", default=50,
                        help="Specify the tolerance allowed for octave errors")
    parser.add_argument("--use_all_variants", action="store", default=False,
                        help="Include all possible variants? Must be followed by True or False")
    parser.add_argument("--use_specific_variants", action="store", default=True,
                        help="Include variants specified in sources? Must be followed by True or False")
    parser.add_argument("--use_compound", action="store", default=False,
                        help="Include compound scales? Must be followed by True or False")
    return parser.parse_args()
    

### Create new DataFrame with intervals in cents for theory scales
def process_theory_scales(use_all_variants=False, use_compound=False):
    df = pd.read_csv(PATH_DATA.joinpath('theory_scales.csv'))
    cols_to_keep = ['TheoryID', 'Name', 'Culture', 'Region', 'Country', 'SocID', 'Tuning']
    new_cols = ['ScaleID'] + ['n_notes', 'scale', 'step_intervals', 'tonic_intervals', 'all_intervals'] + cols_to_keep
    df_new = pd.DataFrame(columns=new_cols)
    for i, row in df.iterrows():
        # Some 'compound scales' have been identified.
        # It is not clear yet how these should be approached.
        # WORK IN PROGRESS!!!
        if row['Reduced_scale']=='N' and not use_compound:
            continue
        for ints in [row['Ascending Intervals'], row['Descending Intervals']]:
            vals = list(df.loc[i, cols_to_keep].values)
            if isinstance(ints, str):
                for scale in tuning_system.get_theory_scale_in_cents(ints, row.Tonic, row.Tuning):
                    if use_all_variants:
                        for variant in utils.get_all_variants(scale):
                            N, step_ints, tonic_ints, all_ints = utils.process_scale(variant)
                            idx = len(df_new)
                            df_new.loc[idx] = [f"OT{idx:04d}", N, variant, step_ints, tonic_ints, all_ints] + vals
                    else:
                        N, step_ints, tonic_ints, all_ints = utils.process_scale(scale)
                        idx = len(df_new)
                        df_new.loc[idx] = [f"OT{idx:04d}", N, scale, step_ints, tonic_ints, all_ints] + vals
    df_new['Theory'] = 'Y'
    return df_new


### Create new DataFrame with intervals in cents for measured scales
def process_measured_scales(oct_cut=50, use_specific_variants=True, use_all_variants=False):
    df = pd.read_csv(PATH_DATA.joinpath('measured_scales.csv'))
    df.Intervals = df.Intervals.apply(utils.str_to_ints)
    cols_to_keep = ['MeasuredID', 'Name', 'Culture', 'Region', 'Country', 'SocID', 'Measured_type']
    new_cols = ['ScaleID'] + ['n_notes', 'scale', 'step_intervals', 'tonic_intervals', 'all_intervals'] + cols_to_keep
    df_new = pd.DataFrame(columns=new_cols)
    for row in df.itertuples():
        vals = list(df.loc[row[0], cols_to_keep].values)
        for scale in utils.extract_scale_from_measurement(row, oct_cut, use_specific_variants, use_all_variants):
            N, step_ints, tonic_ints, all_ints = utils.process_scale(scale)
            idx = len(df_new)
            df_new.loc[idx] = [f"OM{idx:04d}", N, scale, step_ints, tonic_ints, all_ints] + vals
    df_new['Theory'] = 'N'
    return df_new


def same_ints(i1, i2):
    if len(i1) != len(i2):
        return False
    return np.all(i1 == i2)
    

### Remove any duplicates within the same Culture
#       some may have been added due to reports in secondary sources
#       OR some scales are labelled differently in reports due
#       to starting on different funadmental frequencies
#       OR some scales may simply be duplicates due to chance
def remove_duplicates(df):
    to_bin = set()
    for row in df.itertuples():
        if row[0] in to_bin:
            continue
        idx = (df.SocID==row.SocID) & (df.step_intervals.apply(lambda x: same_ints(x, row.step_intervals)))
        if sum(idx)>1:
            for i in np.where(idx)[0][1:]:
                to_bin.add(i)
    return df.drop(index=to_bin).reset_index(drop=True)


### Create database of octave scales
def process_data(oct_cut=50, n_min=4, n_max=9,
                 use_specific_variants=True, use_all_variants=False, use_compound=False):

    df = pd.concat([remove_duplicates(process_theory_scales(use_all_variants, use_compound)),
                    remove_duplicates(process_measured_scales(oct_cut, use_specific_variants, use_all_variants))],
                   ignore_index=True)

    ### Only include scales with 4 <= N <= 9
    df = df.loc[(df.n_notes>=n_min)&(df.n_notes<=n_max)].reset_index(drop=True)

    ### Some basic metrics for scales
    df['min_int'] = df.step_intervals.apply(min)
    df['max_int'] = df.step_intervals.apply(max)
    df['octave'] = df.scale.apply(max)
    df['octave_dev'] = np.abs(df['octave'] - 1200)
    df['irange'] = df['max_int'] - df['min_int']

    return df


def reformat_df_and_save(df):
    cols = ['scale', 'step_intervals', 'tonic_intervals', 'all_intervals']
    for c in cols:
        df[c] = df[c].apply(utils.ints_to_str)
    df.to_csv(PATH_DATA.joinpath('octave_scales.csv'), index=False)
    

if __name__ == '__main__':

    args = parse_args()
    df = process_data(oct_cut=args.octave_cutoff, n_min=args.n_min, n_max=args.n_max,
                      use_specific_variants=args.use_specific_variants, use_all_variants=args.use_all_variants,
                      use_compound=args.use_compound)

    reformat_df_and_save(df)
    

    


