import requests
import os

def chat_with_llama(prompt, model="llama-3.1-70b", api_key=os.getenv("GROQ_API_KEY"), endpoint_url="<ENDPOINT_URL>"):
    """
    Sends a prompt to the ChatGroq API and retrieves the response from the LLaMA 3.1 model.
    
    Parameters:
        prompt (str): The user prompt to send to the LLaMA model.
        model (str): The name of the model to use (default is 'llama-3.1-70b').
        api_key (str): Your API key for authentication.
        endpoint_url (str): The API endpoint URL.
    
    Returns:
        str: The response from the LLaMA model.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 300,  # Adjust the response length as needed
        "temperature": 0.7,  # Adjust for creativity (0.0 = deterministic, 1.0 = very creative)
        "top_p": 0.9        # Nucleus sampling (adjust as needed)
    }
    
    try:
        response = requests.post(endpoint_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "No response received")
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    prompt = "Explain the concept of reinforcement learning in simple terms."
    api_key = "your_actual_api_key"  # Replace with your API key
    endpoint_url = "https://api.chatgroq.com/v1/completions"  # Replace with the correct URL
    
    response = chat_with_llama(prompt, api_key=api_key, endpoint_url=endpoint_url)
    print("LLaMA Model Response:", response)
