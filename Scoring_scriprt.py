import pandas as pd
import ollama
import re
from tqdm import tqdm

def score_applicant(applicant_data, scoring_reasons):
    """Scores an applicant's responses and captures reasoning using Ollama 3."""
    scores = {}
    education_level = applicant_data["Level of Education"].strip().lower()
    if education_level == "secondary school":
        scores["Education"] = 0
        scoring_reasons["Education"] = {"score": 0, "reasoning": "Directly assigned score based on 'Secondary School' criterion.", "english_level": "basic"} # Assuming basic for secondary school
    else:
        education_result = score_text_with_ollama_with_english_assessment(applicant_data["Level of Education"], "Education", applicant_data["Level of Education"])
        scoring_reasons["Education"] = education_result
        scores["Education"] = scoring_reasons["Education"]["score"]

    leadership_result = score_text_with_ollama_with_english_assessment(
        applicant_data["Tell us about your leadership experience and what you learned from it. (Limit 300 words)"],
        "Leadership Experience",
        applicant_data["Tell us about your leadership experience and what you learned from it. (Limit 300 words)"]
    )
    scoring_reasons["Leadership Experience"] = leadership_result
    scores["Leadership Experience"] = scoring_reasons["Leadership Experience"]["score"]

    motivation_result = score_text_with_ollama_with_english_assessment(
        applicant_data["Why are you interested in joining the Leading Change Africa Virtual Leadership Academy?\n(Limit 100 words)"],
        "Program Motivation",
        applicant_data["Why are you interested in joining the Leading Change Africa Virtual Leadership Academy?\n(Limit 100 words)"]
    )
    scoring_reasons["Program Motivation"] = motivation_result
    scores["Program Motivation"] = scoring_reasons["Program Motivation"]["score"]

    aspirations_result = score_text_with_ollama_with_english_assessment(
        applicant_data["What are your long-term aspirations in education, career, or leadership? (50 words)"],
        "Aspirations",
        applicant_data["What are your long-term aspirations in education, career, or leadership? (50 words)"]
    )
    scoring_reasons["Aspirations"] = aspirations_result
    scores["Aspirations"] = scoring_reasons["Aspirations"]["score"]

    return scores, scoring_reasons

def score_text_with_ollama(text, category, applicant_answer):
    """Scores a text response using Ollama 3."""
    prompt = f"""
    Score the following applicant's answer for the "{category}" category based on the scoring criteria provided.
    Applicant's Answer: "{applicant_answer}"

    Scoring Criteria for {category}:
    {get_scoring_criteria(category)}

    Provide the score (0-5) as a number and a brief explanation.

    Format your response as:
    Score: [score]
    Reasoning: [your explanation]
    """
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        response_text = response['message']['content'].strip()

        score_match = re.search(r"Score:\s*(\d+)", response_text, re.IGNORECASE)
        reasoning_match = re.search(r"Reasoning:\s*(.+)", response_text, re.IGNORECASE | re.DOTALL)

        score = 0
        reasoning = "Reasoning not found."

        if score_match:
            score = int(score_match.group(1))
        if reasoning_match:
            reasoning = reasoning_match.group(1).strip()

        return {"score": score, "reasoning": reasoning, "english_level": "N/A"} # Added english_level

    except Exception as e:
        print(f"Error scoring {category}: {e}")
        return {"score": 0, "reasoning": f"Error during scoring: {e}", "english_level": "Error"} # Added english_level

def score_text_with_ollama_with_english_assessment(text, category, applicant_answer):
    """Scores a text response and assesses English level using Ollama 3."""
    prompt = f"""
    Score the following applicant's answer for the "{category}" category based on the scoring criteria provided.
    Also, provide an assessment of the applicant's English language proficiency in this answer, categorizing it as "great", "basic", or "weak".

    Applicant's Answer: "{applicant_answer}"

    Scoring Criteria for {category}:
    {get_scoring_criteria(category)}

    Provide the score (0-5) as a number, followed by a brief explanation of why you gave that score, referencing specific parts of the applicant's answer. Then, on a new line, state the English level assessment.

    Format your response as:
    Score: [score]
    Reasoning: [your explanation]
    English Level: [great/basic/weak]
    """
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        response_text = response['message']['content'].strip()

        score_match = re.search(r"Score:\s*(\d+)", response_text, re.IGNORECASE)
        reasoning_match = re.search(r"Reasoning:\s*(.+)(?:\nEnglish Level:)", response_text, re.IGNORECASE | re.DOTALL)
        english_level_match = re.search(r"English Level:\s*(great|basic|weak)", response_text, re.IGNORECASE)

        score = 0
        reasoning = "Reasoning not found."
        english_level = "Not Assessed"

        score = int(score_match.group(1))
        if reasoning_match:
            reasoning = reasoning_match.group(1).strip()
        if english_level_match:
            english_level = english_level_match.group(1).lower()

        return {"score": score, "reasoning": reasoning, "english_level": english_level}

    except Exception as e:
        print(f"Error scoring {category}: {e}")
        return {"score": 0, "reasoning": f"Error during scoring: {e}", "english_level": "Error"}

def get_scoring_criteria(category):
    """Returns the scoring criteria for a given category."""
    criteria = {
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
    return criteria.get(category, "Criteria not found")

def calculate_percentage(scores):
    """Calculates the percentage score from a total of 20."""
    total_score = sum(scores.values())
    return (total_score / 20) * 100

def assess_internet_computer(applicant_data):
    """Heuristic assessment of internet and computer access (very basic)."""
    # This is a very rudimentary approach and likely inaccurate.
    # Consider more direct questions in your application if this is critical.
    keywords_positive = ["computer", "laptop", "internet", "online", "digital", "zoom", "reliable connection"]
    response_text = " ".join(applicant_data.astype(str).tolist()).lower()
    for keyword in keywords_positive:
        if keyword in response_text:
            return "Likely"
    return "Unclear"

# Main execution
df = pd.read_excel(r"C:\Users\BLESSINGS\Documents\applicants\applicants.xlsx")

batch_size = 10  # You can adjust this value
all_results = []

# Use tqdm to create a progress bar for the batches
for i in tqdm(range(0, len(df), batch_size), desc="Processing Batches"):
    batch = df[i:i + batch_size]
    batch_scores = []
    batch_percentages = []
    batch_scoring_reasons = []
    batch_english_levels = []
    batch_internet_computer = []

    # Use tqdm to create a progress bar for the applicants within each batch (optional)
    for index, row in batch.iterrows():
        scoring_reasons = {}
        applicant_scores, scoring_reasons = score_applicant(row, scoring_reasons)
        percentage = calculate_percentage(applicant_scores)
        english_levels = {cat: scoring_reasons[cat].get('english_level', 'N/A') for cat in scoring_reasons}
        internet_computer_assessment = assess_internet_computer(row)

        batch_scores.append(applicant_scores)
        batch_percentages.append(percentage)
        batch_scoring_reasons.append(scoring_reasons)
        batch_english_levels.append(english_levels)
        batch_internet_computer.append(internet_computer_assessment)

    batch_scores_df = pd.DataFrame(batch_scores, index=batch.index)
    batch_reasons_df_list = []
    batch_english_levels_df_list = []
    for i in range(len(batch_scoring_reasons)):
        reason_dict = {}
        english_dict = {}
        reasons = batch_scoring_reasons[i]
        english = batch_english_levels[i]
        for cat in reasons:
            reason_dict[f"{cat}_Score"] = reasons[cat]['score']
            reason_dict[f"{cat}_Reasoning"] = reasons[cat]['reasoning']
            english_dict[f"{cat}_English_Level"] = english[cat]
        batch_reasons_df_list.append(reason_dict)
        batch_english_levels_df_list.append(english_dict)

    batch_reasons_df = pd.DataFrame(batch_reasons_df_list, index=batch.index)
    batch_english_levels_df = pd.DataFrame(batch_english_levels_df_list, index=batch.index)
    batch_percentages_series = pd.Series(batch_percentages, index=batch.index, name='Percentage')
    batch_internet_computer_series = pd.Series(batch_internet_computer, index=batch.index, name='Good Internet and Computer (Inferred)')

    batch_results = pd.concat([batch, batch_scores_df, batch_reasons_df, batch_english_levels_df, batch_percentages_series, batch_internet_computer_series], axis=1)
    all_results.append(batch_results)

# Concatenate all batch results
final_df = pd.concat(all_results)

# Save to a new Excel file
final_df.to_excel(r"C:\Users\BLESSINGS\Documents\applicants\applicant_scores_results_with_english_internet.xlsx", index=False)

print(f"Applicant scores, reasoning, English level assessment, and internet/computer inference saved to applicant_scores_results_with_english_internet.xlsx in batches of {batch_size}")