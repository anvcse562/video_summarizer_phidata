
import streamlit as st
import time
from pathlib import Path
import tempfile
import os
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv

load_dotenv()

# Initialize the API Key and configure Google Generative AI
API_KEY = os.getenv("GOOGLE_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if API_KEY and PROJECT_ID:
    vertexai.init(project=PROJECT_ID, location='us-central1')
else:
    raise ValueError("Missing required environment variables. Check your .env file.")

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬")
st.header("Powered by Gemini 1.5 Flash")

# Initialize Gemini model
model = GenerativeModel("gemini-1.5-pro-002")

# File uploader for video
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    # Display video on Streamlit
    st.video(video_path, format="video/mp4", start_time=0)

    # User input for analysis
    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
        help="Provide specific questions or insights you want from the video."
    )

    if st.button("🔍 Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    video_part = Part.from_uri(video_path, mime_type="video/mp4")
                    
                    prompt = f"""
                    Analyze the uploaded video for content and context.
                    Respond to the following query using video insights:
                    {user_query}

                    Provide a detailed, user-friendly, and actionable response.
                    """

                    contents = [prompt, video_part]
                    response = model.generate_content(contents)

                # Display the result from the agent
                st.subheader("Analysis Result")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
            finally:
                # Clean up temporary video file
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



####################

# from autogen import AssistantAgent, UserProxyAgent
# import google.generativeai as genai
# import tempfile
# import time
# import streamlit as st
# import os
# from dotenv import load_dotenv
# from pathlib import Path

# load_dotenv()
# os.environ.pop("OPENAI_API_KEY", None)
# API_KEY = os.getenv("GOOGLE_API_KEY")
# print(API_KEY)
# if API_KEY:
#     genai.configure(api_key=API_KEY)
# else:
#     print("GOOGLE_API_KEY not found in environment variables")

# st.set_page_config(
#     page_title="Multimodal AI Agent- Video Summarizer",
#     page_icon="🎥",
#     layout="wide"
# )
# genai.configure(api_key=API_KEY)

# st.title("AutoGen Video AI Summarizer Agent 🎥🎤🖬")
# st.header("Powered by Gemini 2.0 Flash Exp")

# config_list = [
#     {
#         "model":"gemini-pro",      #"gemini-2.0-flash-exp",
#         "api_key": API_KEY,  # Use the Google API key here.
#     }
# ]

# llm_config = {"config_list": config_list, "seed": 42}

# @st.cache_resource
# def initialize_agents():
#     assistant = AssistantAgent(
#         name="Video_Analyst",
#         llm_config=llm_config,
#         system_message="You are an expert video analyst. Analyze videos and provide detailed insights."
#     )
#     user_proxy = UserProxyAgent(
#         name="User_Proxy",
#         human_input_mode="NEVER",
#         max_consecutive_auto_reply=10,
#         is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
#         code_execution_config={"work_dir": "coding"},
#         llm_config=llm_config,
#     )
#     return assistant, user_proxy

# assistant, user_proxy = initialize_agents()

# video_file = st.file_uploader(
#     "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
# )

# if video_file:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
#         temp_video.write(video_file.read())
#         video_path = temp_video.name

#     st.video(video_path, format="video/mp4", start_time=0)

#     user_query = st.text_area(
#         "What insights are you seeking from the video?",
#         placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
#         help="Provide specific questions or insights you want from the video."
#     )

#     if st.button("🔍 Analyze Video", key="analyze_video_button"):
#         if not user_query:
#             st.warning("Please enter a question or insight to analyze the video.")
#         else:
#             try:
#                 with st.spinner("Processing video and gathering insights..."):
#                     processed_video = genai.upload_file(video_path)
#                     while processed_video.state.name == "PROCESSING":
#                         time.sleep(1)
#                         processed_video = genai.get_file(processed_video.name)

#                     analysis_prompt = f"""
#                     Analyze the uploaded video for content and context.
#                     Respond to the following query using video insights and supplementary web research:
#                     {user_query}

#                     Provide a detailed, user-friendly, and actionable response.
#                     """

#                     user_proxy.initiate_chat(
#                         assistant,
#                         message=analysis_prompt,
#                         videos=[processed_video]
#                     )

#                 st.subheader("Analysis Result")
#                 st.markdown(user_proxy.last_message()["content"])

#             except Exception as error:
#                 st.error(f"An error occurred during analysis: {error}")
#             finally:
#                 Path(video_path).unlink(missing_ok=True)
# else:
#     st.info("Upload a video file to begin analysis.")

