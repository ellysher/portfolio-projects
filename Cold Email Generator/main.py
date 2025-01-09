import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    # App title with an emoji for added appeal
    st.title("📧 Cold Mail Generator for Quantum AI")
    
    # Add a header image or logo
    st.image("logo.png", use_container_width=True, caption="Effortlessly Generate Professional Cold Emails")

    # Create a sidebar for navigation or additional options
    st.sidebar.title("App Options")
    st.sidebar.markdown("Select the options below to customize your experience.")
    
    # Sidebar options
    st.sidebar.checkbox("Enable Advanced Features", key="advanced")
    st.sidebar.selectbox("Choose Email Tone:", ["Professional", "Casual", "Friendly"], key="tone")
    
    # Main app layout
    st.markdown("## Generate a Cold Email with Ease")
    st.markdown("Provide the URL of the job posting or target website, and our fine-tuned AI model will craft a personalized email for you.")

    # Input field with placeholder and initial value
    url_input = st.text_input(
        "Enter the URL of the job posting or target website:", 
        value="https://jobs.nike.com/job/R-48652",
        placeholder="e.g., https://jobs.company.com/job-description"
    )

    # Initialize session state for generated email content
    if "generated_email" not in st.session_state:
        st.session_state.generated_email = ""

    # Submit button with custom styling
    submit_button = st.button("🚀 Generate Email", key="submit")

    # Process submission
    if submit_button:
        if url_input.strip():
            st.success("Processing the provided URL... ✨")
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.session_state.generated_email = email  # Update session state with generated email
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.error("Please enter a valid URL before submitting.")

    # Display the generated email in a text area
    st.text_area("Generated Email", value=st.session_state.generated_email, height=300)

    # Footer with contact info or credits
    st.markdown("---")
    st.markdown(
        "#### Created by [Elisha Aura](https://yourportfolio.com) "
    )


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
