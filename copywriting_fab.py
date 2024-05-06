import os
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity FAB",
        layout="wide",
    )

    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Input section
    with st.expander("**PRO-TIP** - Provide the key features, advantages, and benefits of your product or service", expanded=True):
        fab_product_name = st.text_input('**Enter Product/Service Name**')
        fab_product_details = st.text_input(f'**Describe Your Offers ?** (List the Features of product)')
        fab_benefits = st.text_input(f"**Mention Benefits or Results Experienced by the Customer:**")
        
        # Generate FAB Copy button
        if st.button('**Get FAB Copy**'):
            # Validate input fields
            if validate_input(fab_product_name, "Product/Service Name") and \
                validate_input(fab_product_details, "Description") and \
                validate_input(fab_benefits, "Benefits"):

                # Proceed with further processing
                with st.spinner("Generating FAB Copy..."):
                    fab_content = generate_fab_copywrite(fab_product_name, fab_product_details, fab_benefits)
                    if fab_content:
                        st.subheader('**🧕 Your FAB Marketing Copy:**')
                        st.markdown(fab_content)
                        st.markdown("\n\n\n")
                    else:
                        st.error("💥**Failed to generate FAB Copy. Please try again!**")


# Function to validate if the input field is not empty
def validate_input(input_text, field_name):
    if not input_text:
        st.error(f"{field_name} is required!")
        return False
    return True


# Function to generate FAB copywrite
def generate_fab_copywrite(fab_product_name, fab_product_details, fab_benefits):
    """ Function to call upon LLM to get the work done. """

    prompt = f"""As an Expert FAB copywriter, I need your help in creating a marketing campaign for {fab_product_name}, 
        which {fab_product_details}. Your task is to incorporate the FAB copywriting framework,
        by providing the features, advantages, and benefits of {fab_benefits}.
        """
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)    


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.7,
            "top_k": 0,
            "max_output_tokens": 500,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
