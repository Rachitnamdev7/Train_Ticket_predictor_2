import pandas as pd

# Load CSV
df = pd.read_csv("train_data.csv")

# Replace 'GN' with 'SL' in 'Category' column
df['class'] = df['class'].replace('GN', 'SL')

# Save cleaned data (overwrite or use a new file)
df.to_csv("train_data.csv", index=False)

print("Data cleaned and saved to train_data.csv")
