import random

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []

    def add_track(self, name, artist, duration):
        """Добавляет трек в список."""
        self.tracks.append({
            'name': name,
            'artist': artist,
            'duration': duration
        })

    def remove_track(self, name):
        """Удаляет трек по названию."""
        self.tracks = [t for t in self.tracks if t['name'] != name]

    def total_duration(self):
        """Возвращает общую длительность всех треков."""
        return sum(t['duration'] for t in self.tracks)

    def find_by_artist(self, artist):
        """Находит все треки конкретного исполнителя."""
        return [t for t in self.tracks if t['artist'] == artist]

    def longest_track(self):
        """Находит самый длинный трек."""
        return max(self.tracks, key=lambda x: x['duration']) if self.tracks else None

    def shortest_track(self):
        """Находит самый короткий трек."""
        return min(self.tracks, key=lambda x: x['duration']) if self.tracks else None

    def shuffle(self):
        """Перемешивает треки в случайном порядке."""
        random.shuffle(self.tracks)

    def sort_by_duration(self, reverse=False):
        """Сортирует треки по длительности."""
        self.tracks.sort(key=lambda x: x['duration'], reverse=reverse)

my_playlist = Playlist("Избранное")

my_playlist.add_track("In the End", "Linkin Park", 216)
my_playlist.add_track("Starboy", "The Weeknd", 230)
my_playlist.add_track("Believer", "Imagine Dragons", 204)

print(f"Общая длительность: {my_playlist.total_duration()} сек.")

longest = my_playlist.longest_track()
print(f"Самый длинный трек: {longest['name']} ({longest['duration']} сек.)")

my_playlist.sort_by_duration()
print("Треки после сортировки:")
for track in my_playlist.tracks:
    print(f"- {track['name']} ({track['duration']} сек.)")

my_playlist.remove_track("Believer")

