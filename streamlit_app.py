import streamlit as st
from langchain_groq import ChatGroq
from utils import save_feedback
from main import create_graph
from langchain.callbacks.base import BaseCallbackHandler
import os

# Environment setup
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]["API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = "Social Media Positioning Master"

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_final=False):
        self.container = container
        self.text = initial_text
        self.placeholder = container.empty()
        self.display_final = display_final

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        if not self.silent:
            self.placeholder.markdown(self.text + "▌")

    def on_llm_end(self, *args, **kwargs) -> None:
        if not self.display_final:
            self.placeholder.empty()

def create_streaming_model(api_key: str, stream_handler: StreamHandler):
    """Create a streaming-enabled model"""
    return ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0.8,
        api_key=api_key,
        streaming=True,
        callbacks=[stream_handler]
    )

def run_analysis(model, core_value, target_audience, persona, monetization):
    """Run the positioning analysis using the graph"""
    # Create initial state
    initial_state = {
        "messages": [],
        "core_value_provided": core_value,
        "target_audience": target_audience,
        "persona": persona,
        "monetization": monetization,
        "aligned": False
    }
    
    # Create and run graph
    graph = create_graph(model)
    result = graph.invoke(initial_state)
    
    # Get the last message which will be either from AnalysisAgent or PositioningAgent
    final_message = result["messages"][-1]["content"]
    is_aligned = result["aligned"]  # This should be determined directly from the result
    return final_message, is_aligned

def display_analysis(content: str, is_aligned: bool):
    """Display the analysis with proper formatting."""
    title = "### Detailed Analysis" if is_aligned else "### Improvement Suggestions"
    st.markdown(title)
    st.markdown(content)

def main():
    st.set_page_config(
        page_title="Social Media Positioning Master",
        page_icon="🎯",
        layout="wide"
    )

    # Sidebar setup
    st.sidebar.header("💬 Social Media Positioning Master")
    st.sidebar.markdown(
        "This app analyzes the alignment between your business's core value, "
        "target audience, persona, and monetization strategy using AI. "
        "To use this App, you need to provide a Groq API key, which you can get [here](https://console.groq.com/keys) for free."
    )
    
     # Instructions
    st.sidebar.write("### Instructions")
    st.sidebar.write("1️⃣ Enter your core value proposition")
    st.sidebar.write("2️⃣ Define your target audience")
    st.sidebar.write("3️⃣ Describe your brand persona")
    st.sidebar.write("4️⃣ Explain your monetization strategy")
    st.sidebar.write("5️⃣ Click 'Analyze Positioning' for detailed insights")

    # Initialize session state
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

     # Feedback Form
    st.sidebar.subheader("Feedback Form")
    feedback = st.sidebar.text_area(
        "Your Thoughts and Feedback",
        value=st.session_state.feedback,
        placeholder="Share your feedback here..."
    )
        
    if st.sidebar.button("Submit Feedback"):
        if feedback:
            try:
                save_feedback(feedback)
                st.session_state.feedback = ""
                st.sidebar.success("Thank you for your feedback! 😊")
            except Exception as e:
                st.sidebar.error(f"Error saving feedback: {str(e)}")
        else:
            st.sidebar.error("Please enter your feedback before submitting.")

    st.sidebar.image("assets/logo01.jpg", use_column_width=True)

    # API Key Input
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key...",
        help="Your key will not be stored"
    )
    
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.", icon="🔑")
        return

    # Input Form
    with st.form("positioning_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            core_value = st.text_area(
                "Core Value Proposition",
                placeholder="e.g., Easy-to-use AI tools for automating basic business processes",
                help="What primary value or benefit does your business offer?"
            )
            
            target_audience = st.text_area(
                "Target Audience",
                placeholder="e.g., Small business owners with limited technical knowledge",
                help="Who are you trying to reach and serve?"
            )
            
        with col2:
            persona = st.text_area(
                "Brand Persona",
                placeholder="e.g., A helpful, approachable AI consultant",
                help="What character or image does your brand project?"
            )
            
            monetization = st.text_area(
                "Monetization Strategy",
                placeholder="e.g., Affordable AI software-as-a-service subscriptions",
                help="How do you generate revenue?"
            )
        
        analyze_button = st.form_submit_button("Analyze Positioning")
    
    if analyze_button:
        if not all([core_value, target_audience, persona, monetization]):
            st.error("Please fill out all fields for a complete analysis.", icon="⚠️")
            return
        
        try:
            with st.spinner("Analyzing your Social Media positioning..."):
                # Create a container for the final output
                output_container = st.container()

                # Create model with streaming handler
                stream_handler = StreamHandler(st.empty())
                model = create_streaming_model(groq_api_key, stream_handler)
                
                # Run analysis
                analysis_content, is_aligned = run_analysis(
                    model,
                    core_value,
                    target_audience,
                    persona,
                    monetization
                )

                # Only display analysis content once
                display_analysis(analysis_content, is_aligned)
                    
                st.session_state.analysis_complete = True
                
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}", icon="🚨")
            st.session_state.analysis_complete = False

if __name__ == "__main__":
    main()