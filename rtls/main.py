"""Main script for RTLS system."""

import pandas as pd
import matplotlib.pyplot as plt
from .data.processor import DataProcessor
from .models.localizer import Localizer

def main():
    """Main function to run the RTLS system."""
    # Initialize components
    processor = DataProcessor()
    localizer = Localizer()
    
    # Load raw data
    try:
        df = pd.read_excel('data/raw_data.xlsx')
        df = df.sort_values(by=['timestamp'])
    except FileNotFoundError:
        print("Error: Raw data file not found. Please ensure data/raw_data.xlsx exists.")
        return
    
    # Process data
    processed_df = processor.process_raw_data(df)
    
    # Classify records
    logical_records, semi_logical_records = processor.classify_records(processed_df)
    
    # Estimate positions
    positions = localizer.estimate_position(logical_records)
    
    # Plot results
    plot_results(positions, logical_records)
    
    # Save results
    save_results(positions, logical_records)

def plot_results(positions: pd.DataFrame, records: pd.DataFrame):
    """Plot the localization results.
    
    Args:
        positions: DataFrame with estimated positions
        records: DataFrame with original records
    """
    plt.figure(figsize=(10, 10))
    
    # Plot transmitter positions
    for tx_id, (x, y) in processor.transmitter_coords.items():
        plt.plot(x, y, 'ro', label=f'Transmitter {tx_id}')
    
    # Plot estimated positions
    plt.plot(positions['x'], positions['y'], 'b.', label='Estimated Positions')
    
    plt.grid(True)
    plt.legend()
    plt.title('RTLS Localization Results')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    
    plt.savefig('results/localization_plot.png')
    plt.close()

def save_results(positions: pd.DataFrame, records: pd.DataFrame):
    """Save the localization results.
    
    Args:
        positions: DataFrame with estimated positions
        records: DataFrame with original records
    """
    # Combine positions with original records
    results = pd.concat([records, positions], axis=1)
    
    # Save to CSV
    results.to_csv('results/localization_results.csv', index=False)

if __name__ == '__main__':
    main() 