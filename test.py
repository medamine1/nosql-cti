import pandas as pd
import random
import os
import uuid
from datetime import datetime

TRAIN_PATH = "train_dataset.csv"
TEST_PATH = "test_dataset.csv"
OUTPUT_DIR = "/Users/Medamine/Desktop/noo/random_samples"

def get_columns(csv_path):
    df = pd.read_csv(csv_path, nrows=0)
    return list(df.columns)

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_cols = get_columns(TRAIN_PATH)
    test_cols = get_columns(TEST_PATH)
    print("Columns in train_dataset.csv:")
    print(train_cols)
    print("\nColumns in test_dataset.csv:")
    print(test_cols)
    print("\nColumns only in train:")
    print(sorted(set(train_cols) - set(test_cols)))
    print("\nColumns only in test:")
    print(sorted(set(test_cols) - set(train_cols)))

    df = pd.read_csv(TEST_PATH)
    for i in range(1, 11):
        n_lines = random.randint(2, 10)
        sample = df.sample(n=n_lines, random_state=random.randint(0, 10000))
        # Add timestamp and uuid to ensure unique filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:6]
        out_path = os.path.join(OUTPUT_DIR, f"random_sample_{i}_{timestamp}_{unique_id}.csv")
        sample.to_csv(out_path, index=False)
        print(f"Random sample {i} with {n_lines} lines saved to {out_path}")
    print("\nAll 10 random sample files generated successfully.")

if __name__ == "__main__":
    main()