
from vampire_random_generator.attributes import attributes_all
from vampire_random_generator.disciplines import *
import random

blood_potency_choices = [1,2,3,4]
generation_choices = [16,15,14,13,12,11,10]
humanity_choices = [3,4,5,6,7,8,9,10]
clan_choices = ['Banu Haqim', 'Brujah', 'Gangrel', 'Caitiff', 'Hecata', 'Lasombra', 'Malkavian', 'The Ministry', 
                'Nosferatu', 'Ravnos', 'Salubri', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']
disciplines_clan_list = []


def initialize_disciplines_clan_list(clan):
    global disciplines_clan_list
    if "Banu Haqim" in clan:
        disciplines_clan_list = [blood_sorcery, celerity, obfuscate]
    elif "Brujah" in clan:
        disciplines_clan_list = [celerity, potence, presence]
    elif "Caitiff" in clan:
        disciplines_clan_list = [blood_sorcery, celerity, obfuscate, potence, presence, animalism, 
                                 fortitude, protean, auspex, oblivion_hecata, oblivion_lasombra, dominate]
    elif "Gangrel" in clan:
        disciplines_clan_list = [animalism, fortitude, protean]
    elif "Hecata" in clan:
        disciplines_clan_list = [auspex, fortitude, oblivion_hecata]
    elif "Lasombra" in clan:
        disciplines_clan_list = [dominate, oblivion_lasombra, potence]
    elif "Malkavian" in clan:
        disciplines_clan_list = [auspex, dominate, obfuscate_malkavian]
    elif "The Ministry" in clan:
        disciplines_clan_list = [protean, obfuscate_nosferatu, presence]
    elif "Nosferatu" in clan:
        disciplines_clan_list = [animalism, obfuscate_nosferatu, potence]
    elif "Ravnos" in clan:
        disciplines_clan_list = [animalism, obfuscate_ravnos, presence]
    elif "Salubri" in clan:
        disciplines_clan_list = [auspex, dominate, fortitude]
    elif "Toreador" in clan:
        disciplines_clan_list = [auspex, celerity, presence]
    elif "Tremere" in clan:
        disciplines_clan_list = [auspex, dominate, blood_sorcery]
    elif "Tzimisce" in clan:
        disciplines_clan_list = [animalism, protean_tzimisce, dominate]
    elif "Ventrue" in clan:
        disciplines_clan_list = [dominate, fortitude, presence]
    elif "Sangue Fraco" in clan:
        disciplines_clan_list = [thin_blood_alchemy_1, thin_blood_alchemy_2]   

def disciplines_generator():
    disciplines_result = ''
# Escolher aleatoriamente 2 disciplinas
    chosen_disciplines_1 = random.choice(disciplines_clan_list)
    chosen_disciplines_2 = random.choice(disciplines_clan_list)

    # Verificar se as disciplinas escolhidas são iguais
    while chosen_disciplines_1 == chosen_disciplines_2:
        # Refazer a escolha para chosen_disciplines_2
        chosen_disciplines_2 = random.choice(disciplines_clan_list)

    # Determinar o nível de cada disciplina
    levels_chosen_disciplines_1 = [1, 2]
    levels_chosen_disciplines_2 = [1]

    # Atribuir habilidades com base nos níveis
    abilities_chosen_disciplines_1 = [random.choice(chosen_disciplines_1[level - 0]) for level in levels_chosen_disciplines_1]
    abilities_chosen_disciplines_2 = [random.choice(chosen_disciplines_2[1]) for _ in range(len(levels_chosen_disciplines_2))]
    discipline_name_1 = chosen_disciplines_1[0][0]
    discipline_name_2 = chosen_disciplines_2[0][0]
    disciplines_result += (
        #print("Chosen Discipline 1:", chosen_disciplines_1)
        f"{discipline_name_1}: Level 1: {abilities_chosen_disciplines_1[0]}\n"
        f"{discipline_name_1}: Level 2: {abilities_chosen_disciplines_1[1]}\n"

    # print("Chosen Discipline 2:", chosen_disciplines_2)
        f"{discipline_name_2}: Level 1: {abilities_chosen_disciplines_2[0]}\n"
        ) 
    return disciplines_result

def stats_generator():
    global clan
    result = "\nSTATS:\n"

    # HEALTH_TRACK
    health = attributes_all['Stamina'] + 3
    result += f'Vida: {health}\n'

    # WILLPOWER
    willpower = attributes_all['Composure'] + attributes_all['Resolve']
    result += f'Willpower: {willpower}\n'

    # HUMANITY
    humanity = random.choice(humanity_choices)
    result += f"Humanidade: {humanity}\n"

    #GENERATION + BLOODPOTENCY + CLAN
    generation = random.choice(generation_choices)
    blood_potency = random.choice(blood_potency_choices)
    clan = random.choice(clan_choices)
    if generation in [16,15,14]:
       blood_potency = 0
       clan = 'Sangue Fraco'
       result += (
            f"Potência de Sangue: Zero\n"
            f"Geração: {generation}\n"
            f'Clã: {clan}\n'
            )
    else:
        result += (
            f'Potência de Sangue: {blood_potency}\n'
            f'Geração: {generation}\n'
            f'Clã: {clan}\n'
        )

    # Verifica o clã
    if 'Banu Haqim'or 'Brujah'or 'Gangrel'or 'Caitiff'or 'Hecata'or 'Lasombra'or 'Malkavian'or 'The Ministry'or 'Nosferatu'or 'Ravnos'or 'Salubri'or 'Toreador'or 'Tremere'or 'Tzimisce'or 'Ventrue' in clan:
        initialize_disciplines_clan_list(clan)
        result += f'\nDisciplines:\n{disciplines_generator()}'


    return result