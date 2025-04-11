import pandas as pd

class OutputHandler:
    """Writes the processed results to an output Excel file."""
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

    def write_results_to_excel(self, all_results):
        """Writes the list of result dictionaries to an Excel file."""
        results_df = pd.DataFrame(all_results)
        results_df.to_excel(self.output_file_path, index=False)
        print(f"Applicant scores, reasoning, etc. saved to {self.output_file_path} using OOP structure.")