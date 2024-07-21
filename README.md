
# Chatbot with predefined QnA pair and information from PDF
This repository contains a chatbot implementation that leverages both predefined question-answer pairs and information extracted from a PDF document. It uses Chainlit for handling user interactions and processes user questions to provide relevant responses based on the provided data.



## Installation

Create and activate a virtual environment(optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
Install the required packages

```bash
pip install -r requirements.txt
```

## Required python packages

Ensure your requirements.txt includes the following packages:

```bash
nltk
PyMuPDF
scikit-learn
chainlit
```
If you don't have a requirements.txt, you can install the packages manually:
```bash
pip install pymupdf nltk scikit-learn chainlit
```
## Prepare the Data
1. Ensure you have a JSON file named Questions.json
2. Ensure you have a PDF file named Corpus.pdf with the relevant company information.


## Running the chatbot

1. Place the PDF file (Corpus.pdf) and the JSON file in the same directory as the script.

2. Run the script using chainlit:

```bash
chainlit run app.py
```
3. Interact with the Chatbot: Open a web browser and navigate to the Chainlit interface URL provided in the terminal after running the above command. This is typically http://localhost:8000 or a similar address



## Troubleshooting

**FileNotFoundError**: Ensure that the file paths in the script are correctly specified and the files exist in those locations.

**ModuleNotFoundError**: Verify that all required packages are installed and that you are using the correct Python environment



    