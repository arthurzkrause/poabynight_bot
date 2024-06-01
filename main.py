import random, copy
from typing import Final
from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokentoken.token_username import TOKEN,BOT_USERNAME
from vampire_random_generator.disciplines_functions import all_discipline
from vampire_random_generator.clans_text import clan_description
from vampire_random_generator.eater_eggs import easter_eggs_test, controle_updates, feedingComplications1, feedingComplications2

TOKEN
BOT_USERNAME

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello and welcome to the World of Darkness!\n- This is a bot from POA by Night, an encyclopedia project where you can find out more about the RPG world created for the Vampire the Masquerade system for Porto Alegre, Rio Grande do Sul, Brazil. For more information, visit our networks: https://linktr.ee/poabynight\n\n'
'What you can do:\n'
'- Play dice with the command /v5\n'
'- Make a random character with /character_generator.\n'
'- Get information about clans and disciplines by writing their names in the conversation.\n'
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'COMMANDS:\n'
        '- /v5 X Y (X = Total Dice Pool | Y = Total Hunger Dice)\n'
        '- /character_generator: Generates a random character with Skills, Attributes and Disciplines.\n'
        '- Get information about clans and disciplines! Just type their name in the conversation!\n'
        '- /updates show what and when something was introduced\n'
        '- /dice_rolls has some rolls that can help the storytelling\n'
        '- /predator_type_roll inform about the rouls to hunt.\n'
        '- /resonance to know more about the mechanic\n'
        '- /feeding_complications to know more about how can you mess the feeding\n'
        '- Try "social conflicts"'
	    '- You can type UPPER or lower case.\n\n'
         'Most of the content comes directly from the official Wiki!'
         'Do you want to send any update ideas?\n'
         'https://www.instagram.com/poabynight\n'
        )

async def character_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    import copy
    from vampire_random_generator.attributes import attributes_all, available_attributes_value, reset_attributes_values
    from vampire_random_generator.skills import skills_all, available_skill_value, reset_skill_values
    from vampire_random_generator.name_generator.surname import surname_list
    from vampire_random_generator.name_generator.own_name import name_list
    from vampire_random_generator.other_stats import stats_generator
    #OBS: Tentei fazer com que o bot fornecesse um personagem aleatório de um clã específico mudando só a variável "clan" ao ser digitado "/character_generator ventrue". Não consegui e deixo isso pro meu eu do futuro.

    # NAME GENERATOR
    def name_surname_age():
        age = random.randint(18, 60)

        name_generated = random.choice(name_list)

        first_surname_generated = random.choice(surname_list)
        second_surname_generated = random.choice(surname_list)

        return f"Name:\n{name_generated} {first_surname_generated} {second_surname_generated}\nAge: {age}\n"


    # ATTRIBUTES GENERATOR
    def attributes_generator():
        reset_attributes_values()
        result = "\nATTRIBUTES\n"
        for attribute in attributes_all:
            if available_attributes_value:
                assigned_value = random.choice(available_attributes_value)
                attributes_all[attribute] = assigned_value
                available_attributes_value.remove(assigned_value)
                result += f"{attribute}: {assigned_value}\n"
            else:
                result += f"{attribute}: No options available\n"

        return result

    # SKILLS GENERATOR - usa quase tudo que tá em vampir_random_generator.other_stats
    def skill_generator(category):
        reset_skill_values()
        result = f"\nSKILLS:\Type: {category}\n"
        values = available_skill_value.get(category, [])

        for atributo in skills_all:
            if values:
                assigned_value = random.choice(values)
                skills_all[atributo] = assigned_value
                values.remove(assigned_value)
                result += f"{atributo}: {assigned_value}\n"
            else:
                result += f"{atributo}: No options available\n"
        
        return result

    # Choose the desired category
    chosen_category = random.choice(list(available_skill_value.keys()))

    # RUN
    vampire_generated = f'{name_surname_age()}{attributes_generator()}{skill_generator(chosen_category)}{stats_generator()}'

    await update.message.reply_text(vampire_generated)

#DADOS
async def v5_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Divide o texto em partes usando espaços como delimitador
    args = text.split()

    # Verifica se há pelo menos dois argumentos
    if len(args) == 3 and args[1].isdigit() and args[2].isdigit():
        # Converte os argumentos para inteiros
        total_de_dados = int(args[1])
        dado_de_fome = int(args[2])

        # Verifica se os números são diferentes de zero -------------------------OK
        if total_de_dados > 20:
            await update.message.reply_text("Dice limit is 20 dice per roll.")
            return
        elif total_de_dados == 0 and dado_de_fome == 0:
            await update.message.reply_text("Why are you going to roll zero dice?")
            return
        elif total_de_dados == 0:
            await update.message.reply_text("What do you mean? The total number of dice is 0 and you still want to roll something?")
            return
        # Verifica se o dado de fome é zero ------------------------OK
        elif dado_de_fome == 0:
            # Se sim, rola o segundo número sem interferências
            result_dado_de_fome = 0
            result_total_de_dados = roll_dice(total_de_dados)
            sorted_total_de_dados = sort_dice_results(result_total_de_dados)
            ten_critic= double_ten_successes(sorted_total_de_dados)
            successes_dices = sum(1 for roll in result_total_de_dados if int(roll) >= 6)+ten_critic
            
            response_message = f"Dices: {', '.join(map(str, sorted_total_de_dados))}\nHunger Dices: 0\n{successes_dices} successes\n"
        # Verifica se o DADO DE FOME é maior que o TOTAL DE DADOS  ------------------- ok
        elif dado_de_fome >= total_de_dados:
            # Se sim, rola o segundo número sem interferências
            result_total_de_dados = 0
            result_dado_de_fome = roll_dice(total_de_dados)
            sorted_dados_de_fome = sort_dice_results(result_dado_de_fome)
            ten_critic = double_ten_successes(sorted_dados_de_fome)
            successes_dices = sum(1 for roll in result_dado_de_fome if int(roll) >= 6)+ten_critic
            bestial = check_for_double_ten(sorted_dados_de_fome)

            response_message = f"Dices: 0\nHunger Dices: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} successes\n{bestial}"
        else:
            # Se não, rola o primeiro número e pega os últimos num_dice2 resultados
            # TOTAL DE DADOS
            result_total_de_dados = roll_dice(total_de_dados)
            #COPIA total de dados e ORDENA para análise futura
            result_total_de_dados_copy = copy.deepcopy(result_total_de_dados)
            sorted_result_total_de_dados_copy = sorted(result_total_de_dados_copy, reverse=True)
            # DADOS DE FOME
            result_dado_de_fome = result_total_de_dados[-dado_de_fome:]
            sorted_dados_de_fome = sort_dice_results(result_dado_de_fome)
            # Atualiza a variável total_de_dados, removendo os dados de fome e ordena
            result_total_de_dados = result_total_de_dados[:-dado_de_fome]
            sorted_total_de_dados = sort_dice_results(result_total_de_dados)
            #Análise
            ten_critic = double_ten_successes(sorted_result_total_de_dados_copy)
            successes_dices = sum(1 for roll in sorted_result_total_de_dados_copy if int(roll) >= 6) + ten_critic
            
            # Verifica se há crítico bestial
            bestial = ""
            if 10 in sorted_total_de_dados and 10 in sorted_dados_de_fome:
                bestial = "Messy Critical!"
            elif 1 in sorted_total_de_dados and 1 in sorted_dados_de_fome:
                bestial = "Bestial Failure!"

            response_message = f"Dices: {', '.join(map(str, sorted_total_de_dados))}\nHunger Dices: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} successes\n{bestial}"

            
        await update.message.reply_text(response_message)

    else:
        # Mensagem de erro se os argumentos não forem válidos
        response_message = f"Do you want to roll the dice?\nPlay in the format '/v5 4 1'!\n\nIn the example:\n4 is the Total Dices\n1 is the Total Hunger Dices!\n\nThe result will appear as:\nTotal dice pool: result.\nHunger Dices: result."

        # Responde ao usuário com mensagem de erro
        await update.message.reply_text(response_message)

def double_ten_successes(how_many_tens):
    #confere dupla de 10 e soma no resultado, já que dois 10 são 4 pontos de sucesso.
    ten_successes = 0
    i = 0  # Inicializamos o índice fora do loop para evitar IndexError
    while i < len(how_many_tens) - 1:
        if int(how_many_tens[i]) == 10 and int(how_many_tens[i + 1]) == 10:
            ten_successes += 2
            i += 2  # Pular para a próxima possível dupla de 10
        else:
            i += 1  # Mover para o próximo elemento na lista
    return ten_successes

def check_for_double_ten(dados):
    #confere se há dois 10 ou 1 na rolagem e
    for i in range(len(dados) - 1):
        if int(dados[i]) == 10 and int(dados[i + 1]) == 10:
            return critico_falha_bestial(dados)
        elif int(dados[i]) == 1 and int(dados[i + 1]) == 1:
            return critico_falha_bestial(dados)
    return ''

def critico_falha_bestial(critic_list):
    #imprime mensagem de crítico
    if 10 in critic_list and 10 in critic_list:
        crit_message = "Messy Critical"
    elif 1 in critic_list and 1 in critic_list:
        crit_message = "Bestial Failure!\n"
    return crit_message
    
def roll_dice(num_dice):
    # Realiza a rolagem de dados de 10 lados
    results = [random.randint(1, 10) for _ in range(num_dice)]

    return results

def sort_dice_results(results_list):
    # Ordena a lista em ordem decrescente - Acho que isso não é necessário, mas é aquilo, já tá feito
    results_sorted = sorted(results_list, reverse=True)

    return results_sorted

async def clans_disciplines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Do you want to know more about the clans and their disciplines?\nJust type their name here in the chat and you will get some information!\n\nThe options are:\n- Banu Haqim\n- Brujah\n- Gangrel\n- Caitiff\n- Hecata\n- Lasombra\n- Malkavian\n- Ministry\n- Nosferatu\n- Ravnos\n- Salubri\n- Toreador\n- Tremere\n- Tzimisce\n- Ventrue\n- Mortals\n\nDisciplines:\n- Animalism\n- Auspex\n- Blood Sorcery\n- Blood Sorcery Rituals\n- Celerity\n- Dominate\n- Fortitude\n- Obfuscate\n- Oblivion\n- Oblivion Ceremonies\n- Potence\n- Presence\n- Protean\n- Thin Blood Alchemy'
)

#Updates - controle de atualizações - vampire_random_generator / easter_eggs
async def updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado_formatado = "\n".join(controle_updates) 
    await update.message.reply_text(resultado_formatado)

#Dice rolls, inform the Narrator about some mechanics
async def dice_rolls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Frenzy\nWillpower + (Humanity/3)(rounded down)\n\nAutomatic Wins\nPlayer's dice pool is double the challenge\n\nWinning at a cost\nRoll that includes successes, but fails. You may achieve your goal, but at some cost.\n\nTake Half\nDivide your total dice in half (round down). This will be your number of successes.\n\nMultiple opponents\nLose one die for each successive action in the same turn.\n\nExtended test\nCan be used between characters\nHigh difficulty test with cumulative rolls.\nE.g Getting your hands on a relic requires three wins for each task:\nInt + Larceny - overcome alarm \nDex + Stealth - Invade location through skylight\nComposure + Stealth - Extract relic from security laser\n\nSingle roll\nIf after 3 turns of combat and the question 'Will anything dramatically change with more interactions?' if not:\n- Difficulty 3 if the players won the last turn.\n- Difficulty 4 if they suffered the same as the npc\n- Difficulty 5 if the NPC won the last turn\n- Difficulty 6 if the players were lucky to be alive.\n\nManeuver\nThe character studies the opponent and moves to a place of advantage, or a critical point. Bonus of 1-3 dice.\n\nTotal Attack\n+1 damage, but cannot defend any attack. If it is a Ranged Weapon, discharge the weapon. (Even if the NPC has more successes, he will still take all the damage.)\n\nTotal Defense\nCharacter just wants to survive. Gains a bonus die on all defense rolls. If you are in good cover, if become immune to ranged attacks, as long as you are not flanked (maneuver). Can only perform minor actions.")

#Resonance, inform about the mecanic of resonances
async def resonance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choleric\nThe humor of passion and anger but also one of jealousy and violence. This Resonance can, but not exclusively, be found in vessels that have the will to fight back against whatever problems they face\n- Emotions: Angry, violent, bullying, passionate or envious.\n- Disciplines: Celerity and Potence.\n\nMelancholy\nThe humor of sadness and the downtrodden but also those who seek enlightenment. This Resonance can, but not exclusively, be found in vessels who have lost the will to fight or those who are seized by the gain of knowledge.\n- Emotions: Sad, scared, depressed, intellectual, or grounded.\n- Disciplines: Fortitude and Obfuscate.\n\nPhlegmatic\nThe humor of those who are calm and relaxed or those who are lost in their own reminiscing. This Resonance can, but not exclusively, be found in vessels who are at peace or can't find a reason to care at the moment.\n- Emotions: Lazy, apathetic, calm, controlling, and sentimental.\n- Disciplines: Auspex and Dominate.\n\nSanguine\nThe humor of sex and passion but also of happiness and liveliness. This Resonance can, but not exclusively, be found in vessels who have a sexual interest in the vampire or are simply enjoying life itself.\n- Emotions: Horny, happy, enthusiastic, addicted, active, and flighty.\n- Disciplines: Blood Sorcery and Presence.\n\n'Empty'\nThis Resonance represents those who lack general emotions.\n- Emotions: That of sociopaths or the emotionally detached.\n- Disciplines: Oblivion.\n\nAnimal Blood\nWhile not a Resonance, it does serve a purpose to vampires. Giving them access to the last two Disciplines of Animalism and Protean. The Storyteller is free to correlate animal blood to the main four Resonances, should they find it important to their chronicle.")

#predator_type_roll inform the rolls to hunt
async def predator_type_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Alleycat\n - Strength + Brawl is to take blood by force or threat. Wits + Streetwise can be used to find criminals as if a vigilante figure.\n\nBagger - Intelligence + Streetwise can be used to find, gain access and purchase the goods.\n\nBlood Leech\n - This Predator Type is suggested to not be abstracted down to a dice pool.\n\nCleaver\n - Manipulation + Subterfuge is used to condition the victims, socializing with them and feeding from them without the cover being blown.\n\nConsensualist\n - Manipulation + Persuasion allows the kindred to take blood by consent, under the guide of medical work or mutual kink.\n\nFarmer\n - Composure + Animal Ken is the roll to find and catch the chosen animal.\n\nOsiris\n - Manipulation + Subterfuge or Intimidation + Fame are both used to feed from the adoring fans.\n\nSandman\n - Dexterity + Stealth is for casing a location, breaking in and feeding without leaving a trace.\n\nScene Queen\n - Manipulation + Persuasion aids in feeding from those within the Kindred's subgroup, through conditioning and isolation to gain blood or gaslighting or forced silence.\n\nSiren\n - Charisma + Subterfuge is how sirens feed under the guise of sexual acts.\n\nExtortionist\n - Strength/Manipulation + Intimidation to feed through coercion.\n\nGraverobber\n - Resolve + Medicine for sifting through the dead for a body with blood. Manipulation + Insight for moving among miserable mortals.\n\nRoadside Killer\n - Dexterity/Charisma + Drive to feed by picking up down and outs with no other options.\n\nGrim Reaper\n - Intelligence + Awareness/Medicine in order to find victims.\n\nMontero\n - Intelligence + Stealth represents the expert planning of well-trained Retainers. Whereas a well-practiced plan and patient waiting is represented by Resolve + Stealth\n\nPursuer\n - Intelligence + Investigation to locate and find a victim no one will notice is gone. Stamina + Stealth for long stalking of unaware urban victims.\n\nTrapdoor\n - Charisma + Stealth for the victims that enter expecting a fun-filled night. Dexterity + Stealth to feed upon trespassers. Wits + Awareness + Haven dots is used to navigate the maze of the den itself.")

async def feeding_complications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado_formatado = "\n".join(feedingComplications1) 
    await update.message.reply_text(resultado_formatado)
    resultado_formatado = "\n".join(feedingComplications2) 
    await update.message.reply_text(resultado_formatado)

#Handle Responses - se o usuário digitar algo que não um comando,o bot devolve algo escrito
def handle_response(text: str) -> str:
    processed: str = text.lower()
    #EASTER EGG - vampire_random_generator / easter_eggs
    if processed in easter_eggs_test:
        return f'{easter_eggs_test[processed]}'
    
    #CLÃS - vampire_random_generator / Clans_text
    elif processed in clan_description:
        return f'{clan_description[processed]}'
    
    #DISCIPLINES - vampire_random_generator / disciplines_functions
    elif processed in all_discipline:
        processed_upper = processed.upper()
        return f'{processed_upper}:\n{all_discipline[processed]}'
    
    else:
        return "Type the name of the discipline or clan you are interested in! There are some other surprises out there, don't give up!"    
  
#Handling Messages - Diferencia se é grupo ou não.
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str=update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        response: str=handle_response(text)
    print('Bot', response)
    await update.message.reply_text(response)

#Errors - imprimir no terminal pra eu saber o que tá acontecendo
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}'),

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('v5',v5_command))
    app.add_handler(CommandHandler('character_generator',character_generator))
    app.add_handler(CommandHandler('clans_disciplines',clans_disciplines))
    app.add_handler(CommandHandler('updates',updates))
    app.add_handler(CommandHandler('dice_rolls',dice_rolls))
    app.add_handler(CommandHandler('resonance',resonance))
    app.add_handler(CommandHandler('predator_type_roll',predator_type_roll))
    app.add_handler(CommandHandler('feeding_complications',feeding_complications))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)