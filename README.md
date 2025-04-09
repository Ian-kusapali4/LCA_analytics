# Applicant Scoring and Analysis Tool

This project is a Python-based tool designed to automate the scoring and analysis of applicant data, typically sourced from an Excel spreadsheet. It leverages the power of Large Language Models (LLMs), specifically `llama3` via the `ollama` library, to evaluate applicant responses based on defined scoring criteria.

## Features

* **Automated Scoring:** Scores applicant responses across multiple categories (e.g., Education, Leadership Experience, Program Motivation, Aspirations) using the `llama3` LLM.
* **Reasoning Capture:** The LLM provides a brief explanation for each score assigned, referencing specific parts of the applicant's answer.
* **English Language Assessment:** For essay-based questions, the tool assesses the applicant's English language proficiency, categorizing it as "great," "basic," or "weak."
* **Basic Internet and Computer Access Inference:** Performs a rudimentary keyword search within the applicant data to provide a speculative assessment of their internet and computer access. **Note:** This is not a reliable method and should be treated with caution.
* **Batch Processing:** Processes applicants in batches to manage memory usage and improve efficiency for large datasets.
* **Excel Output:** Saves the original applicant data along with the generated scores, reasoning, English level assessments, and percentage scores to a new Excel file.
* **Object-Oriented Structure:** The codebase is organized using OOP principles for better modularity, maintainability, and scalability.

## Prerequisites

* **Python 3.6 or higher:** Ensure you have Python installed on your system.
* **Pandas Library:** Used for reading and writing Excel files (`pip install pandas`).
* **Ollama:** You need to have Ollama installed and running with the `llama3` model available. Follow the installation instructions on the [Ollama website](https://ollama.com/).
* **Tqdm Library:** Used for displaying progress bars during processing (`pip install tqdm`).

## Installation

1.  **Clone the repository (if applicable) or download the script.**
2.  **Install the required Python libraries:**
    ```bash
    pip install pandas ollama tqdm
    ```
3.  **Ensure Ollama is running and the `llama3` model is pulled:**
    ```bash
    ollama pull llama3
    ollama run llama3
    ```
    Keep the Ollama server running in a separate terminal.

## Usage

1.  **Prepare your applicant data:** Ensure your applicant data is in an Excel file (e.g., `applicants.xlsx`) located in the same directory as the script or provide the correct file path in the `main()` function. The Excel file should have columns corresponding to the categories you want to score (e.g., "Level of Education," "Tell us about your leadership experience...", etc.).
2.  **Run the Python script:**
    ```bash
    python your_script_name.py
    ```
    Replace `your_script_name.py` with the actual name of your Python file.
3.  **Review the output:** After the script finishes, a new Excel file (e.g., `applicant_scores_results_oop.xlsx`) will be created in the same directory. This file will contain the original applicant data along with the generated scores, reasoning, English level assessments, percentage scores, and the internet/computer access inference.

## Project Structure (OOP)

* **`Applicant` Class:** Represents a single applicant and holds their data.
* **`Scorer` Class:** Responsible for scoring applicant data using the Ollama model and applying scoring criteria. Includes methods for scoring each category and assessing English level and internet/computer access.
* **`Result` Class:** Represents the scoring results for a single applicant.
* **`DataProcessor` Class:** Handles reading and processing the input Excel data into `Applicant` objects.
* **`OutputHandler` Class:** Writes the processed results to an output Excel file.
* **`main()` function:** Orchestrates the data processing, scoring, and output generation.

## Configuration

* **`file_path`:** Set the path to your applicant data Excel file in the `main()` function.
* **`output_file`:** Define the name of the output Excel file in the `main()` function.
* **`batch_size`:** Adjust the `batch_size` in the `main()` function to control how many applicants are processed in each batch. This can be helpful for managing memory usage with large datasets.
* **Scoring Criteria:** The scoring criteria for each category are defined within the `get_scoring_criteria` method of the `Scorer` class. You can modify these criteria to fit your specific needs.
* **Ollama Model:** The script currently uses the `llama3` model. You can change this in the `Scorer`'s `__init__` method if needed.

## Important Notes and Limitations

* **Internet and Computer Access Inference:** The method used to infer internet and computer access is very basic and **highly unreliable**. It relies on the presence of certain keywords in the applicant's text. For accurate information, consider adding direct questions to your application form.
* **English Language Assessment:** While the LLM provides an assessment of English proficiency, it's important to remember that this is an AI-based evaluation and might not be perfectly accurate or aligned with human judgment. Manual review of applications, especially those flagged with "weak" English, is recommended.
* **Subjectivity of Scoring:** Scoring open-ended text responses can be subjective. The LLM's interpretations might vary. Regularly review the reasoning provided by the LLM to ensure it aligns with your expectations.
* **Error Handling:** The script includes basic error handling for Ollama communication, but you might want to add more robust error handling for production use.
* **Performance:** The processing time will depend on the size of your dataset, the complexity of the prompts, and the performance of your system and Ollama setup.

## Contributing

Contributions to this project are welcome. Feel free to fork the repository and submit pull requests with improvements or bug fixes.

## License
