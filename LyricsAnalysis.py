from lyricsgenius import Genius
from pandas import DataFrame
from re import sub, escape
from string import punctuation

'''
The user gives two artist and it could chooses by manual albums from the selected artists.
Then it could selecting tracks.

After selecting the tracks we see how many times be the same words in both of them
'''


class SelectTrackLyrics:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.token = 'n6pObQoAE-FlcBm6eYdwjCscQ0wHMEhJbQ0szM8OfoNZqempOWhVKRLO3mPzqFh-'
        self.genius = Genius(self.token, remove_section_headers=True, skip_non_songs=True, verbose=False, timeout=10)

        self.artists = self.genius.search_artists(search_term=self.artist_name, per_page=50, page=1)  # search for the artist
        self.artists = self.artists['sections'][0]['hits']

    def search_artist(self):
        artists_df = DataFrame(columns=['Artist'])  # DataFrame for the Artists

        for index in range(len(self.artists)):
            artists_df.loc[len(artists_df['Artist'].index)] = self.artists[index]['result']['name']  # add all artist name to DataFrame

        artists_df.index += 1  # start DataFrame index

        print(artists_df)
        return artists_df

    def select_artist(self):
        artists_df = self.search_artist()
        artist_id = 0  # selected index of the artist from the DataFrame

        while artist_id == 0:
            selected_index_number = int(input("Choose artist by index number: "))
            if selected_index_number not in artists_df.index:
                print("Wrong ID number.")

            for index, artist in enumerate(self.artists, 1):
                if selected_index_number == index:
                    artist_id = artist['result']['id']

        return artist_id

    def search_albums(self):
        artist_albums = None

        while not artist_albums:
            artist_id = self.select_artist()
            artist = self.genius.artist_albums(artist_id)  # look for artist albums by id
            artist_albums = artist['albums']  # album names
            if not artist_albums:
                print(f"\n'{artist_albums}'... Empty albums list. :( \n")  # if artist haven't uploaded

        albums_df = DataFrame(columns=['Album_name'])  # Album names in DataFrame
        album_id_numbers_df = DataFrame(columns=['Album_id'])  # Album indexes in DataFrame

        for album in artist_albums:
            albums_df.loc[len(albums_df.index)] = album['name']  # add name of the album to DataFrame
            album_id_numbers_df.loc[len(album_id_numbers_df.index)] = album['id']  # add album id to DataFrame
            album_id_numbers_df['Album_id'] = album_id_numbers_df['Album_id'].astype('int32')

        albums_df.index += 1
        album_id_numbers_df.index += 1

        print(albums_df)
        return albums_df, album_id_numbers_df

    def select_album(self):
        albums_name, albums_ids = self.search_albums()
        album_id = 0

        while album_id == 0:
            album_title = int(input("Choose album by index number: "))
            if album_title not in albums_name.index:
                print("Wrong ID number.")
            else:
                album_id = albums_ids['Album_id'][album_title]

        return album_id

    def search_track(self):
        album_id = self.select_album()

        album_tracks = self.genius.album_tracks(album_id)  # look for album tracks by album id
        tracks = album_tracks['tracks']  # tracks of the album

        track_title_df = DataFrame(columns=['Track_name'])  # Tracks names in DataFrame
        song_url_df = DataFrame(columns=['Song_url'])  # Tracks url

        for index in range(len(tracks)):
            if not tracks[index]['song']['instrumental']:
                track_title_df.loc[len(track_title_df.index)] = tracks[index]['song']['title']  # add track name to df
                song_url_df.loc[len(song_url_df.index)] = tracks[index]['song']['url']  # add track url to df

        track_title_df.index += 1
        song_url_df.index += 1

        print(track_title_df)
        return track_title_df, song_url_df

    def selected_track(self):
        tracks_title, song_url = self.search_track()

        track_url = None  # selected url

        while not track_url:
            track_title = int(input("Choose track by index number: "))
            if track_title not in tracks_title.index:
                print("No lyrics found.")
            else:
                track_url = song_url['Song_url'][track_title]

        print(f'\n{track_url}')
        return track_url

    def selected_song_lyrics(self):

        track_url = self.selected_track()

        song_lyrics = self.genius.lyrics(song_url=track_url)  # look for lyrics by track url
        song_lyrics = song_lyrics.split("\n")[1:]  # remove song header
        song_lyrics = "\n".join(song_lyrics)

        chars = escape(punctuation)
        clear_lyrics = sub(r'[' + chars + ']', '', song_lyrics)  # lyrics without punctuation marks

        print(f'{clear_lyrics}\n')
        return clear_lyrics


class LyricsAnalysis:
    def __init__(self):
        self.artist_1 = SelectTrackLyrics("Eminem")
        self.artist_2 = SelectTrackLyrics("Led Zeppelin")

        self.song_lyrics_from_artist_1 = self.artist_1.selected_song_lyrics()
        self.song_lyrics_from_artist_2 = self.artist_2.selected_song_lyrics()

        self.lyrics_words_from_song_1 = self.song_lyrics_from_artist_1.split()  # split the two clear lyrics
        self.lyrics_words_from_song_2 = self.song_lyrics_from_artist_2.split()

        self.lyrics_words_from_song_1 = [words.lower() for words in self.lyrics_words_from_song_1]
        self.lyrics_words_from_song_2 = [words.lower() for words in self.lyrics_words_from_song_2]

        self.same_words_per_time_in_dict = {}
        self.get_same_word()

    def get_same_word(self):  # if the word is same in the second lyrics
        for word in self.lyrics_words_from_song_1:
            self.same_words_per_time_in_dict[word] = list(self.lyrics_words_from_song_2).count(word)

    def print_same_word(self):
        for key, value in self.same_words_per_time_in_dict.items():
            if value:
                print(f"The word '{key.capitalize()}' from the Song 1 appeared '{value}' times in the Song 2 lyrics"
                      )


if __name__ == "__main__":
    lyrics_analyzis = LyricsAnalysis()
    lyrics_analyzis.print_same_word()
