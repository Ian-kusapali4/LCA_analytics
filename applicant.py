class Applicant:
    """Represents a single applicant and their data."""
    def __init__(self, applicant_data):
        self.applicant_id = applicant_data.name  # Use DataFrame index as ID
        self.education_level = applicant_data.get("Level of Education", "").strip()
        self.leadership_experience_text = applicant_data.get("Tell us about your leadership experience and what you learned from it. (Limit 300 words)", "")
        self.program_motivation_text = applicant_data.get("Why are you interested in joining the Leading Change Africa Virtual Leadership Academy?\n(Limit 100 words)", "")
        self.aspirations_text = applicant_data.get("What are your long-term aspirations in education, career, or leadership? (50 words)", "")
        self.data = applicant_data # Store the entire row for the internet/computer assessment

    def get_education_level(self):
        return self.education_level

    def get_leadership_experience(self):
        return self.leadership_experience_text

    def get_program_motivation(self):
        return self.program_motivation_text

    def get_aspirations(self):
        return self.aspirations_text

    def get_data(self):
        return self.data