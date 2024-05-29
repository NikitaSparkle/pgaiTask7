import googlemaps
import json
import time


def get_restaurants(city):
    client = googlemaps.Client(key='Google Maps API Key')  # Removed for security reasons

    geocode = client.geocode(city)
    if not geocode:
        return "City not found."

    coordinates = geocode[0]['geometry']['location']

    places = client.places_nearby(location=coordinates, type='restaurant', radius=5000)
    restaurant_list = collect_places(places, client)

    while 'next_page_token' in places:
        time.sleep(2)
        places = client.places_nearby(page_token=places['next_page_token'])
        restaurant_list.extend(collect_places(places, client))

    top_restaurants = sorted(restaurant_list, key=lambda x: x.get('number_of_reviews', 0), reverse=True)[:30]

    return json.dumps(top_restaurants, ensure_ascii=False, indent=2)


def collect_places(places, client):
    restaurant_list = []
    for place in places['results']:
        restaurant = {
            'name': place['name'],
            'address': place.get('vicinity'),
            'number_of_reviews': place.get('user_ratings_total', 0)
        }
        restaurant_list.append(restaurant)
    return restaurant_list


city = input("Enter the name of the city: ")
result = get_restaurants(city)

print(result)

with open('restaurants.json', 'w', encoding='utf-8') as file:
    file.write(result)
