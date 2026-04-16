import pytest
from ama_clean import *

df = pd.read_csv(r"C:\Users\calri\Documents\data_prep\Data_Cleaning\alumni_anonymized.csv",index_col='Id No')
df.rename(columns={"Custom.Year":"Exit Year","Places & Date of Birth & Death":"Birth Year"},inplace=True)

def test_extract_exit_year():
    drop_invalid_rows(df)
    extract_exit_year(df)
    assert df[df["Exit Year"].between(1874, 1984) == False].empty
    assert 2669 not in df.index
    assert 10538 not in df.index
    assert df.loc[4316, "Exit Year"] == 1957
    assert df.loc[5037, "Exit Year"] == 1978
    assert df.loc[630, "Exit Year"] == 1964
    assert df.loc[10073, "Exit Year"] == 1898
    assert df.loc[28, "Exit Year"] == 1929


