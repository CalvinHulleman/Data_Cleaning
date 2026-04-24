#RUN AS: python -m pytest test_df.py   
import pytest
import pandas as pd
#put your file name here (the cleaned up version)
df = pd.read_csv(r'C:\Users\calri\Documents\data_prep\Data_Cleaning\ama_clean.csv', index_col='Id No')

#The tests that you crowd-sourced are below.
def test_eliminations():
    assert 9308 not in df.index
    assert 9229 not in df.index
    assert 9211 not in df.index
    assert 2669 not in df.index
    assert 10538 not in df.index

def test_birthday_cleaning():
    assert df.loc[586, "Birth Year"] == 1912
    assert df.loc[2881, "Birth Year"] == 1930
    assert df.loc[6140, "Birth Year"]== 1902
    assert df.loc[1182, "Birth Year"]== 1910
    assert df.loc[5769, "Birth Year"]== 1873

#my file didn't pass this one - I would save this for last
def test_hard_cases():
    assert df.loc[8524, "Birth Year"] == 1947

def test_exit_cleaning():
    assert df.loc[11283, "Exit Year"] == 1961
    assert df.loc[5037, "Exit Year"] == 1978
    assert df.loc[630, "Exit Year"] == 1964
    assert df.loc[10073, "Exit Year"] == 1898
    assert df.loc[28, "Exit Year"] == 1929
    # assert df.loc[4316, "Exit Year"] == 1957

def test_filtering_exits():
    for elm in df["Exit Year"]:
        assert elm >= 1879
        assert elm <= 1984

def test_filtering_bday():
    for elm in df["Birth Year"]:
        assert elm >= 1845
        assert elm <= 1985




