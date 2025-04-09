import os
import numpy as np
import cv2
from skimage.feature import hog
from skimage.measure import shannon_entropy
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

def extract_color_histogram(image, bins=32):
    """Extract color histogram features from image."""
    # Convert to HSV color space which is more perceptually meaningful for natural scenes
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Extract histograms for each channel
    h_hist = cv2.calcHist([hsv], [0], None, [bins], [0, 180])
    s_hist = cv2.calcHist([hsv], [1], None, [bins], [0, 256])
    v_hist = cv2.calcHist([hsv], [2], None, [bins], [0, 256])
    
    # Normalize histograms
    h_hist = cv2.normalize(h_hist, h_hist, 0, 1, cv2.NORM_MINMAX)
    s_hist = cv2.normalize(s_hist, s_hist, 0, 1, cv2.NORM_MINMAX)
    v_hist = cv2.normalize(v_hist, v_hist, 0, 1, cv2.NORM_MINMAX)
    
    # Concatenate into a single feature vector
    return np.concatenate([h_hist, s_hist, v_hist]).flatten()

def extract_edge_features(image):
    """Extract edge-based features from image."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate edge map using Canny edge detector
    edges = cv2.Canny(gray, 100, 200)
    
    # Calculate edge density (proportion of edge pixels)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Calculate edge orientation histogram
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Compute gradient magnitude and orientation
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    orientation = np.arctan2(sobel_y, sobel_x) * (180 / np.pi) % 180
    
    # Create a histogram of edge orientations
    hist, _ = np.histogram(orientation[magnitude > 30], bins=18, range=(0, 180), density=True)
    
    # Return edge density and orientation histogram
    return np.concatenate([[edge_density], hist])

def extract_texture_features(image):
    """Extract texture features using HOG."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate HOG features
    hog_features = hog(gray, orientations=9, pixels_per_cell=(16, 16),
                       cells_per_block=(2, 2), feature_vector=True)
    
    # Normalize HOG features
    hog_features = normalize(hog_features.reshape(1, -1))[0]
    
    return hog_features

def extract_skyline_features(image):
    """Extract features related to the skyline of the mountain."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary threshold to detect sky vs. land
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find skyline (for each column, find highest non-sky pixel)
    skyline = []
    h, w = thresh.shape
    for col in range(w):
        # Find the first non-sky (white) pixel from top to bottom
        for row in range(h):
            if thresh[row, col] < 127:  # Non-sky pixel
                skyline.append(row / h)  # Normalize by height
                break
        else:
            skyline.append(1.0)  # No skyline found in this column
    
    # Simplify skyline by sampling at regular intervals
    skyline_sampled = skyline[::w//20]  # Sample ~20 points
    
    # Calculate skyline roughness (standard deviation)
    skyline_roughness = np.std(skyline)
    
    # Calculate skyline height (average position)
    skyline_height = np.mean(skyline)
    
    # Return sampled skyline points and derived metrics
    return np.concatenate([skyline_sampled, [skyline_roughness, skyline_height]])

def compute_entropy(image):
    """Compute image entropy as a measure of complexity."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate entropy
    entropy = shannon_entropy(gray)
    
    return entropy

def extract_features(image_path):
    """Extract all features from an image."""
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    
    # Extract all features
    color_features = extract_color_histogram(image)
    edge_features = extract_edge_features(image)
    texture_features = extract_texture_features(image)
    skyline_features = extract_skyline_features(image)
    entropy = compute_entropy(image)
    
    # Combine all features into a single vector
    features = np.concatenate([
        color_features, 
        edge_features, 
        texture_features, 
        skyline_features, 
        [entropy]
    ])
    
    return features

def calculate_euclidean_distance(features1, features2):
    """Calculate Euclidean distance between two feature vectors."""
    return np.sqrt(np.sum((features1 - features2) ** 2))

def visualize_features(image_path, output_dir="feature_visualization"):
    """Visualize the extracted features from an image."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    
    # Extract base filename for output
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Create a figure with multiple subplots
    plt.figure(figsize=(15, 10))
    
    # 1. Original image
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis('off')
    
    # 2. Color histogram
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    plt.subplot(2, 3, 2)
    for i, color in enumerate(['h', 's', 'v']):
        hist = cv2.calcHist([hsv], [i], None, [32], [0, 180 if i == 0 else 256])
        plt.plot(hist, label=color)
    plt.title("HSV Histogram")
    plt.legend()
    
    # 3. Edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    plt.subplot(2, 3, 3)
    plt.imshow(edges, cmap='gray')
    plt.title("Edge Detection")
    plt.axis('off')
    
    # 4. HOG Visualization (simplified)
    plt.subplot(2, 3, 4)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    plt.imshow(magnitude, cmap='viridis')
    plt.title("Gradient Magnitude (HOG)")
    plt.axis('off')
    
    # 5. Skyline Detection
    plt.subplot(2, 3, 5)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plt.imshow(thresh, cmap='gray')
    plt.title("Skyline Detection")
    plt.axis('off')
    
    # 6. Entropy visualization
    plt.subplot(2, 3, 6)
    from scipy.ndimage import uniform_filter
    entropy_img = np.zeros_like(gray, dtype=float)
    for i in range(0, gray.shape[0], 9):
        for j in range(0, gray.shape[1], 9):
            patch = gray[i:i+9, j:j+9]
            if patch.size > 0:
                entropy_img[i:i+9, j:j+9] = shannon_entropy(patch)
    entropy_img = uniform_filter(entropy_img, size=5)
    plt.imshow(entropy_img, cmap='inferno')
    plt.title(f"Entropy: {shannon_entropy(gray):.2f}")
    plt.axis('off')
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_features.jpg"))
    plt.close()
    
    print(f"Feature visualization saved to {os.path.join(output_dir, f'{base_name}_features.jpg')}")

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mountain_feature_extractor.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    features = extract_features(image_path)
    print(f"Extracted {len(features)} features from {image_path}")
    
    # Visualize features
    visualize_features(image_path) 