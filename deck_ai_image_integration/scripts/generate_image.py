import argparse
import os
import sys
import base64
import requests
import json

def generate_image(prompt_file, output_file):
    """
    Generates an image using Gemini/Imagen API based on the prompt in prompt_file
    and saves it to output_file.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Prompt file '{prompt_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if not prompt:
        print("Error: Prompt is empty.", file=sys.stderr)
        sys.exit(1)

    print(f"Generating image for prompt: {prompt[:50]}...")

    # API Endpoint for Imagen on Google AI Studio
    # Note: Using v1beta/models/imagen-3.0-generate-001:predict
    # If this specific model/endpoint is not available for the key, it will fail.
    # Users may need to adjust the model name (e.g. to 'gemini-2.0-flash-exp' if that supports image gen via generateContent).
    
    # Attempt 1: Imagen 3.0 via REST
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "instances": [
            {"prompt": prompt}
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9" # Useful for slides
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            print(f"Error calling API: {response.status_code} - {response.text}", file=sys.stderr)
            # Fallback suggestion or handling specific errors could go here
            sys.exit(1)
            
        result = response.json()
        
        # Parse the response (structure depends on the specific endpoint version, but typically:)
        # { "predictions": [ { "bytesBase64Encoded": "..." } ] }
        # OR 
        # { "predictions": [ { "mimeType": "image/png", "bytesBase64Encoded": "..." } ] }
        
        predictions = result.get("predictions")
        if not predictions:
            print(f"No predictions found in response: {result}", file=sys.stderr)
            sys.exit(1)
            
        image_data_b64 = predictions[0].get("bytesBase64Encoded")
        if not image_data_b64:
             print(f"No image data in prediction: {predictions[0]}", file=sys.stderr)
             sys.exit(1)
             
        image_bytes = base64.b64decode(image_data_b64)
        
        with open(output_file, "wb") as f:
            f.write(image_bytes)
            
        print(f"Image successfully saved to {output_file}")

    except Exception as e:
        print(f"Exception during generation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate image from prompt file.")
    parser.add_argument("prompt_file", help="Path to file containing the prompt")
    parser.add_argument("-o", "--output", required=True, help="Path to output image file")
    args = parser.parse_args()
    
    generate_image(args.prompt_file, args.output)
