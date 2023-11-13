from pathlib import Path

import pandas as pd

# Construct the absolute path to the files
files = [
    "WB - пылесос для мебели - 01082023 - 31082023.xlsx",
    "WB - пылесос для мебели - 01092023 - 30092023.xlsx",
    "WB - пылесос для мебели - 01102023 - 30102023.xlsx",
]


def load_files(files, df: pd.DataFrame = None) -> pd.DataFrame:
    # Get the absolute path of the directory containing the script
    script_directory = Path().cwd().resolve() / "data"
    for file in files:
        # Construct the absolute path to the files
        file_path = script_directory / file
        # Read the XLSX file using pandas
        temp = pd.read_excel(file_path)
        # Melt df's date and metric
        temp = temp.melt(id_vars=temp.columns[:52], var_name="date", value_name="value")
        # Split out column into date and metric
        temp[["Дата", "metric"]] = temp["date"].str.split().apply(pd.Series)
        # Set correct metric
        temp["Дата"] = pd.to_datetime(temp["Дата"], dayfirst=True)
        # Drop unneeded
        temp.dropna(axis="columns", how="all", inplace=True)
        temp.drop(columns="date", inplace=True)
        # Concatenate it all together
        if df is not None:
            df = pd.concat([df, temp])
        else:
            df = temp
    # df.rename(
    #     columns={"Коммент.": "Коммент", "Медиан. цена": "Медиан цена"}, inplace=True
    # )
    df["metric"] = df["metric"] + "/день"
    # Pivot the metric
    df = df.pivot(
        index=list(df.columns[:51]) + [df.columns[52]], columns="metric", values="value"
    ).reset_index()
    df.columns.name = None
    df.sort_values(by=["Дата", "Позиция в поиске"], inplace=True)
    df.reset_index(inplace=True, drop=True)
    # df.to_csv(script_directory / "joined.csv", index=False)
    return df


data = load_files(files)
