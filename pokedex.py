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
    pokenombre = pokenombre.capitalize()
    print("Has seleccionado a", pokenombre) #el pokemon ["genera"]["genus"] where ["language"]["name"] == "es"
    # Obtiene la URL de la cadena de evolución del pokemon
    evolution_chain_url = data["species"]["url"]
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
   # Realiza una solicitud para obtener los datos de la cadena de evolución
    species_response = requests.get(evolution_chain_url) #le pegamos a la url de la especie
    if species_response.status_code == 200:
        species_data = species_response.json() #convertimos la response a json para recorrerla
    # Obtiene la URL de la cadena de evolución de Bulbasaur
        evolution_chain_url = species_data["evolution_chain"]["url"] #le pegamos a la url de la evolucion
        
        # Realiza una solicitud para obtener los datos de la cadena de evolución
        evolution_chain_response = requests.get(evolution_chain_url)
        if evolution_chain_response.status_code == 200:
            evolution_chain_data = evolution_chain_response.json() #convertimos la response a json para recorrerla

            def find_evolutions(pokemon_data, target_name, evolutions=[]):
            # Verificar si el nombre del pokemon actual coincide con el objetivo
                if pokemon_data.get("species", {}).get("name") == target_name:
                    # Recorrer las evoluciones y agregar los nombres a la lista
                    for evolution in pokemon_data.get("evolves_to", []):
                        evolutions.append(evolution.get("species", {}).get("name"))
                else:
                    # Si no coincide, seguir buscando en las evoluciones
                    for evolution in pokemon_data.get("evolves_to", []):
                        find_evolutions(evolution, target_name, evolutions)
                return evolutions
            
            pokenombre = pokenombre.lower()
            evolutions = find_evolutions(evolution_chain_data["chain"], pokenombre)

            # Imprimir las evoluciones encontradas
            pokenombre = pokenombre.capitalize()
            print("Evolucion de", pokenombre + ":")
            for evolution in evolutions:
                print(evolution.capitalize())
        else:
            print("Error al obtener la cadena de evolución:", evolution_chain_response.status_code)
    else:
        print("Error al obtener los datos de la especie:", species_response.status_code)

    # Realiza una segunda solicitud para obtener los datos de las localizaciones del pokemon
    locations_url = data["location_area_encounters"]
    locations_response = requests.get(locations_url)
    if locations_response.status_code == 200:
        locations_data = locations_response.json()
        # Imprime los nombres de las localizaciones del pokemon
        print("\nLocalizaciones de", pokenombre + ":")
        if len(locations_data) > 0:
            for location in locations_data:
                print(location["location_area"]["name"])
        else:
            print("Ruta desconocida. Este pokemon es muy raro de encontrar en estado salvaje. ")

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
