"""Configuration settings for the RTLS system."""

from typing import Dict, Tuple

# Transmitter coordinates mapping
TRANSMITTER_COORDS: Dict[str, Tuple[float, float]] = {
    '00000058': (3.0, 0.0),
    '00000059': (0.0, 3.0),
    '00000060': (6.0, 0.0),
    '00000061': (3.0, 3.0),
    '0000004d': (0.0, 0.0),
    '0000004e': (6.0, 3.0),
}

# Maximum distance between transmitters for logical records (in meters)
MAX_TRANSMITTER_DISTANCE: float = 4.25

# Kalman filter parameters
KALMAN_FILTER_PARAMS = {
    'transition_matrices': [[1, 0, 1, 0],
                          [0, 1, 0, 1],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]],
    'observation_matrices': [[1, 0, 0, 0],
                           [0, 1, 0, 0]],
    'initial_state_mean': [0, 0, 0, 0],
    'initial_state_covariance': [[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]],
    'transition_covariance': [[0.1, 0, 0, 0],
                            [0, 0.1, 0, 0],
                            [0, 0, 0.1, 0],
                            [0, 0, 0, 0.1]],
    'observation_covariance': [[0.1, 0],
                             [0, 0.1]],
}

# Data processing parameters
RSSI_COLUMNS = ['rssi_1', 'rssi_2', 'rssi_3']
INSTANCE_COLUMNS = ['instance_1', 'instance_2', 'instance_3']
COORDINATE_COLUMNS = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3'] 