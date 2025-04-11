import ollama
import re

class Scorer:
    """Responsible for scoring applicant data using Ollama."""
    def __init__(self, ollama_model='llama3'):
        self.ollama_model = ollama_model
        self.scoring_criteria = self._load_scoring_criteria()

    def _load_scoring_criteria(self):
        """Returns the scoring criteria for each category."""
        return {
            "Education": """
            0- Secondary School
            1- PhD
            2- Masters
            3- Degree / graduate / Post-graduate
            4- certificate / diploma / Undergraduate
            5- Post Secondary
            """,
            "Leadership Experience": """
            Scoring based on experience, learning, and **clarity of English expression**:
            5- Strong, detailed experience with deep learning reflections and impact demonstrated. Excellent English, clear and articulate.
            4- Well-articulated experience with meaningful insights into leadership growth. Good English with minor errors.
            3- Clear leadership experience with some reflection on lessons learned. Understandable English with noticeable errors.
            2- Basic description of experience with limited learning outcomes. Difficult to understand due to significant errors.
            1- No leadership experience or learning mentioned. Very poor English, largely incomprehensible.
            """,
            "Program Motivation": """
            Scoring based on motivation, connection to program goals, and **clarity of English expression**:
            5- Strong motivation, well-articulated connection between program and leadership goals, supported by concrete examples. Excellent English, clear and concise.
            4- Clear motivation, links personal goals to the program, but lacks concrete examples. Good English with minor errors.
            3- Some clarity but lacks depth in reasons for applying. Understandable English with noticeable errors.
            2- Weak or vague response. Difficult to understand due to significant errors.
            1- No answer or incomprehensible due to very poor English.
            """,
            "Aspirations": """
            Scoring based on connection to future leadership aspirations and **clarity of English expression**:
            5- Strong, clear link between leadership experience and societal impact. Excellent English, clear and concise.
            4- Connects past experience to future aspirations. Good English with minor errors.
            3- Mentions leadership but lacks a strong link to future goals. Understandable English with noticeable errors.
            2- No connection to future leadership aspirations or difficult to understand.
            1- No answer or incomprehensible due to very poor English.
            """
        }

    def get_scoring_criteria(self, category):
        """Returns the scoring criteria for a given category."""
        return self.scoring_criteria.get(category, "Criteria not found")

    def _score_text_with_ollama(self, text, category, applicant_answer):
        """Scores a text response using Ollama 3."""
        prompt = f"""
        Score the following applicant's answer for the "{category}" category based on the scoring criteria provided.
        Applicant's Answer: "{applicant_answer}"

        Scoring Criteria for {category}:
        {self.get_scoring_criteria(category)}

        Provide the score (0-5) as a number and a brief explanation.

        Format your response as:
        Score: [score]
        Reasoning: [your explanation]
        """
        try:
            response = ollama.chat(model=self.ollama_model, messages=[{'role': 'user', 'content': prompt}])
            response_text = response['message']['content'].strip()

            score_match = re.search(r"Score:\s*(\d+)", response_text, re.IGNORECASE)
            reasoning_match = re.search(r"Reasoning:\s*(.+)", response_text, re.IGNORECASE | re.DOTALL)

            score = 0
            reasoning = "Reasoning not found."

            if score_match:
                score = int(score_match.group(1))
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()

            return {"score": score, "reasoning": reasoning, "english_level": "N/A"}

        except Exception as e:
            print(f"Error scoring {category}: {e}")
            return {"score": 0, "reasoning": f"Error during scoring: {e}", "english_level": "Error"}

    def _score_text_with_ollama_with_english_assessment(self, text, category, applicant_answer):
        """Scores a text response and assesses English level using Ollama 3."""
        prompt = f"""
        Score the following applicant's answer for the "{category}" category based on the scoring criteria provided.
        Also, provide an assessment of the applicant's English language proficiency in this answer, categorizing it as "great", "basic", or "weak".

        Applicant's Answer: "{applicant_answer}"

        Scoring Criteria for {category}:
        {self.get_scoring_criteria(category)}

        Provide the score (0-5) as a number, followed by a brief explanation of why you gave that score, referencing specific parts of the applicant's answer. Then, on a new line, state the English level assessment.

        Format your response as:
        Score: [score]
        Reasoning: [your explanation]
        English Level: [great/basic/weak]
        """
        try:
            response = ollama.chat(model=self.ollama_model, messages=[{'role': 'user', 'content': prompt}])
            response_text = response['message']['content'].strip()

            score_match = re.search(r"Score:\s*(\d+)", response_text, re.IGNORECASE)
            reasoning_match = re.search(r"Reasoning:\s*(.+)(?:\nEnglish Level:)", response_text, re.IGNORECASE | re.DOTALL)
            english_level_match = re.search(r"English Level:\s*(great|basic|weak)", response_text, re.IGNORECASE)

            score = 0
            reasoning = "Reasoning not found."
            english_level = "Not Assessed"

            if score_match:
                score = int(score_match.group(1))
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()
            if english_level_match:
                english_level = english_level_match.group(1).lower()

            return {"score": score, "reasoning": reasoning, "english_level": english_level}

        except Exception as e:
            print(f"Error scoring {category}: {e}")
            return {"score": 0, "reasoning": f"Error during scoring: {e}", "english_level": "Error"}

    def score_education(self, education_level):
        """Scores the education level."""
        education_level_lower = education_level.strip().lower()
        if education_level_lower == "secondary school":
            return {"score": 0, "reasoning": "Directly assigned score based on 'Secondary School' criterion.", "english_level": "basic"}
        else:
            return self._score_text_with_ollama_with_english_assessment(education_level, "Education", education_level)

    def score_applicant(self, applicant):
        """Scores an applicant's responses."""
        scores = {}
        scoring_reasons = {}

        education_result = self.score_education(applicant.get_education_level())
        scoring_reasons["Education"] = education_result
        scores["Education"] = scoring_reasons["Education"]["score"]

        leadership_result = self._score_text_with_ollama_with_english_assessment(
            applicant.get_leadership_experience(),
            "Leadership Experience",
            applicant.get_leadership_experience()
        )
        scoring_reasons["Leadership Experience"] = leadership_result
        scores["Leadership Experience"] = scoring_reasons["Leadership Experience"]["score"]

        motivation_result = self._score_text_with_ollama_with_english_assessment(
            applicant.get_program_motivation(),
            "Program Motivation",
            applicant.get_program_motivation()
        )
        scoring_reasons["Program Motivation"] = motivation_result
        scores["Program Motivation"] = scoring_reasons["Program Motivation"]["score"]

        aspirations_result = self._score_text_with_ollama_with_english_assessment(
            applicant.get_aspirations(),
            "Aspirations",
            applicant.get_aspirations()
        )
        scoring_reasons["Aspirations"] = aspirations_result
        scores["Aspirations"] = scoring_reasons["Aspirations"]["score"]

        return scores, scoring_reasons

    def assess_internet_computer(self, applicant_data):
        """Heuristic assessment of internet and computer access."""
        keywords_positive = ["computer", "laptop", "internet", "online", "digital", "zoom", "reliable connection"]
        response_text = " ".join(applicant_data.astype(str).tolist()).lower()
        for keyword in keywords_positive:
            if keyword in response_text:
                return "Likely"
        return "Unclear"