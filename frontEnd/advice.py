import logging
from backEnd.data_validation import UserData
from backEnd.recommender import generate_advice_stream
import streamlit as st

logger = logging.getLogger(__name__)

def generate_advice_ui(inputs: UserData):
    """
    Generate and display financial advice in the Streamlit UI.

    Args:
        inputs (UserData): The user's financial data and goals.
    """
    advice_placeholder = st.empty()
    complete_advice = ""

    advice_placeholder.text("Generating Financial Advice...")

    try:
        for advice_chunk in generate_advice_stream(inputs):
            if advice_chunk:
                complete_advice += advice_chunk
                advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)
            else:
                logger.warning("Received empty advice chunk")

    except ValueError as ve:
        error_message = f"Invalid input data: {str(ve)}"
        logger.error(error_message)
        st.error(error_message)

    except ConnectionError as ce:
        error_message = "Unable to connect to the advice generation service. Please try again later."
        logger.error(f"Connection error: {str(ce)}")
        st.error(error_message)

    except Exception as e:
        error_message = "An unexpected error occurred while generating advice."
        logger.exception(f"Unexpected error in generate_advice_ui: {str(e)}")
        st.error(error_message)

    finally:
        if not complete_advice:
            st.warning("No advice was generated. Please check your inputs and try again.")
        else:
            st.success("Financial advice generation complete!")
