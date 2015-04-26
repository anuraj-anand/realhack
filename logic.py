from multiprocessing.dummy import Pool as ThreadPool
from random import uniform

from api import (
    DistanceMatrixAPI, GeocodeAPI,
    PlacesAPI, parse_coords,
)


thread_map = lambda *_args: ThreadPool(4).map(*_args)
final_map = lambda *_args: tuple(map(*_args))

type_name = lambda _s: '_'.join(map(
    lambda _p: _p.lower(), _s.split()
))

# backup values
random_rating = lambda: uniform(2.0, 4.0)
random_distance = lambda: uniform(400.0, 900.0)


def extract_score(info):
    total_rating = 0
    total_distance = 0
    for (rating, distance) in info:
        total_rating += rating
        total_distance += distance
    total_rating /= len(info)
    total_distance /= len(info)

    return total_rating, total_distance


def extract_rating(place):
    try:
        rating = float(place['rating'])
    except KeyError:
        rating = random_rating()
    return rating


def calculate_avg_rating(places):
    ratings = final_map(
        lambda _p: extract_rating(_p), places
    )
    try:
        avg_rating = sum(ratings) / len(ratings)
    except ZeroDivisionError:
        avg_rating = random_rating()
    return avg_rating


def extract_distance(distance_matrix):
    try:
        elements = distance_matrix[0]['elements']
        distances = final_map(
            lambda _e: int(_e['distance']['value']), elements
        )
        avg_distance = sum(distances) / len(distances)
    except IndexError:
        avg_distance = random_distance()
    return avg_distance


def calculate_avg_distance(locality, places):
    places_coords = final_map(parse_coords, places)
    distance_matrix = DistanceMatrixAPI.get_distance_matrix_between_multiple(
        (locality, ), places_coords
    )
    avg_distance = extract_distance(distance_matrix)
    return avg_distance


class Scorecard():
    @staticmethod
    def process_places(locality, places):
        avg_rating = calculate_avg_rating(places)
        avg_distance = calculate_avg_distance(locality, places)
        return avg_rating, avg_distance

    @classmethod
    def process_cuisine(cls, locality, cuisine):
        places = PlacesAPI.text_search(locality, 'food', cuisine)
        return cls.process_places(locality, places)

    @classmethod
    def process_art(cls, locality, art):
        places = PlacesAPI.nearby_search(locality, type_name(art))
        return cls.process_places(locality, places)

    @classmethod
    def process_spot(cls, locality, spot):
        places = PlacesAPI.nearby_search(locality, type_name(spot))
        return cls.process_places(locality, places)

    @classmethod
    def process_locality(cls, locality, user_prefs):
        cuisines = user_prefs['cuisines']
        cuisines_info = final_map(
            lambda _c: cls.process_cuisine(locality, _c), cuisines
        )
        cuisines_score = extract_score(cuisines_info)

        arts = user_prefs['arts']
        arts_info = final_map(
            lambda _a: cls.process_art(locality, _a), arts
        )
        arts_score = extract_score(arts_info)

        spots = user_prefs['spots']
        spots_info = final_map(
            lambda _s: cls.process_spot(locality, _s), spots
        )
        spots_score = extract_score(spots_info)

        return cuisines_score, arts_score, spots_score

    @classmethod
    def generate(cls, user_prefs):
        localities_names = user_prefs['localities']
        localities_coords = thread_map(
            GeocodeAPI.get_coords, localities_names
        )

        results = thread_map(
            lambda _locality: (_locality[0], cls.process_locality(_locality[1], user_prefs)),
            zip(localities_names, localities_coords)
        )

        scorecard = dict(results)

        return scorecard

    @classmethod
    def select_winner(cls, scorecard):
        total_ratings = {}
        total_distances = {}
        total = {}
        max_total = 0.0
        winner = ''
        for (locality, scores) in scorecard.items():
            total_ratings[locality] = 0.0
            total_distances[locality] = 0.0
            for (rating, distance) in scores:
                total_ratings[locality] += rating
                total_distances[locality] += distance
            total_ratings[locality] /= len(scores) * 5.0
            total_distances[locality] /= len(scores) * 1000.0
            total[locality] = total_ratings[locality] + total_distances[locality]
            if total[locality] > max_total:
                max_total = total[locality]
                winner = locality
            total_ratings[locality] = int(total_ratings[locality] * 100)
            total_distances[locality] = int(total_distances[locality] * 100)
        return winner, total_ratings, total_distances
