# Alwrity - AI Generator for CopyWriting FAB Formula

Alwrity is an AI-powered generator designed to assist users in creating compelling marketing copy using the FAB (Features, Advantages, Benefits) formula. This tool leverages OpenAI's powerful ChatGPT model to generate FAB marketing copy based on user-provided inputs.

## Features

- **Input Section:** Users can input the product or service name, description, and ultimate benefits to generate FAB marketing copy.
- **Pro-Tip:** Provides guidance on how to use the FAB copywriting formula effectively.
- **Progress Spinner:** Displays a spinner during copy generation to indicate activity.
- **Error Handling:** Handles exceptions gracefully and provides helpful error messages to users.

## How to Use

1. **Input Section:** Enter the product or service name, description, and ultimate benefits in the input fields provided.
2. **Generate FAB Copy:** Click the "Get FAB Copy" button to generate FAB marketing copy based on the provided inputs.
3. **View Copy:** Once generated, the FAB marketing copy will be displayed in the web app for review and use.

## Requirements

- Python 3.6+
- Streamlit
- Tenacity
- OpenAI
- Streamlit Lottie

## How to Run

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up environment variables:
   - `OPENAI_API_KEY`: OpenAI API key.
4. Run the Alwrity script using `streamlit run alwrity.py`.
