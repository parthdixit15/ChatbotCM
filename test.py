import json
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import nltk
import chainlit as cl

# Download the Punkt tokenizer models
nltk.download('punkt')

# Load QA pairs from a JSON file
def load_qa_json(filepath):
    """Load question-answer pairs from a JSON file."""
    with open(filepath, 'r') as file:
        qa_pairs = json.load(file)
    return qa_pairs

# Extract text from a PDF file using fitz (PyMuPDF)
def extract_text_from_pdf(filepath):
    """Extract text content from a PDF file."""
    pdf_document = fitz.open(filepath)
    text = ''
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to find the most similar question using TF-IDF and cosine similarity
def get_most_similar_question(user_question, qa_pairs):
    """Find the most similar predefined question to the user's input using TF-IDF and cosine similarity."""
    questions = [qa['question'] for qa in qa_pairs]
    vectorizer = TfidfVectorizer().fit_transform([user_question] + questions)
    similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    most_similar_idx = similarities.argmax()
    similarity_score = similarities[0, most_similar_idx]
    
    # Debugging
    print(f"QA Similarity Scores: {similarities}")
    print(f"Most Similar Index: {most_similar_idx}")
    print(f"Similarity Score: {similarity_score}")

    if similarity_score > 0.6:  # Adjust the threshold as needed
        return qa_pairs[most_similar_idx]['answer']
    return None

# Function to search for relevant information in PDF text
def search_pdf_text(question, pdf_text):
    """Search for relevant information in the extracted PDF text."""
    sentences = sent_tokenize(pdf_text)
    vectorizer = TfidfVectorizer().fit_transform([question] + sentences)
    similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    most_similar_idx = similarities.argmax()
    similarity_score = similarities[0, most_similar_idx]

    # Debugging
    print(f"PDF Similarity Scores: {similarities}")
    print(f"Most Similar Index: {most_similar_idx}")
    print(f"Similarity Score: {similarity_score}")

    if similarity_score > 0.3:  # Adjust the threshold as needed
        return sentences[most_similar_idx]
    return None

# Maintain conversation context
conversation_history = []

# Main chatbot function with contextual awareness
def chatbot(question, qa_pairs, pdf_text):
    """Provide an answer to the user's question using QA pairs and PDF text with context."""
    global conversation_history
    conversation_history.append(question)

    # Generate context-based question
    context_question = " ".join(conversation_history[-3:])  # Use the last 3 messages for context

    # Try to get an answer from QA pairs
    answer = get_most_similar_question(question, qa_pairs)
    if not answer:
        # If not found in QA pairs, try the PDF content
        answer = search_pdf_text(question, pdf_text)
    if not answer:
        # Default response if no relevant information is found
        answer = "Please contact the business directly."

    # Append answer to history
    conversation_history.append(answer)
    return answer

# Chainlit async function to handle user messages
@cl.on_message
async def main(message: cl.Message):
    # Load data
    qa_pairs = load_qa_json('./Questions.json')  
    pdf_text = extract_text_from_pdf('./Corpus.pdf')  

    # Get answer from chatbot
    answer = chatbot(message.content, qa_pairs, pdf_text)
    
    # Send the answer back to the user
    await cl.Message(
        content=answer
    ).send()
