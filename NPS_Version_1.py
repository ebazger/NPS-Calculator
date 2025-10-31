##purpose of this code is to use the NPS column in your file and give you a quick summary

import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_nps(file_path, column_name):
    """
    Loads a file (CSV or Excel), calculates NPS and displays statistics.
    """
    # 1. Load the data
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith('.xlsx') or file_path.lower().endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please use .csv, .xlsx, or .xls.")
            return
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # 2. Validate the column name
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the file.")
        print(f"Available columns are: {list(df.columns)}")
        return

    # Extract the NPS column, handle potential non-numeric values
    ratings = pd.to_numeric(df[column_name], errors='coerce').dropna()
    
    if ratings.empty:
        print("Error: The selected column contains no valid numeric ratings.")
        return
        
    # Ensure ratings are within the 0-10 range
    ratings = ratings[(ratings >= 0) & (ratings <= 10)]

    if ratings.empty:
        print("Error: No ratings found within the 0-10 range in the selected column.")
        return

    # 3. Categorize ratings
    promoters = ratings[ratings >= 9]
    passives = ratings[(ratings >= 7) & (ratings <= 8)]
    detractors = ratings[ratings <= 6]

    # 4. Calculate percentages
    total_responses = len(ratings)
    percent_promoters = (len(promoters) / total_responses) * 100
    percent_detractors = (len(detractors) / total_responses) * 100
    percent_passives = (len(passives) / total_responses) * 100

    # 5. Calculate NPS score
    nps_score = percent_promoters - percent_detractors

    # 6. Display results
    print("-" * 40)
    print("NPS Calculation Results:")
    print("-" * 40)
    print(f"Total valid responses:   {total_responses}")
    print(f"Promoters (9-10):        {len(promoters)} ({percent_promoters:.1f}%)")
    print(f"Passives (7-8):          {len(passives)} ({percent_passives:.1f}%)")
    print(f"Detractors (0-6):        {len(detractors)} ({percent_detractors:.1f}%)")
    print("-" * 40)
    print(f"** Net Promoter Score (NPS): {nps_score:.2f} **")
    print("-" * 40)

    # 7. Display additional statistics
    print("\nAdditional Statistics:")
    print(f"Mean rating:             {ratings.mean():.2f}")
    print(f"Median rating:           {ratings.median():.2f}")
    print(f"Standard Deviation:      {ratings.std():.2f}")
    print(f"Min rating:              {ratings.min()}")
    print(f"Max rating:              {ratings.max()}")

    # 8. Optional: Visualize the distribution
    plt.figure(figsize=(8, 5))
    ratings.hist(bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
                 edgecolor='black', align='mid')
    plt.title(f'Distribution of NPS Ratings in "{column_name}"')
    plt.xlabel('Rating (0-10)')
    plt.ylabel('Frequency')
    plt.xticks(range(11))
    plt.grid(axis='y', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    # Ask the user for inputs
    print("--- NPS Calculator ---")
    
    while True:
        file_path = input("Enter the full path to your file (CSV or Excel): ").strip()
        if os.path.exists(file_path):
            break
        else:
            print("Invalid path or file does not exist. Please try again.")

    column_name = input("Enter the exact name of the column containing the NPS rating: ").strip()

    # Run the calculation function
    calculate_nps(file_path, column_name)
