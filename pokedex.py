#gTTS es GoogleTexttoSpeech, para darle la funcionalidad de audio a la pokedex
from gtts import gTTS 
import os

import requests

# URL base de la PokeAPI
base_url = "https://pokeapi.co/api/v2/"

pokemon = input("Ingrese nro de pokemon o nombre en minuscula: ")
if isinstance(pokemon, str):
     pokemon
else:
    int(pokemon)

# Realiza una solicitud para obtener los datos de Bulbasaur
response = requests.get(base_url + "pokemon/" + pokemon)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    # Obtiene el nombre de Bulbasaur
    pokenombre = data["forms"][0]["name"]
    # Obtiene la URL de la cadena de evolución de Bulbasaur
    evolution_chain_url = data["species"]["url"]
    
   # Realiza una solicitud para obtener los datos de la cadena de evolución
    species_response = requests.get(evolution_chain_url)
    if species_response.status_code == 200:
        species_data = species_response.json()
    # Obtiene la URL de la cadena de evolución de Bulbasaur
        evolution_chain_url = species_data["evolution_chain"]["url"]
        
        # Realiza una solicitud para obtener los datos de la cadena de evolución
        evolution_chain_response = requests.get(evolution_chain_url)
        if evolution_chain_response.status_code == 200:
            evolution_chain_data = evolution_chain_response.json()
            # Imprime los datos de la cadena de evolución
            print("Evolución de", pokenombre + ":") 
            for chain in evolution_chain_data["chain"]["evolves_to"]:
                print(chain["species"]["name"])
        else:
            print("Error al obtener la cadena de evolución:", evolution_chain_response.status_code)
    else:
        print("Error al obtener los datos de la especie:", species_response.status_code)

    # Realiza una segunda solicitud para obtener los datos de las localizaciones de Bulbasaur
    locations_url = data["location_area_encounters"]
    locations_response = requests.get(locations_url)
    if locations_response.status_code == 200:
        locations_data = locations_response.json()
        # Imprime los nombres de las localizaciones de Bulbasaur
        print("\nLocalizaciones de", pokenombre + ":")
        for location in locations_data:
            print(location["location_area"]["name"])
    else:
        print("Error al obtener las localizaciones:", locations_response.status_code)
    
    # Obtiene la URL de la especie del Pokémon
    species_url = data["species"]["url"]
    species_response = requests.get(species_url)
    if species_response.status_code == 200:
        species_data = species_response.json()
        # Busca la descripción de Kanto en los datos de la especie
        for flavor_text_entry in species_data["flavor_text_entries"]:
            if flavor_text_entry["language"]["name"] == "es" and flavor_text_entry["version"]["name"] == "x":
                kanto_description = flavor_text_entry["flavor_text"]
                break
        # Imprime la descripción de Kanto
        print("\nDescripción de Kanto de", pokenombre + ":")
        print(kanto_description)

        #Ahora para el audio de la pokedex tengo que crear un archivo gTTS:
        tts = gTTS(text=kanto_description, lang="es")
        tts.save("descripcion.mp3")
        os.system("start descripcion.mp3")

    else:
        print("Error al obtener los datos de la especie:", species_response.status_code)

else:
    print("Error al obtener los datos de", pokemon, response.status_code)
