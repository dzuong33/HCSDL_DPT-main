"""
Simple test script to verify feature extraction works
(does not require all dependencies installed)
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def test_feature_extraction(image_path):
    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return False
    
    # Try to load the image
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return False
        
        print(f"Successfully loaded image: {image_path}")
        print(f"Image shape: {image.shape}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect edges (basic feature)
        edges = cv2.Canny(gray, 100, 200)
        
        # Plot the results
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Original Image")
        plt.axis('off')
        
        plt.subplot(1, 3, 2)
        plt.imshow(gray, cmap='gray')
        plt.title("Grayscale")
        plt.axis('off')
        
        plt.subplot(1, 3, 3)
        plt.imshow(edges, cmap='gray')
        plt.title("Edge Detection")
        plt.axis('off')
        
        # Save the output
        os.makedirs("test_output", exist_ok=True)
        output_path = os.path.join("test_output", "test_result.jpg")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        print(f"Test successful! Results saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_feature_extraction.py <image_path>")
        print("Example: python test_feature_extraction.py ../mountain_images/mountain_001.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_feature_extraction(image_path) 