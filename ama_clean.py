import pytest
import pandas as pd 
import re

df = pd.read_csv(r"C:\Users\calri\Documents\data_prep\Data_Cleaning\alumni_anonymized.csv",index_col='Id No')
df.rename(columns={"Custom.Year":"Exit Year","Places & Date of Birth & Death":"Birth Year","Id No":"Id"},inplace=True)


def drop_invalid_rows(df):
    # Drop empty year rows
    df.dropna(subset=["Exit Year","Birth Year"], inplace=True)

    # Drop Rows that do not contain Exit year
    rows = df[df["Exit Year"].str.contains(r'\d{2}') == False].index
    df.drop(rows,inplace=True)

    # Drop rows that do not contain year value
    rows = df[df["Birth Year"].str.contains(r'\d{2}') == False].index
    df.drop(rows,inplace=True)

    rows = df[(df["Birth Year"].str.contains('(?:DOB|Born)') == False) & (df["Birth Year"].str.contains('(?:Died|DOD)'))].index
    df.drop(rows,inplace=True)

    rows = df[df["Birth Year"].str.contains('(?:DOB|Born): UNK')].index
    df.drop(rows,inplace=True)
        
def extract_exit_year(df):
    for i, elm in df["Exit Year"].items():
        year = str(elm).strip()
        year = re.search(r'\d{2}\d*',year).group()
        other = re.search(r'\d{4}', str(df.at[i, "Other No"]))
        if len(year) == 2:
            if int(year) < 81:
                year = "19" + year
            elif int(year) > 85:
                year = "18" + year
            elif other:
                year = other.group()
        df.at[i, "Exit Year"] = int(year)

drop_invalid_rows(df)
extract_exit_year(df)

def extract_birth_year(df):
    for i, elm in df["Birth Year"].items():
        year = elm.strip()
        index = re.findall(r'\d{2}/\d{2}/\d{2}',elm)
        sea = re.search(r'\d{4}', year)
        other = df.at[i, "Other No"]
        death = re.search('(?:DOD|Died|DOC)',year)
        if index:
            if (('DOB' in elm) | ('Born' in elm)):
                if sea:
                    if death:
                        if death.start() > sea.start():
                            year = sea.group()
                        else:
                            year = index[0][-2:]
                            if int(sea.group()) > 1900:
                                year = "19" + year
                            else:
                                year = "18" + year
                    else:
                        year = sea.group()
                else:
                    year = index[0][-2:]
                    if df.at[i, "Exit Year"] > 1925:
                        year = "19" + year
                    elif df.at[i, "Exit Year"] > 1800:
                        year = "18" + year
                    else:
                        year = 0  
        elif sea:
            if death:
                    if death.start() > sea.start():
                        year = sea.group()
                    else:
                        year = 0
            else:
                year = sea.group()
        elif float(other) > 0:
            year = str(other)[:2] + re.search(r'\d{2}',year).group()
        else:
            year = 0
        if (int(df.at[i, "Exit Year"]) - int(year)) > 25:
            year = 0
        df.at[i, "Birth Year"] = int(year)

def remove_indistuinguishable(df):
    rows = df[((df["Exit Year"] > 79) & 
              (df["Exit Year"] < 85) &
              (df["Birth Year"] < 1000)) |
              (df["Birth Year"] == 0)].index
    df.drop(rows,inplace=True)
    df.at[2881, "Birth Year"] = 1930

def exit_year_2(df):
    for i, elm in df["Exit Year"].items():
        year = str(elm)
        birth = df.at[i, "Birth Year"]
        if (len(year) == 2) & (birth > 1000):
            year = str(birth)[:2] + year
        df.at[i, "Exit Year"] = int(year)

extract_birth_year(df)
exit_year_2(df)
remove_indistuinguishable(df)
df.to_csv(r'C:\Users\calri\Documents\data_prep\Data_Cleaning\ama_clean.csv',index=True)