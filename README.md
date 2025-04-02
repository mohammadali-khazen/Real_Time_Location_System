# Real-Time Location System (RTLS)

A Python-based Real-Time Location System (RTLS) that uses Bluetooth Low Energy (BLE) technology to track workers and objects in construction sites. The system localizes the position of workers wearing hardhats equipped with receivers that communicate with fixed transmitters on the job site.

## Features

- Real-time position tracking using BLE technology
- Modular infrastructure placement strategy
- Robust data processing and filtering
- Advanced localization algorithms combining triangulation and Kalman filtering
- Visualization of tracking results
- Support for multiple transmitters and receivers

## Project Structure

```
Real_Time_Location_System/
├── data/
│   ├── raw/                    # Raw data files
│   │   ├── elasticsearch/      # Elasticsearch datasets
│   │   └── rssi_dataset/       # RSSI-distance relationship data
│   ├── processed/              # Processed data files
│   └── results/                # Output results and visualizations
├── rtls/                       # Main package directory
│   ├── config/                 # Configuration files
│   ├── data/                   # Data processing modules
│   ├── models/                 # Localization models
│   └── utils/                  # Utility functions
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation file
└── README.md                   # This file
```

## System Architecture

The system consists of four main modules:

1. **Data Pre-Processing**

   - Processes raw data from Elasticsearch
   - Converts transmitter IDs to coordinates
   - Implements Semi-Logical to Logical record conversion
   - Handles data cleaning and validation

2. **RSSI-Distance Prediction**

   - Converts Received Signal Strength Indicator (RSSI) to distance
   - Uses calibrated path loss model
   - Handles signal attenuation and interference

3. **Position Estimation**

   - Implements triangulation-based localization
   - Uses least squares method for position calculation
   - Supports multiple transmitter configurations
   - Handles edge cases and error conditions

4. **Position Post-Processing**
   - Applies Kalman filtering for position smoothing
   - Reduces noise and improves accuracy
   - Handles missing or invalid data

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Real_Time_Location_System.git
cd Real_Time_Location_System
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:

```bash
pip install -e .
```

For development installation:

```bash
pip install -e ".[dev]"
```

## Usage

1. Prepare your data:

   - Place your raw data file in the `data/raw` directory
   - Ensure the data follows the expected format (see Data Format section)

2. Run the localization system:

```bash
python -m rtls.main
```

3. View results:
   - Check the `data/results` directory for:
     - `localization_results.csv`: Detailed position data
     - `localization_plot.png`: Visualization of tracking results

## Configuration

The system can be configured through `rtls/config/settings.py`:

- Transmitter coordinates
- Maximum transmitter distance
- Kalman filter parameters
- Data processing parameters
