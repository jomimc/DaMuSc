

def fix_text(a):
    key = {'+AF8-':'_',
           '+ADs-':';',
           '+ACY-':'and',
           '+AC0-':'-',
           '+IBg-':"'",
           '+IBk-':"'",
           '+ACI-':'"',
           '+IBM-':'-',
           '+//0A4v/9AID//QCZ-':"'",
           '+//0A4v/9AID//QCY-':"'",
           '+//0A4v/9AID//QCc-':"'",
           '+//0A4v/9AID//QCd-':"'",
           '+//0AxP/9AIE-':"a",
           '+//0AxP/9AI0-':"c",
           '+//0Aw//9AKL//QDE//0Agv/9AMX//QCe-':"-",
           '+//0Aw//9AKg-':"e",
           '+//0A4v/9AID//QCT-':"-"}
    for k, v in key.items():
        a = v.join(a.split(k))
    return a


def fix_cols(df):
    cols = [fix_text(c) for c in df.columns]
    return df.rename(columns={c1:c2 for c1, c2 in zip(df.columns, cols)})


def fix_rows(df, cols):
    for c in cols:
        df.loc[df[c].notnull(), c] = df.loc[df[c].notnull(), c].apply(fix_text)
    return df


def updating_societies(df):
    soc = pd.read_csv('soceitiesw_metadata.csv')
    cult_key = {k:v for k, v in zip(soc['Name.Scale'], soc.ID)}
    cult_key.update({'Bapere':'Bap25',
                     'Hindustani':'Nor8',
                     'Burma':'Mya29',
                     'Japan':'Jap5',
                     'Turkey':'Tur13',
                     'Sena':'Ase49',
                     'Benin':'Ben83',
                     'BaGanda':'Bag70'})
    df['SocID'] = df.Culture.apply(lambda x: cult_key.get(x, ''))
    return df



