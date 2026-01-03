import argparse
import os
import re
import subprocess
import sys
import hashlib
from datetime import datetime

def generate_image_filename(prompt):
    """Generates a consistent filename based on the prompt hash."""
    prompt_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8]
    return f"ai_gen_{prompt_hash}.png"

def process_slides(input_file, execute_deck=True):
    """
    Parses the input markdown file, finds 'ai-image' blocks,
    generates images using generate_image.py, and creates a processed
    markdown file with standard image links.
    """
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find ai-image blocks
    # Looking for ```ai-image ... ```
    # capturing the content inside.
    pattern = re.compile(r'```ai-image\s+(.*?)```', re.DOTALL)

    def replace_match(match):
        prompt = match.group(1).strip()
        if not prompt:
            return match.group(0) # parsing error or empty, leave it? or warn.
        
        print(f"Found ai-image prompt: {prompt[:30]}...")
        
        # Ensure regex doesn't capture leading/trailing newline issues if user formatted weirdly
        # The prompt is literally the text inside the block.
        
        # Prepare output directory
        output_dir = "assets/generated"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = generate_image_filename(prompt)
        output_path = os.path.join(output_dir, filename)
        
        # Check if we should generate (could skip if exists, but for now force or check?)
        # Let's check if it exists to save time/cost, unless forced.
        # For this implementation, we will check if it exists.
        
        if not os.path.exists(output_path):
            print(f"Generating image for: {filename}")
            
            # Create a localized temp prompt file to pass to generate_image.py
            # because generate_image.py expects a file path.
            temp_prompt_file = f"_temp_prompt_{filename}.txt"
            with open(temp_prompt_file, 'w', encoding='utf-8') as tf:
                tf.write(prompt)
            
            # Call generate_image.py
            cmd = [
                sys.executable,
                "scripts/generate_image.py",
                temp_prompt_file,
                "-o", output_path
            ]
            
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error generating image: {e}")
                # If generation fails, maybe keep the block or put a placeholder?
                # For now, we'll error out or leave the block?
                # Let's leave a placeholder text error in the slide
                return f"**FAILED TO GENERATE IMAGE: {prompt}**"
            finally:
                if os.path.exists(temp_prompt_file):
                    os.remove(temp_prompt_file)
        else:
            print(f"Image already exists, skipping generation: {filename}")

        return f"![{prompt}]({output_path})"

    new_content = pattern.sub(replace_match, content)

    # Output processed file
    base, ext = os.path.splitext(input_file)
    output_markdown = f"{base}_processed{ext}"
    
    with open(output_markdown, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Processed markdown saved to: {output_markdown}")

    if execute_deck:
        print(f"Running deck on {output_markdown}...")
        try:
            # Pass through any other arguments to deck if needed?
            # For now just simple deck command
            subprocess.run(["deck", output_markdown], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running deck: {e}")
            sys.exit(e.returncode)
        except FileNotFoundError:
            print("Error: 'deck' command not found in PATH.")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown for AI images and run deck.")
    parser.add_argument("input_file", help="Input markdown file")
    parser.add_argument("--no-deck", action="store_true", help="Skip running deck, just generate markdown")
    
    args = parser.parse_args()
    
    process_slides(args.input_file, execute_deck=not args.no_deck)
