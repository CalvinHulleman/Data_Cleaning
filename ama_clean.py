import pytest
import pandas as pd 
import re

df = pd.read_csv(r"C:\Users\calri\Documents\data_prep\Data_Cleaning\alumni_anonymized.csv",index_col='Id No')
df.rename(columns={"Custom.Year":"Exit Year","Places & Date of Birth & Death":"Birth Year"},inplace=True)


def drop_invalid_rows(df):
    # Drop empty year rows
    df.dropna(subset=["Exit Year","Birth Year"], inplace=True)

    # Drop Rows that do not contain Exit year
    rows = df[df["Exit Year"].str.contains(r'\d{2}') == False].index
    df.drop(rows,inplace=True)

    # Drop rows that do not contain year value
    rows = df[df["Birth Year"].str.contains(r'\d{2}') == False].index
    df.drop(rows,inplace=True)

def extract_exit_year(df):
    for i, elm in df["Exit Year"].items():
        year = str(elm).strip()
        year = re.search(r'\d{2}\d*',year).group()
        if len(year) == 2:
            if int(year) < 80:
                year = "19" + year
            else:
                year = "18" + year
        df.at[i, "Exit Year"] = int(year)

drop_invalid_rows(df)
extract_exit_year(df)
print(df)

