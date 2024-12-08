import pandas as pd

filepath = 'F://github/Triantafulloy-Thanasis-Project01-AM7115132300010/Crime_Data_from_2020_to_Present_20241025.csv'

# Read the CSV file
df = pd.read_csv(filepath)
print(df.head(10))

# Delete the "Part 1-2" column
df = df.drop(columns=['Part 1-2'])
# Delete rows where 'Status' is NaN
df = df.dropna(subset=['Status'])

# Delete rows where 'Vict Age' is greater than 100
df = df[df['Vict Age'] <= 100]
# Delete rows where 'Vict Age' equals '-'
df = df[df['Vict Sex'] != '-']
# Delete rows where 'Vict Age' equals '-'
df = df[df['Vict Descent'] != '-']

# Replace NaN values in 'Premis Cd' with 0 and cast to float
df['Premis Cd'] = df['Premis Cd'].fillna(0).astype(float)
# Replace NaN values in the 'Weapon Used Cd' column with 0
df['Weapon Used Cd'] = df['Weapon Used Cd'].fillna(0).astype(int)
# Replace NaN values in the 'Weapon_Used_Cd' column with 0
df['Weapon Used Cd'] = df['Weapon Used Cd'].fillna(0).astype(int)

# Correct Crime Code where 'Crm Cd' is different from 'Crm Cd 1' by setting 'Crm Cd 1' to 'Crm Cd'
df.loc[df['Crm Cd'] != df['Crm Cd 1'], 'Crm Cd'] = df['Crm Cd 1']

# Delete every entry that has NaN in 'Crm Cd' and 'Crm Cd 1'
df = df.dropna(subset=['Crm Cd'])

# Cast Crm Cd to int
df['Crm Cd'] = df['Crm Cd'].astype(int)


# Save the modified DataFrame to a new CSV
df.to_csv('F://github/Triantafulloy-Thanasis-Project01-AM7115132300010/Crime_Data_from_2020_to_Present_20241025_clean.csv', index=False)
