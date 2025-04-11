class Result:
    """Represents the scoring results for a single applicant."""
    def __init__(self, applicant_id, scores, scoring_reasons, percentage, internet_computer_assessment):
        self.applicant_id = applicant_id
        self.scores = scores
        self.scoring_reasons = scoring_reasons
        self.percentage = percentage
        self.internet_computer_assessment = internet_computer_assessment

    def to_dict(self):
        """Returns the result as a dictionary for DataFrame creation."""
        result_dict = {"Applicant_ID": self.applicant_id, "Percentage": self.percentage, "Good Internet and Computer (Inferred)": self.internet_computer_assessment}
        for cat, score in self.scores.items():
            result_dict[f"{cat}_Score"] = score
        for cat, reasons in self.scoring_reasons.items():
            result_dict[f"{cat}_Reasoning"] = reasons.get("reasoning", "N/A")
            result_dict[f"{cat}_English_Level"] = reasons.get("english_level", "N/A")
        return result_dict