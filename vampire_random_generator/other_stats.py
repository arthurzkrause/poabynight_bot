
from vampire_random_generator.attributes import attributes_all
import random

blood_potency_choices = [1,2,3,4]
generation_choices = [16,15,14,13,12,11,10]
humanity_choices = [3,4,5,6,7,8,9,10]
clan_choices = ['Banu Haqim', 'Brujah', 'Gangrel', 'Caitiff', 'Hecata', 'Lasombra', 'Malkavian', 'The Ministry', 
                'Nosferatu', 'Ravnos', 'Salubri', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']

def stats_generator():
    result = "\nSTATS:\n"

    # HEALTH_TRACK
    health = attributes_all['Stamina'] + 3
    result += f'Health: {health}\n'

    # WILLPOWER
    willpower = attributes_all['Composure'] + attributes_all['Resolve']
    result += f'Willpower: {willpower}\n'

    # HUMANITY
    humanity = random.choice(humanity_choices)
    result += f"Humanity: {humanity}\n"

    # GENERATION + BLOODPOTENCY + CLAN
    generation = random.choice(generation_choices)
    blood_potency = random.choice(blood_potency_choices)
    clan = random.choice(clan_choices)

    if generation in [16, 15, 14]:
        blood_potency = 0
        result += (
            f"Blood Potency: Zero\n"
            f"Generation: {generation}\n"
            f"Clan: ThinBlood\n"
        )
    else:
        result += (
            f'Blood Potency: {blood_potency}\n'
            f'Generation: {generation}\n'
            f'Clan: {clan}\n'
        )

    return result