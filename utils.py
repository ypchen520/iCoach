import pandas as pd
import model
import toml

constants = toml.load("constants.toml")

def upload_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    # print(df.head(5))
    for index, row in df.iterrows():
        date = pd.to_datetime(row["Date"])
        category = row["Category"]
        subcategory = row["Subcategory"]
        task = row["Task"]
        print(task)
        print(date)
        total = int(row["Total"]) if task != "Basketball" else row["Total"]
        model.Task(name=task, total=total, date=date)
        if index < 5:
            print(index)
            print(date)
            print(category)
            print(subcategory)
            print(task)
            print(total)
        # print(type(row[["Date"]]))
        # print(row["Task"])

