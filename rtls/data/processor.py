"""Data processing module for RTLS system."""

from typing import Tuple, List
import pandas as pd
import numpy as np
from ..config.settings import (
    TRANSMITTER_COORDS,
    MAX_TRANSMITTER_DISTANCE,
    RSSI_COLUMNS,
    INSTANCE_COLUMNS,
    COORDINATE_COLUMNS,
)

class DataProcessor:
    """Process raw RTLS data and prepare it for localization."""
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.transmitter_coords = TRANSMITTER_COORDS
        self.max_distance = MAX_TRANSMITTER_DISTANCE
    
    def process_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process raw data from Elasticsearch.
        
        Args:
            df: Raw DataFrame from Elasticsearch
            
        Returns:
            Processed DataFrame with extracted RSSI and instance values
        """
        # Extract instance IDs and RSSI values
        processed_df = pd.DataFrame()
        processed_df['timestamp'] = df['timestamp']
        
        # Extract instance IDs
        for i, col in enumerate(INSTANCE_COLUMNS, 1):
            processed_df[col] = df['nearest'].str.slice(16 + (i-1)*37, 24 + (i-1)*37, 1)
        
        # Extract RSSI values
        for i, col in enumerate(RSSI_COLUMNS, 1):
            processed_df[col] = df['nearest'].str.slice(33 + (i-1)*37, 36 + (i-1)*37, 1)
        
        processed_df['Puck'] = df['instanceId']
        
        # Clean and convert data
        processed_df = self._clean_data(processed_df)
        processed_df = self._convert_coordinates(processed_df)
        
        return processed_df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the processed data.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        # Remove empty values and convert RSSI to numeric
        df = df[df != ''].dropna()
        df = df.reset_index(drop=True)
        
        # Convert RSSI values to numeric and restore negative sign
        for col in RSSI_COLUMNS:
            df[col] = pd.DataFrame(df[col])[col].str.extract(r'(\d+)', expand=False)
            df[col] = df[col].astype(int) * -1
        
        return df
    
    def _convert_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert transmitter IDs to coordinates.
        
        Args:
            df: DataFrame with transmitter IDs
            
        Returns:
            DataFrame with converted coordinates
        """
        # Create coordinate columns
        for i, col in enumerate(COORDINATE_COLUMNS):
            if col.startswith('X'):
                df[col] = df[INSTANCE_COLUMNS[i//2]].map(lambda x: self.transmitter_coords[x][0])
            else:
                df[col] = df[INSTANCE_COLUMNS[i//2]].map(lambda x: self.transmitter_coords[x][1])
        
        return df
    
    def classify_records(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Classify records as logical or semi-logical.
        
        Args:
            df: DataFrame with transmitter coordinates
            
        Returns:
            Tuple of (logical_records, semi_logical_records)
        """
        # Calculate distances between transmitters
        distances = self._calculate_distances(df)
        
        # Classify records
        logical_mask = (distances['dis_12'] < self.max_distance) & \
                      (distances['dis_13'] < self.max_distance) & \
                      (distances['dis_23'] < self.max_distance)
        
        logical_records = df[logical_mask].copy()
        semi_logical_records = df[~logical_mask & (distances['dis_12'] < self.max_distance)].copy()
        
        return logical_records, semi_logical_records
    
    def _calculate_distances(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate distances between transmitters.
        
        Args:
            df: DataFrame with transmitter coordinates
            
        Returns:
            DataFrame with calculated distances
        """
        distances = pd.DataFrame()
        distances['dis_12'] = np.sqrt(((df['X1']-df['X2'])**2) + ((df['Y1']-df['Y2'])**2))
        distances['dis_13'] = np.sqrt(((df['X1']-df['X3'])**2) + ((df['Y1']-df['Y3'])**2))
        distances['dis_23'] = np.sqrt(((df['X2']-df['X3'])**2) + ((df['Y2']-df['Y3'])**2))
        return distances 