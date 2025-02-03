    
import requests
import zipfile
import io

def download_and_extract_zip():
    # URL of the zip file
    zip_url = "https://www.dropbox.com/scl/fo/fnxqx48me9ig8jmaoybiu/ABlA8GDE6wrS45I7w4q8t4c?rlkey=t0k1aixmwcke5zhi8ion7kgww&e=1&dl=1"  # Note: changed dl=0 to dl=1 for direct download
    
    try:
        # Send GET request to download the file
        response = requests.get(zip_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create a BytesIO object from the response content
        zip_data = io.BytesIO(response.content)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_data) as zip_ref:
            zip_ref.extractall("./downloaded_data")  # Extract to a directory named 'downloaded_data'
            
        print("Successfully downloaded and extracted the zip file.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_and_extract_zip()
