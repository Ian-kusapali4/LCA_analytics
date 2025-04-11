import pandas as pd
from applicant import Applicant

class DataProcessor:
    """Handles reading and processing the input Excel data."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(self.file_path)

    def get_applicants(self):
        """Yields Applicant objects from the DataFrame."""
        for index, row in self.df.iterrows():
            yield Applicant(row)

    def calculate_percentage(self, scores):
        """Calculates the percentage score from a total of 20."""
        total_score = sum(scores.values())
        return (total_score / 20) * 100