from flask import Flask, request, jsonify
import pandas as pd
from pyngrok import ngrok

# Initialize Flask app
app = Flask(__name__)

# Load the scraped data from the CSV file
try:
    scraped_data = pd.read_csv('scraped_medium_articles.csv')
    print("CSV file loaded successfully.")
    
    # Drop rows with missing titles
    scraped_data = scraped_data.dropna(subset=['Title'])
    print("Rows with missing titles dropped.")
    
    # Debug: Print the first few rows of the CSV
    print("Sample data from CSV:")
    print(scraped_data.head())
except Exception as e:
    print(f"Error loading CSV file: {e}")
    scraped_data = pd.DataFrame()  # Fallback to an empty DataFrame

# Root route
@app.route('/')
def home():
    return "Flask app is running. Use the /search endpoint to search for articles."

# Search route
@app.route('/search', methods=['GET'])
def search():
    try:
        # Get the keyword from the query parameters
        keyword = request.args.get('keyword', '').lower()
        print(f"Received keyword: {keyword}")
        
        # Debug: Print the first few titles
        print("Sample titles in CSV:")
        print(scraped_data['Title'].head())
        
        # Filter the DataFrame based on the keyword in the titles
        results = scraped_data[scraped_data['Title'].str.lower().str.contains(keyword, na=False)]
        print(f"Found {len(results)} matching results.")
        
        # Debug: Print the matching results
        print("Matching results:")
        print(results)
        
        # Convert the results to a list of dictionaries
        results_json = results.to_dict(orient='records')
        
        # Return the results as JSON
        return jsonify(results_json)
    except Exception as e:
        print(f"Error in /search endpoint: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# Run the Flask app
if __name__ == '__main__':
    # Set your ngrok authtoken
    ngrok.set_auth_token("2tldkQUiOO8nR7ZVy7JBMuDpMRt_4cExE55ssWK6bfTNC1Rmj")  # Replace with your actual authtoken
    
    # Start ngrok tunnel
    public_url = ngrok.connect(5000).public_url
    print(f" * Running Flask app on Colab. Public URL: {public_url}")
    
    # Run the Flask app
    app.run()
    # https://<ngrok-url>.ngrok-free.app/search?keyword=technology