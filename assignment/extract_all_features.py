import os
import numpy as np
import pickle
import pandas as pd
from mountain_feature_extractor import extract_features, visualize_features
from tqdm import tqdm
import pymongo
from datetime import datetime

# Cập nhật URI MongoDB Atlas mặc định
DEFAULT_MONGODB_URI = "mongodb+srv://vuduy050903:JggOWW4dggxdA5IE@cluster0.rowvk9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def extract_features_from_directory(image_dir, output_dir="output", upload_to_mongodb=True, mongodb_uri=None):
    """Extract features from all images in a directory and save them."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Dictionary to store features
    features_dict = {}
    
    print(f"Extracting features from {len(image_files)} images...")
    
    # Extract features from each image
    for image_file in tqdm(image_files):
        image_path = os.path.join(image_dir, image_file)
        try:
            # Extract features
            features = extract_features(image_path)
            
            # Store features
            features_dict[image_file] = features
            
            # Visualize features for a few sample images (every 20th image)
            if image_files.index(image_file) % 20 == 0:
                visualize_features(image_path, os.path.join(output_dir, "feature_visualization"))
                
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    
    # Save features to a pickle file
    with open(os.path.join(output_dir, "mountain_features.pkl"), "wb") as f:
        pickle.dump(features_dict, f)
    
    # Also save as CSV for easy inspection
    feature_df = pd.DataFrame.from_dict(features_dict, orient='index')
    feature_df.to_csv(os.path.join(output_dir, "mountain_features.csv"))
    
    print(f"Features extracted and saved to {os.path.join(output_dir, 'mountain_features.pkl')}")
    print(f"Features also saved as CSV to {os.path.join(output_dir, 'mountain_features.csv')}")
    
    # Upload to MongoDB if requested
    if upload_to_mongodb:
        upload_features_to_mongodb(features_dict, mongodb_uri)
    
    return features_dict

def upload_features_to_mongodb(features_dict, mongodb_uri=None):
    """Upload the extracted features to MongoDB."""
    # Use default connection string if none provided
    if mongodb_uri is None:
        mongodb_uri = DEFAULT_MONGODB_URI
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client["mountain_image_search"]
        collection = db["image_features"]
        
        print(f"Connected to MongoDB Atlas")
        
        # Prepare documents for bulk upload
        documents = []
        for image_name, features in features_dict.items():
            # Convert numpy arrays to lists for MongoDB storage
            if isinstance(features, np.ndarray):
                features_list = features.tolist()
            else:
                features_list = features
                
            doc = {
                "image_name": image_name,
                "features": features_list,
                "feature_count": len(features_list) if isinstance(features_list, list) else 0,
                "timestamp": datetime.now()
            }
            documents.append(doc)
        
        # First delete any existing documents with the same image names
        image_names = [doc["image_name"] for doc in documents]
        collection.delete_many({"image_name": {"$in": image_names}})
        
        # Insert all documents
        if documents:
            result = collection.insert_many(documents)
            print(f"Successfully uploaded {len(result.inserted_ids)} documents to MongoDB")
        else:
            print("No features to upload")
            
    except Exception as e:
        print(f"Error uploading to MongoDB: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract features from mountain images")
    parser.add_argument("--image_dir", default="../mountain_images", help="Directory containing the images")
    parser.add_argument("--output_dir", default="2", help="Directory to save the outputs")
    parser.add_argument("--mongodb_uri", default=DEFAULT_MONGODB_URI, help="MongoDB connection URI")
    parser.add_argument("--skip_mongodb", action="store_true", help="Skip uploading to MongoDB")
    
    args = parser.parse_args()
    
    features_dict = extract_features_from_directory(
        args.image_dir, 
        args.output_dir, 
        upload_to_mongodb=not args.skip_mongodb,
        mongodb_uri=args.mongodb_uri
    )
    
    print(f"Extracted features for {len(features_dict)} images") 