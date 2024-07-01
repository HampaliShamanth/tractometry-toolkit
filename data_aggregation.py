import os
import pandas as pd
from collections import defaultdict
from tract_analysis.calculations import calculate_tract_statistics, calculate_length, calculate_span
from tract_analysis.tractogram_processing import preprocess_tractogram, voxelise_tractogram


def aggregate_results_to_dataframe(root_directory, file_paths, reference_image):
    """
    Aggregate results from multiple tractography files into dataframes.

    Parameters:
        root_directory (str): Path to the root directory containing subject directories.
        file_paths (list): List of file paths to tractography files to be analyzed.
        reference_image (str): Path to the reference image file.

    Returns:
        dfs (dict): Dictionary of dataframes containing aggregated statistics.
    """
    # Initialize a dictionary to hold dataframes for each statistic
    dfs = defaultdict(pd.DataFrame)

    # List to hold dataframes for individual subject data
    spans_data = []

    # Check if the root directory exists
    if not os.path.isdir(root_directory):
        print("Error: Root directory does not exist.")
        return dfs

    # Iterate over each subject directory in the root directory
    for subject_dir in os.listdir(root_directory):
        subject_path = os.path.join(root_directory, subject_dir)

        if os.path.isdir(subject_path):
            subject_data = {}  # Dictionary to hold file paths for each subject

            # Find the tractography files for each subject
            for file_path in file_paths:
                found_file = False
                for root, _, files in os.walk(subject_path):
                    for file in files:
                        if file == os.path.basename(file_path):
                            subject_data[os.path.basename(file_path)] = os.path.join(root, file)
                            found_file = True
                            break
                    if found_file:
                        break

            # Create a dataframe for the current subject
            df = pd.DataFrame(subject_data, index=[subject_dir])
            spans_data.append(df)

    # Concatenate all subject dataframes into a single dataframe
    if spans_data:
        result_df = pd.concat(spans_data)
    else:
        result_df = pd.DataFrame()

    # Store the dataframe of file paths in the dfs dictionary
    dfs['file_paths'] = result_df

    # Dictionary to hold statistics for all subjects and files
    all_statistics = defaultdict(list)

    # Iterate over each subject and their corresponding tractography files
    for index, row in result_df.iterrows():
        for i, file_path in enumerate(file_paths):
            tract_path = row.iloc[i]

            try:
                # Preprocess the tractogram and calculate necessary parameters
                tractogram, voxel_spacing, E1, E2 = preprocess_tractogram(tract_path, reference_image)
                lengths = calculate_length(tractogram.streamlines)
                spans = calculate_span(tractogram.streamlines)
                N, voxels_data = voxelise_tractogram(tract_path, reference_image)

                # Calculate various tract statistics
                tract_stats_dict = calculate_tract_statistics(lengths, spans, voxel_spacing, N, voxels_data)

                # Append the statistics to the all_statistics dictionary
                for stat_name, stat_value in tract_stats_dict.items():
                    all_statistics[stat_name].append((index, tract_path, stat_value))
            except Exception as e:
                print(f"Error processing file {tract_path}: {e}")

    # Convert the collected statistics into dataframes
    for stat_name, stat_list in all_statistics.items():
        stat_dict = {}
        for index, tract_path, stat_value in stat_list:
            subject_id = index
            if subject_id not in stat_dict:
                stat_dict[subject_id] = {}
            stat_dict[subject_id][os.path.basename(tract_path)] = stat_value

        # Store the dataframe of statistics in the dfs dictionary
        dfs[stat_name] = pd.DataFrame(stat_dict).T

    # Print each dataframe for verification
    for statistic, df in dfs.items():
        print(f"DataFrame for {statistic}:")
        print(df)

    return dfs


def save_to_excel(dfs, output_file):
    """
    Save the aggregated dataframes to an Excel file.

    Parameters:
        dfs (dict): Dictionary of dataframes to be saved.
        output_file (str): Path to the output Excel file.
    """
    # Use ExcelWriter to write multiple dataframes to an Excel file
    with pd.ExcelWriter(output_file) as writer:
        for stat_name, df in dfs.items():
            df.to_excel(writer, sheet_name=stat_name)
