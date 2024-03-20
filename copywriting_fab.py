import time #Iwish
import os
import json
import openai
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
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

    # Sidebar input for OpenAI API Key
    st.sidebar.title("FAB Copywriting")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown(f"🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")
    
    # Title and description
    st.title("✍️ Alwrity - AI Generator for CopyWriting FAB Formula")
    with st.expander("What is **Copywriting FAB formula** & **How to Use**? 📝❗"):
        st.markdown('''
           ### What's FAB copywriting Formula, How to use this AI generator 🗣️
    ---
    #### FAB Copywriting Formula

    FAB is another effective copywriting formula, standing for:

    1. **Features**: Highlight the features of the product or service.
    2. **Advantages**: Explain how these features benefit the customer.
    3. **Benefits**: Emphasize the ultimate benefits or results experienced by the customer.

    The FAB formula helps in clearly communicating the value proposition and persuading the audience to take action.

    #### FAB Copywriting Formula: Simple Example

    **Product Features:** 25MP Camera, 128GB Storage
    **Advantages:** Capture stunning photos with high resolution and store all your memories securely.
    **Benefits:** Preserve your precious moments in crystal-clear detail and never worry about running out of space.

    --- ''')
    
    # Input section
    with st.expander("**PRO-TIP** - Provide the key features, advantages, and benefits of your product or service", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            fab_product_name = st.text_input('**Enter Product/Service Name**')
        with col2:
            fab_product_details = st.text_input(f'**Describe *{fab_product_name}* Offers ?** (List the Features of {fab_product_name})')
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            fab_benefits = st.text_input(f"**Emphasize the Ultimate Benefits or Results Experienced by the Customer:**")
        with col2:
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
                            st.subheader('**👩🔬👩🔬 Your FAB Marketing Copy:**')
                            st.markdown(fab_content)
                        else:
                            st.error("💥**Failed to generate FAB Copy. Please try again!**")

    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")
    st.markdown('''
                Copywrite using FAB formula - powered by AI (OpenAI, Gemini Pro).
                Implemented by [Alwrity](https://alwrity.netlify.app).
                Know more: [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know)
                ''')


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
    
    # Exception Handling.
    copywrite_fab = openai_chatgpt(prompt)
    return copywrite_fab


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=300, top_p=0.9, n=2):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 8192.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
            # Additional parameters can be included here
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"OpenAI error: {err}")



# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url

if __name__ == "__main__":
    main()
