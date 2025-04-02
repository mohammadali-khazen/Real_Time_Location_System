"""Localization module for RTLS system."""

from typing import Tuple, List, Dict
import numpy as np
import pandas as pd
from pykalman import KalmanFilter
from ..config.settings import KALMAN_FILTER_PARAMS

class Localizer:
    """Handle position estimation using RSSI and transmitter coordinates."""
    
    def __init__(self):
        """Initialize the Localizer with Kalman filter."""
        self.kf = KalmanFilter(**KALMAN_FILTER_PARAMS)
    
    def estimate_position(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estimate position using RSSI and transmitter coordinates.
        
        Args:
            df: DataFrame with RSSI and transmitter coordinates
            
        Returns:
            DataFrame with estimated positions
        """
        # Calculate distances from RSSI
        distances = self._rssi_to_distance(df)
        
        # Estimate position using triangulation
        positions = self._triangulate(df, distances)
        
        # Apply Kalman filter for smoothing
        smoothed_positions = self._apply_kalman_filter(positions)
        
        return smoothed_positions
    
    def _rssi_to_distance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert RSSI values to distances using path loss model.
        
        Args:
            df: DataFrame with RSSI values
            
        Returns:
            DataFrame with estimated distances
        """
        # Path loss model parameters (these should be calibrated)
        A = -60  # Reference RSSI at 1m
        n = 2.0  # Path loss exponent
        
        distances = pd.DataFrame()
        for i, rssi_col in enumerate(['rssi_1', 'rssi_2', 'rssi_3'], 1):
            distances[f'd{i}'] = 10 ** ((A - df[rssi_col]) / (10 * n))
        
        return distances
    
    def _triangulate(self, df: pd.DataFrame, distances: pd.DataFrame) -> pd.DataFrame:
        """Estimate position using triangulation.
        
        Args:
            df: DataFrame with transmitter coordinates
            distances: DataFrame with estimated distances
            
        Returns:
            DataFrame with estimated positions
        """
        positions = pd.DataFrame()
        
        # For each row, calculate position using three transmitters
        for idx in df.index:
            # Get transmitter coordinates
            tx1 = np.array([df.loc[idx, 'X1'], df.loc[idx, 'Y1']])
            tx2 = np.array([df.loc[idx, 'X2'], df.loc[idx, 'Y2']])
            tx3 = np.array([df.loc[idx, 'X3'], df.loc[idx, 'Y3']])
            
            # Get distances
            d1 = distances.loc[idx, 'd1']
            d2 = distances.loc[idx, 'd2']
            d3 = distances.loc[idx, 'd3']
            
            # Calculate position using least squares
            pos = self._least_squares_triangulation(tx1, tx2, tx3, d1, d2, d3)
            
            positions.loc[idx, 'x'] = pos[0]
            positions.loc[idx, 'y'] = pos[1]
        
        return positions
    
    def _least_squares_triangulation(self, tx1: np.ndarray, tx2: np.ndarray, tx3: np.ndarray,
                                   d1: float, d2: float, d3: float) -> np.ndarray:
        """Calculate position using least squares method.
        
        Args:
            tx1, tx2, tx3: Transmitter coordinates
            d1, d2, d3: Estimated distances
            
        Returns:
            Estimated position [x, y]
        """
        # Formulate the system of equations
        A = np.array([
            [2*(tx1[0] - tx3[0]), 2*(tx1[1] - tx3[1])],
            [2*(tx2[0] - tx3[0]), 2*(tx2[1] - tx3[1])]
        ])
        
        b = np.array([
            d3**2 - d1**2 - tx3[0]**2 + tx1[0]**2 - tx3[1]**2 + tx1[1]**2,
            d3**2 - d2**2 - tx3[0]**2 + tx2[0]**2 - tx3[1]**2 + tx2[1]**2
        ])
        
        # Solve using least squares
        try:
            pos = np.linalg.lstsq(A, b, rcond=None)[0]
        except np.linalg.LinAlgError:
            # If matrix is singular, return midpoint of transmitters
            pos = np.mean([tx1, tx2, tx3], axis=0)
        
        return pos
    
    def _apply_kalman_filter(self, positions: pd.DataFrame) -> pd.DataFrame:
        """Apply Kalman filter to smooth position estimates.
        
        Args:
            positions: DataFrame with position estimates
            
        Returns:
            DataFrame with smoothed positions
        """
        # Prepare measurements for Kalman filter
        measurements = positions[['x', 'y']].values
        
        # Apply Kalman filter
        smoothed_positions, _ = self.kf.smooth(measurements)
        
        # Create DataFrame with smoothed positions
        result = pd.DataFrame(smoothed_positions, columns=['x', 'y'])
        
        return result 