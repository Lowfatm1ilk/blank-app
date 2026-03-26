import streamlit as st
from openai import OpenAI
import json
client = OpenAI(api_key=st.secrets['json'] )

if 'pokedex' not in st.session_state:
    st.session_state['pokedex'] = []

def print_pokemon(d):
    for k in d.keys():
        if type(d[k])==dict:
            for k1 in d[k].keys():
                st.write("   " +k1 + ': ' + str(d[k][k1]))
        elif type(d[k])==list:
            for l in d[k]:
                st.write(l)
        else:
            st.write(k + ": "+ str(d[k]))
jason = """{
  "name": "Pikachu",
  "entry_number": "0025",
  "stats": {
    "hp": 8,
    "attack": 9,
    "defense": 6,
    "special_attack": 9,
    "special_defense": 7,
    "speed": 14
  },
  "description": "When several of these Pokémon gather, their electricity can build and cause lightning storms. It stores electric energy in its cheeks and releases it in powerful bursts.",
  "details": {
    "height": "1 ft 4 in",
    "weight": "13.2 lbs",
    "gender": "Male or Female",
    "category": "Mouse Pokémon",
    "abilities": [
      "Static",
      "Lightning Rod"
    ]
  },
  "type": [
    "Electric"
  ],
  "weak_to": [
    "Ground"
  ],
  "evolves_into": "Raichu"
} 
"""

system_prompt = "You make pokedex entries but make sure to double check your info from trusted pokemon sources with the following json format:" + jason

with st.form('form'):
    ans1 = st.text_input("Would you like to (1) view generated entries of pokedex or (2) add new entries to pokedex ")

    submit = st.form_submit_button('Submit')
    if submit:
        if ans1.strip()=="1":
            if(len(st.session_state['pokedex'])>0):
                pokemon = st.text_input("What pokemon would you like to see in the pokedex ")

                button = st.button('See entry')
                if button:
                    for i in range(len(st.session_state['pokedex'])):
                        if st.session_state['pokedex'][i]["name"].lower()==pokemon.lower():
                            print_pokemon(st.session_state['pokedex'][i])


        elif ans1.strip()=="2":
            
            user_prompt = input("Tell me a pokemon.")

            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type":"json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            new_pokemon = json.loads(response.choices[0].message.content)
            print_pokemon(new_pokemon)
            st.session_state['pokedex'].append(new_pokemon)