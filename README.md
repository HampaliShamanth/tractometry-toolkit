# Tractography Analysis Toolkit

## Overview
The **Tractography Analysis Toolkit** is a Python program designed to derive statistical measures from white matter tracts obtained via tractography. This program quantifies the morphology and structural characteristics of various white matter tracts, enabling objective comparisons between tracts, such as the left and right *Arcuate Fasciculus* (AF_L and AF_R), or determining differences in curvature due to pathological alterations like tumors.

![Alt text](images/shape_analysis_image.png)
![Alt text](images/shape_analysis_image_2.png)


## Objectives
- Compute a set of statistical measures for white matter tracts from tractography data.
- Follow methodologies and metrics outlined in the paper "Shape analysis of the human association pathways" by Fang-Cheng Yeh.
- Aggregate data from multiple subjects into structured Pandas DataFrames for easy analysis and visualization.

## Features
- **Extraction of Tract Metrics**: Calculate metrics such as the number of tracts, mean length, span, curl, elongation, diameter, volume, surface area, and irregularity.
- **Data Input and Organization**: Dynamically handle input of tractography data files and organize data for each tract.
- **Output Format and Labeling**: Output a structured report with the calculated metrics for each tract.
- **Automated Data Aggregation**: Aggregate experiment results from multiple subjects stored across different directories into a Pandas DataFrame.

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your_username/tractography-analysis.git
   cd tractography-analysis
2. Install required dependencies
   ```bash
   pip install -r requirements.txt
## Usage
Compute Tract Statistics
    ```bash
    
    from tract_analysis.data_aggregation import aggregate_results_to_dataframe, save_to_excel
    
    # Define parameters
    root_directory = '/path/to/root_directory'
    file_paths = ['AF_L.tck', 'AF_R.tck']
    reference_image = "/path/to/reference_image.nii"
    output_file = '/path/to/output_file.xlsx'
    
    # Aggregate results into dataframes
    statistical_dataframes = aggregate_results_to_dataframe(root_directory, file_paths, reference_image)
    
    # Save the aggregated dataframes to an Excel file
    save_to_excel(statistical_dataframes, output_file)

Command Line Interface (CLI)
    ```bash
    
    python -m tract_analysis.main -r /path/to/root_directory -f AF_L.tck AF_R.tck -i /path/to/reference_image.nii -o /path/to/output_file.xlsx

Project Structure
    ''''bash

    tract_analysis/
    │
    ├── __init__.py
    ├── calculations.py
    ├── data_aggregation.py
    ├── main.py
    ├── tractogram_processing.py
    ├── utils.py
    │
    └── tests/
        ├── __init__.py
        ├── test_calculations.py
        ├── test_data_aggregation.py
        ├── test_main.py
        ├── test_tractogram_processing.py
        ├── test_utils.py

## Acknowledgments
This toolkit follows methodologies and metrics outlined in the paper "Shape analysis of the human association pathways" by Fang-Cheng Yeh.

