from data_processor import DataProcessor
from scorer import Scorer
from output_handler import OutputHandler
from result import Result
from tqdm import tqdm

def main():
    file_path = r"C:\Users\BLESSINGS\Documents\applicants\applicants.xlsx"
    output_file = r"C:\Users\BLESSINGS\Documents\applicants\applicant_scores_results_oop.xlsx"
    batch_size = 10

    data_processor = DataProcessor(file_path)
    scorer = Scorer()
    output_handler = OutputHandler(output_file)
    all_results = []

    applicants = list(data_processor.get_applicants())
    for i in tqdm(range(0, len(applicants), batch_size), desc="Processing Batches"):
        batch = applicants[i:i + batch_size]
        batch_results = []
        for applicant in batch:
            scores, scoring_reasons = scorer.score_applicant(applicant)
            percentage = data_processor.calculate_percentage(scores)
            internet_computer = scorer.assess_internet_computer(applicant.get_data())
            result = Result(applicant.applicant_id, scores, scoring_reasons, percentage, internet_computer)
            batch_results.append(result.to_dict())
        all_results.extend(batch_results)

    output_handler.write_results_to_excel(all_results)

if __name__ == "__main__":
    main()