import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pickle
import os
import streamlit as st
from PIL import Image



# Configuration des identifiants Spotify
CLIENT_ID = os.getenv('client_id_spotify')
CLIENT_SECRET = os.getenv('client_secret_spotify')

# Initialize Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Initialise model & load in previously stored audio data
tracks_and_features_df = pd.read_csv('tracks_and_features.csv')
features_df = pd.read_csv('features.csv')
tracks_clustered_df = pd.read_csv('tracks_clustered_df.csv')

# Charger le modèle
with open('model_km100.pickle', 'rb') as model_file:
    model_km100 = pickle.load(model_file)

# Charger le scaler
with open('scaler.pickle', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# # Define the background image using CSS
# page_bg_img = '''
# <style>
# .stApp {
#     background-image:url("https://img.freepik.com/psd-gratuit/rendu-3d-du-fond-musical_23-2150810461.jpg?size=626&ext=jpg&ga=GA1.1.89547900.1718974890&semt=ais_user");
#     background-size: cover;
# }
# </style>
# '''

# # Apply the CSS
# st.markdown(page_bg_img, unsafe_allow_html=True)

image = Image.open('logo.png')
st.image(image)

st.markdown("<h1 style='text-align: center;font-size: 2.5em;'>Unlock the Soundtrack of Your Life with Gnoosic – Discover and Enjoy!</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='padding-top: 30px;'>Team: Louis, Adel, Camille</h2>", unsafe_allow_html=True)

# Étape 1: L'utilisateur fournit le titre de la chanson
track_name = st.text_input("Enter the name of a song: ")

def search_track(track_name, market='FR', limit=3):
    results = sp.search(q=f"track:{track_name}", limit=limit, market=market)
    return results

def display_search_results(tracks):
    if not tracks['tracks']['items']:
        st.write("No tracks found.")
        return None

    track_options = []
    for idx, track in enumerate(tracks['tracks']['items']):
        track_info = f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}"
        track_options.append(track_info)
        st.write(track_info)
    
    return track_options

if 'selected_track' not in st.session_state:
    st.session_state.selected_track = None

if track_name and st.session_state.selected_track is None:
    tracks = search_track(track_name)
    track_options = display_search_results(tracks)
         
    if track_options:
        selected_track_number = st.number_input("Enter the number of the track you want to select (1-3): ", max_value=3, step=1)
        if st.button('Confirm Track Selection'):
            st.session_state.selected_track = tracks['tracks']['items'][selected_track_number - 1]
            st.write(f"Track selected: {st.session_state.selected_track['name']} by {st.session_state.selected_track['artists'][0]['name']}")
            st.components.v1.iframe(f"https://open.spotify.com/embed/track/{st.session_state.selected_track['id']}?utm_source=generator",
                                width=320, height=80, scrolling=False)

if st.session_state.selected_track:
    # Étape 2: Traitement de la chanson sélectionnée
    def create_tracks_df(selected_track):
        artist_ids = [selected_track['artists'][0]['id']]
        artist_names = [selected_track['artists'][0]['name']]
        track_ids = [selected_track['id']]
        track_names = [selected_track['name']]
        album_release_dates = [selected_track['album']['release_date']]
        album_release_date_precisions = [selected_track['album']['release_date_precision']]
        is_explicits = [selected_track['explicit']]
        durations_ms = [selected_track['duration_ms']]
        popularity_scores = [selected_track['popularity']]

        audio_features = sp.audio_features([selected_track['id']])[0]
        audio_features_dict = {
            'danceability': [audio_features['danceability']],
            'energy': [audio_features['energy']],
            'key': [audio_features['key']],
            'loudness': [audio_features['loudness']],
            'mode': [audio_features['mode']],
            'speechiness': [audio_features['speechiness']],
            'acousticness': [audio_features['acousticness']],
            'instrumentalness': [audio_features['instrumentalness']],
            'liveness': [audio_features['liveness']],
            'valence': [audio_features['valence']],
            'tempo': [audio_features['tempo']],
            'duration_ms.1': [audio_features['duration_ms']],
            'time_signature': [audio_features['time_signature']],
            'track_href': [audio_features['track_href']]
        }

        tracks_id_df = pd.DataFrame({
            'artist_id': artist_ids,
            'artist_name': artist_names,
            'track_id': track_ids,
            'track_name': track_names,
            'album_release_date': album_release_dates,
            'album_release_date_precision': album_release_date_precisions,
            'is_explicit': is_explicits,
            'duration_ms': durations_ms,
            'popularity': popularity_scores
        })

        audio_features_df = pd.DataFrame(audio_features_dict)
        combined_df = pd.concat([tracks_id_df, audio_features_df], axis=1)
        combined_df['album_release_year'] = 0
        combined_df['album_release_decade'] = 0

        return combined_df

    song_df = create_tracks_df(st.session_state.selected_track)

    # audio_features_model_on = ['is_explicit', 'danceability', 'energy', 'key', 'loudness', 'mode',
    #                            'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    # song_df = song_df[audio_features_model_on]

    # scaled = scaler.transform(song_df)
    # cluster_song = model_km100.predict(scaled)[0]
    # st.write(f"Cluster of your song : {cluster_song}")

    # scaled_features = scaler.transform(tracks_and_features_df[audio_features_model_on])
    # tracks_and_features_df['cluster_km100'] = model_km100.predict(scaled_features)

    #same_cluster_songs = tracks_clustered_df[tracks_clustered_df['cluster_km100'] == cluster_song].sample(3)

    audio_features_model_on = ['is_explicit','popularity', 'danceability', 'energy', 'key','loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo', 'time_signature']

    audio_features_model_on_A = ['is_explicit','popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness']
    audio_features_model_on_B = [ 'acousticness', 'instrumentalness','liveness', 'tempo', 'time_signature']


    tracks_and_features_df = tracks_and_features_df[audio_features_model_on]
    song_df_to_cluster=song_df[audio_features_model_on]

    song_df_to_cluster_A=song_df[audio_features_model_on_A]
    song_df_to_cluster_B=song_df[audio_features_model_on_B]

    # Charger le scaler
    with open('scaler.pickle', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    with open('scaler_A.pickle', 'rb') as scaler_file:
        scalerA = pickle.load(scaler_file)

    with open('scaler_B.pickle', 'rb') as scaler_file:
        scalerB = pickle.load(scaler_file)

    # Charger le modèle
    with open('model_km100.pickle', 'rb') as model_file:
        model_km100 = pickle.load(model_file)
        model_km200_A=pickle.load(model_file)
        model_km200_B=pickle.load(model_file)


    scaled=scaler.transform(song_df_to_cluster)
    scaled_A=scalerA.transform(song_df_to_cluster_A)
    scaled_B=scalerB.transform(song_df_to_cluster_B)

    cluster_song = model_km100.predict(scaled)
    cluster_song_A=model_km200_A.predict(scaled_A)
    cluster_song_B=model_km200_B.predict(scaled_B)

    cluster_song_A=cluster_song_A[0]
    cluster_song_B=cluster_song_B[0]
   

    st.write(f"Cluster of your song: {cluster_song_A}, {cluster_song_B}")

    tracks_clustered_df=pd.read_csv("tracks_clustered_df.csv")
    same_cluster_songs_A = tracks_clustered_df[tracks_clustered_df['cluster_km200_A'] == cluster_song_A]
    same_cluster_songs_B = same_cluster_songs_A[same_cluster_songs_A['cluster_km200_B'] == cluster_song_B]
    same_cluster_songs=same_cluster_songs_B[same_cluster_songs_B["track_id"]!=song_df['track_id'][0]]
    same_cluster_songs=same_cluster_songs.sample(3)

    recommended_song_ids = same_cluster_songs['track_id'].tolist()
    print(f"Identifiants des chansons recommandées : {recommended_song_ids}")

    for track_id in recommended_song_ids:
        st.components.v1.iframe(f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator",
                                width=320, height=80, scrolling=False)

    

    # Feedback de l'utilisateur
    st.write("Are you satisfied of this recommandations ?")
    if st.button("YES"):
        st.write("Thank you")
        st.balloons()
    if st.button("NO"):
        #st.write("try again.")
        st.write("Ask to Louis, he pimps the model.")
