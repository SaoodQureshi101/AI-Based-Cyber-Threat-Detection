import pandas as pd

# 1. Load both labeled datasets
train_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_training-set.csv"
test_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_testing-set.csv"

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

# 2. Combine datasets
combined = pd.concat([train, test], ignore_index=True)
print(f"Initial combined shape: {combined.shape}")

# 3. Basic cleaning
# Remove duplicates
combined.drop_duplicates(inplace=True)

# Handle missing labels (though your sample shows no missing ones)
combined.dropna(subset=['label', 'attack_cat'], inplace=True)

# 4. Verify label distribution
print("\nLabel Distribution:")
print(combined['label'].value_counts())  # Binary labels (0=normal, 1=attack)
print("\nAttack Category Distribution:")
print(combined['attack_cat'].value_counts())

# 5. Save cleaned data
output_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_combined_cleaned.csv"
combined.to_csv(output_path, index=False)
print(f"\nSaved cleaned data to: {output_path}")