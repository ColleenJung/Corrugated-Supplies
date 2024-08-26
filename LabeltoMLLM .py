import logging
import openai
from azure.storage.blob import BlobServiceClient
from io import BytesIO



# Set up OpenAI API key directly (replace with your actual API key)
openai.api_key = "sk-NXXrVgV1TNS5EmCbfStzfzVXFEsfRUKE_Z3vztG1bVT3BlbkFJeC_h7hxVWwcGn872RNQz7e-EGYwuXeqLdpsabxVNIA"

# Set up connection to ADLS
account_name = "corrugatedsuppliesadls"  # Replace with your ADLS account name
account_key = "isSRTr7zr6nxWPkRXjL933X8bEjyOA/oKApVsWiQsZIemR6k3Cvo+w1uO0TGqaCyX9ZdHI9vku5Q+AStVj03Og=="    # Replace with your ADLS account key
container_name = "watchdog"

# Create a BlobServiceClient using a connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def extract_data_with_gpt4(image_data):
    """Use GPT-4 to extract and process data from image."""
    try:
        response = openai.Image.create(
            file=BytesIO(image_data),
            model="gpt-4o",  # Specify the model name here
            task="image-to-text"
        )
        
        # Assuming the response contains the extracted text
        text = response['choices'][0]['text']
        return text
    except Exception as e:
        logging.error(f"Error processing image with GPT-4: {e}")
        return ""

def process_image_from_adls(blob_name):
    """Process an image from the ADLS container."""
    try:
        # Get the blob client
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Download the blob data
        image_data = blob_client.download_blob().readall()

        # Process image using GPT-4
        text = extract_data_with_gpt4(image_data)

        if text:
            logging.info(f"Extracted Text: {text}")
            print(f"Extracted text: {text}")
        else:
            print("Failed to extract text.")
    
    except Exception as e:
        logging.error(f"Failed to process image: {e}")
        print(f"Error processing image: {str(e)}")

# Example usage
blob_name = "raw/labels/org-images/Busted/MB4E25071Z - Tag.jpg"  # Replace with the path to your image in the ADLS container
process_image_from_adls(blob_name)
