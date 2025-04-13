import os
import requests
import gradio as gr

# Retrieve the API key from the environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing! Set it in the Hugging Face Spaces 'Secrets'.")

# Define the API endpoint and headers
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {groq_api_key}"}

# Function to interact with Groq API
def chat_with_groq(user_input):
    # Check if question is related to materials science
    keywords = [
        "material", "materials", "alloy", "composite", "polymer", "ceramic",
        "application", "mechanical properties", "thermal properties", "corrosion",
        "creep", "fatigue", "strength", "tensile", "impact", "fracture", "modulus"
    ]
    
    if not any(word in user_input.lower() for word in keywords):
        return "⚠️ I am an expert in Materials Science, ask me anything about it and I will try my best to answer. Anything outside, feel free to use ChatGPT! 🙂"

    system_prompt = (
        "You are an expert materials scientist. When a user asks about the best materials for a specific application, "
        "provide the top 3 material choices. First, list the key properties required for that application. Then show a clean, "
        "side-by-side comparison in markdown table format of the three materials, with the properties as rows and materials as columns. "
        "Include their relevant mechanical, thermal, and chemical properties. Conclude with a brief summary of which might be best depending on the scenario."
    )
    
    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.json()}"

# Build Gradio interface with better layout and custom styling
with gr.Blocks(title="Materials Science Expert Chatbot", css="""
    #orange-btn {
        background-color: #f97316 !important;
        color: white !important;
        border: none;
        font-weight: bold;
    }
""") as demo:
    
    gr.Markdown("## 🧪 Materials Science Expert\nAsk about the best materials for any engineering or industrial application.")

    with gr.Row():
        with gr.Column(scale=3):
            user_input = gr.Textbox(
                lines=2,
                placeholder="e.g. Best materials for high-temperature turbine blades...",
                label="Ask your question"
            )
        with gr.Column(scale=1, min_width=100):
            submit_btn = gr.Button("Submit", variant="primary", elem_id="orange-btn")

    gr.Markdown("#### 📌 Popular Materials Science related questions")
    gr.Markdown("""
- What are the best corrosion-resistant materials for marine environments (e.g., desalination)?
- Which materials are ideal for solar panel coatings and desert heat management?
- What materials are used for aerospace structures in extreme climates?
- Best high-strength materials for construction in the Gulf region?
- What advanced materials are used in electric vehicles and batteries in the UAE?
- How can one leverage AI/ML techniques in Materials Science?
- I’m a recent high school graduate interested in science. How can I explore Materials Science with AI/ML?
- -------------------------------------------------------------------------
    """)

    output = gr.Markdown()

    submit_btn.click(chat_with_groq, inputs=user_input, outputs=output)

# Launch the app
if __name__ == "__main__":
    demo.launch()
