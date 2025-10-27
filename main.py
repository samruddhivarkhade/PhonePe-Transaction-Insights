import os
import json
import pandas as pd

base_path = "data/aggregated/transaction/country/india/state"

all_data = []

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in os.listdir(year_path):
            if quarter_file.endswith('.json'):
                quarter_path = os.path.join(year_path, quarter_file)
                try:
                    with open(quarter_path, 'r') as f:
                        data = json.load(f)

                        if data.get("data") and data["data"].get("transactionData"):
                            for txn in data["data"]["transactionData"]:
                                all_data.append({
                                    "State": state,
                                    "Year": int(year),
                                    "Quarter": int(quarter_file.strip(".json")),
                                    "Transaction_Type": txn["name"],
                                    "Transaction_Count": txn["paymentInstruments"][0]["count"],
                                    "Transaction_Amount": txn["paymentInstruments"][0]["amount"]
                                })
                except Exception as e:
                    print(f"Error reading {quarter_path}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_data)
print("✅ Combined data shape:", df.shape)
print(df.head(10))  # show first 10 rows for verification

# Check if 'State' exists
print("\nColumns:", df.columns.tolist())

# Save to CSV
df.to_csv("aggregated_transaction.csv", index=False)
print("✅ CSV file created successfully.")
