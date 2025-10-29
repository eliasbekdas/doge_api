import pandas as pd

# creating a series
fruits = pd.Series(["Apple", "Banana", "Cherry", "Date"] , index=["a", "b", "c", "d"])
print(fruits)

# creating a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]}
df = pd.DataFrame(data)
print(df)

# import data from a CSV file
df_csv = pd.read_csv("/Users/eliasbekdas/Desktop/HR_comma_sep.csv")
print(df_csv.head(7))

df_csv.info()

df_csv.describe()

low_satisfaction = df_csv[df_csv["satisfaction_level"] < 0.4]
print(low_satisfaction.head(10))
print("the max is: " , max(low_satisfaction["satisfaction_level"]))

temp0 = df_csv

temp0['satisfaction']= (temp0['satisfaction_level'] * 100).astype(int)
print(temp0.head(5))