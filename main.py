import argparse
from tract_analysis.data_aggregation import aggregate_results_to_dataframe, save_to_excel


def main():
    """
    Main function to aggregate tractography statistics and save to an Excel file.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Aggregate tractography statistics and save to an Excel file.")

    parser.add_argument('-r', '--root_directory', type=str, required=True,
                        help='Path to the root directory containing subject directories.')
    parser.add_argument('-f', '--file_paths', nargs='+', required=True,
                        help='List of tractography file names to be processed.')
    parser.add_argument('-i', '--reference_image', type=str, required=True,
                        help='Path to the reference image file.')
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        help='Path to the output Excel file.')

    args = parser.parse_args()

    # Aggregate results from the tractography files into dataframes
    print("Aggregating results from tractography files...")
    statistical_dataframes = aggregate_results_to_dataframe(args.root_directory, args.file_paths, args.reference_image)

    # Save the aggregated dataframes to an Excel file
    print(f"Saving aggregated results to {args.output_file}...")
    save_to_excel(statistical_dataframes, args.output_file)

    print("Process completed successfully.")


if __name__ == "__main__":
    main()
