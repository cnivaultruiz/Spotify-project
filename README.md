
link to our google presentation :
https://docs.google.com/presentation/d/1b4UTL-Qo6fKK3WJ9xCIEdcNjn-4G5WK1r7RqxoAM-9o/edit#slide=id.g2e75e2bd5d3_0_130

# Gnoosic: Unlock the Soundtrack of Your Life

## Overview
Gnoosic is a music recommendation application designed to help users discover new songs based on their current favorites. By leveraging Spotify's API and advanced machine learning techniques, Gnoosic provides personalized recommendations tailored to your musical tastes.

## Team
- Louis
- Adel
- Camille

## Features
- **Search and Select**: Enter the name of a song to search and select from a list of potential matches.
- **Song Analysis**: The selected song is analyzed for various audio features using Spotify's audio analysis tools.
- **Personalized Recommendations**: Receive song recommendations based on the audio characteristics of your chosen song.
- **User Feedback**: Provide feedback on the recommendations to refine future suggestions.

## Technical Details
- **Spotify API**: Used for searching songs and retrieving audio features.
- **Machine Learning**: Clustering model (KMeans) used to group songs with similar audio features.
- **Streamlit**: Interactive web application framework for the user interface.
- **Data Processing**: Pandas and Scikit-learn for data manipulation and machine learning.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/gnoosic.git
    cd gnoosic
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up Spotify API credentials:
    - Create a `.env` file in the project root.
    - Add your Spotify client ID and secret:
      ```env
      client_id_spotify=your_client_id
      client_secret_spotify=your_client_secret
      ```

## Usage
1. Run the application:
    ```bash
    streamlit run app.py
    ```
2. Open your web browser and navigate to the provided URL.
3. Enter the name of a song to get started.
4. Follow the prompts to select a song, receive recommendations, and provide feedback.

## Contributing
We welcome contributions! Please fork the repository and submit pull requests for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Spotify for providing the API and music data.
- Streamlit for the powerful and easy-to-use web application framework.

Enjoy discovering new music with Gnoosic!