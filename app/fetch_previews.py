"""
fetch_previews.py

Fetches real 30-second preview clips for each song from Apple's public
iTunes Search API (free, no API key required, legal for preview/demo use)
and writes an updated seed_songs.py with real audio_url values.

Run this ONCE from the app folder:
    python fetch_previews.py

It will overwrite seed_songs.py with real iTunes preview URLs where found,
and fall back to the SoundHelix sample for any song it can't find.
"""

import requests
import time
from seed_songs import TAMIL_SONGS, OTHER_LANGUAGE_SONGS, AUDIO_SAMPLES

FALLBACK_SAMPLES = AUDIO_SAMPLES


def search_itunes_preview(title, artist):
    try:
        query = f"{title} {artist}"
        resp = requests.get(
            "https://itunes.apple.com/search",
            params={"term": query, "media": "music", "limit": 1, "country": "IN"},
            timeout=8,
        )
        data = resp.json()
        if data.get("resultCount", 0) > 0:
            return data["results"][0].get("previewUrl")
    except Exception as e:
        print(f"  ! error searching '{title}': {e}")
    return None


def build_updated_list(song_list, label):
    updated = []
    for i, (title, artist, genre, duration) in enumerate(song_list):
        preview = search_itunes_preview(title, artist)
        if preview:
            print(f"[{label}] FOUND  : {title} - {artist}")
            audio = preview
        else:
            print(f"[{label}] FALLBACK: {title} - {artist}")
            audio = FALLBACK_SAMPLES[i % len(FALLBACK_SAMPLES)]
        updated.append((title, artist, genre, duration, audio))
        time.sleep(0.3)
    return updated


def write_seed_file(tamil_updated, other_updated):
    with open("seed_songs.py", "w", encoding="utf-8") as f:
        f.write('AUDIO_SAMPLES = [\n')
        for url in FALLBACK_SAMPLES:
            f.write(f'    "{url}",\n')
        f.write(']\n\n')

        f.write("SONGS_WITH_AUDIO = [\n")
        for title, artist, genre, duration, audio in tamil_updated + other_updated:
            safe_title = title.replace('"', "'")
            safe_artist = artist.replace('"', "'")
            f.write(
                f'    ("{safe_title}", "{safe_artist}", "{genre}", {duration}, "{audio}"),\n'
            )
        f.write("]\n\n")

        f.write(
            "def build_song_objects():\n"
            "    songs = []\n"
            "    for title, artist, genre, duration, audio_url in SONGS_WITH_AUDIO:\n"
            "        songs.append({\n"
            '            "title": title,\n'
            '            "artist": artist,\n'
            '            "genre": genre,\n'
            '            "duration": duration,\n'
            '            "audio_url": audio_url,\n'
            "        })\n"
            "    return songs\n"
        )


if __name__ == "__main__":
    print("Fetching real iTunes previews for Tamil songs...")
    tamil_updated = build_updated_list(TAMIL_SONGS, "TA")

    print("\nFetching real iTunes previews for other language songs...")
    other_updated = build_updated_list(OTHER_LANGUAGE_SONGS, "OTHER")

    write_seed_file(tamil_updated, other_updated)
    print("\nDone. seed_songs.py updated with real preview URLs where available.")