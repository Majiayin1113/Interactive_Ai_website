from diffusers import DiffusionPipeline
import torch

def generate_puppy_image():
    model = "runwayml/stable-diffusion-v1-5"
    
    print("Loading the Stable Diffusion model...")
    # Load the model and move it to the GPU if available
    pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    
    # Prompt for generating a cute puppy
    prompt = "a cute little puppy, fluffy fur, adorable eyes, sitting on grass, high quality, detailed, photorealistic"
    
    print(f"Generating image with prompt: {prompt}")
    print("This may take a few moments...")
    
    # Generate the image
    images = pipe(prompt, num_inference_steps=20).images
    
    # Save and show the image
    output_path = "generated_puppy.png"
    images[0].save(output_path)
    print(f"Image saved as: {output_path}")
    
    # Display the image
    images[0].show()
    
    return images[0]

if __name__ == "__main__":
    generate_puppy_image()