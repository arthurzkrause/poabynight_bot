import random
from typing import Final
from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokentoken.token_username import TOKEN,BOT_USERNAME
from vampire_random_generator.disciplines_functions import all_discipline
from vampire_random_generator.clans_text import clan_description
from vampire_random_generator.eater_eggs import easter_eggs_test

TOKEN
BOT_USERNAME

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Olá, bem vindo ao Mundo das Trevas!\n- Este é um bot do POA by Night, um projeto de enciclopédia onde você pode descobrir sobre o mundo de RPG criado para o sistema de Vampiro a Máscara especialmente para Porto Alegre, Rio Grande do Sul, Brasil. para mais informações, acesse nossas redes: https://linktr.ee/poabynight\n\n'
'Aqui você pode:\n'
'- Jogar dados com o comando /v5\n'
'- Fazer um personagem aleatório com /character_generator.\n'
'- Ter informações sobre os clãs e disciplinas ao escrever seus nomes na conversa\n'
'- Fica ligado pra mais novidades em breve'
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Versão 1.2.0\n'
        'COMANDOS:\n'
        '- /v5 X Y (X= dados normais | Y = dados de fome)\n'
        'Obs: Não use 0 nos dados.\nDupla de 10 não somam +2 no resultado, fiquem de olho nos seus críticos! \n'
        '- /character_generator: Gera um personagem aleatório com Skills, Attributes e Disciplinas\n'
        '- Tenha informações sobre os clãs e disciplinas! É só digitar o nome deles na conversa!\n'
        ' Quer saber se tem alguma novidade? Digita: log\n\n'
        'Quer mandar alguma ideia de update?\n'
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


    # NAME GENERATOR
    def name_surname_age():
        age = random.randint(18, 130)

        name_generated = random.choice(name_list)

        first_surname_generated = random.choice(surname_list)
        second_surname_generated = random.choice(surname_list)

        return f"Nome:\n{name_generated} {first_surname_generated} {second_surname_generated}\nIdade: {age}\n"


    # ATTRIBUTES
    def attributes_generator():
        reset_attributes_values()
        result = "\nATRIBUTOS\n"
        for attribute in attributes_all:
            if available_attributes_value:
                assigned_value = random.choice(available_attributes_value)
                attributes_all[attribute] = assigned_value
                available_attributes_value.remove(assigned_value)
                result += f"{attribute}: {assigned_value}\n"
            else:
                result += f"{attribute}: Sem opções disponíveis\n"

        return result

    # SKILLS
    def skill_generator(category):
        reset_skill_values()
        result = f"\nHABILIDADES:\nTipo: {category}\n"
        values = available_skill_value.get(category, [])

        for atributo in skills_all:
            if values:
                assigned_value = random.choice(values)
                skills_all[atributo] = assigned_value
                values.remove(assigned_value)
                result += f"{atributo}: {assigned_value}\n"
            else:
                result += f"{atributo}: Sem opções disponíveis\n"
        
        return result

    # Choose the desired category
    chosen_category = random.choice(list(available_skill_value.keys()))

    # RUN
    vampire_generated = f'{name_surname_age()}{attributes_generator()}{skill_generator(chosen_category)}{stats_generator()}'

    await update.message.reply_text(vampire_generated)

#/v5
async def v5_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtém o texto da mensagem
    text = update.message.text

    # Divide o texto em partes usando espaços como delimitador
    args = text.split()

    # Verifica se há pelo menos dois argumentos
    if len(args) == 3 and args[1].isdigit() and args[2].isdigit():
        # Converte os argumentos para inteiros
        num_dice1 = int(args[1])
        num_dice2 = int(args[2])

        # Verifica se os números são diferentes de zero
        if num_dice1 == 0 and num_dice2 == 0:
            await update.message.reply_text("Vai rolar zero dados pra que?")
            return
        elif num_dice1 == 0 or num_dice2 == 0:
            await update.message.reply_text("Não consigo rolar zero 😞. Coloca 1 no dado de fome e ignora ele!")
            return

        # Realiza as rolagens de dados
        result1 = roll_dice(num_dice1)
        result2 = roll_dice(num_dice2)

        # Ordena os resultados em ordem decrescente
        result1_sorted = sort_dice_results(result1)
        result2_sorted = sort_dice_results(result2)

        # Verifica se há crítico bestial
        crit_message = ""
        if 10 in result1 and 10 in result2:
            crit_message = "Crítico bestial!\nNão esquece de dobrar os 10 e adicionar aos sucessos!"
        elif 1 in result1 and 1 in result2:
            crit_message = "Fracasso bestial!\nConfere com o narrador a dificuldade da rolagem!"

        # Conta os sucessos para cada rolagem
        successes_1 = sum(1 for roll in result1_sorted if int(roll) >= 6)
        successes_2 = sum(1 for roll in result2_sorted if int(roll) >= 6)

        # Calcula o total de sucessos
        total_successes = successes_1 + successes_2

        successes = f'{total_successes} sucessos'

        # Cria uma mensagem de resposta
        response_message = f"Dados: {', '.join(map(str, result1_sorted))}\nDados de fome: {', '.join(map(str, result2_sorted))}\n{successes}\n{crit_message}"
        # Responde ao usuário
        await update.message.reply_text(response_message)

    else:
        # Mensagem de erro se os argumentos não forem válidos
        response_message = f"Quer usar os dados? Usa na forma '/v5 4 1'!\nPrimeiro os dados normais e depois os dados de fome!\nCuidado com dupla de 10, eles não são dobrados!"

        # Responde ao usuário com mensagem de erro
        await update.message.reply_text(response_message)


def roll_dice(num_dice: int) -> List[int]:
    # Realiza a rolagem de dados de 10 lados
    results = [random.randint(1, 10) for _ in range(num_dice)]

    return results

def sort_dice_results(results_list: List[int]) -> List[int]:
    # Ordena a lista em ordem decrescente
    results_sorted = sorted(results_list, reverse=True)

    return results_sorted

async def clans_and_disciplines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Quer saber mais sobre os clãs e as suas disciplinas?\nÉ só digitar o nome deles \
aqui no chat que você vai ter algumas informações sobre eles! \
Não precisa digitar o /clan\n\n'
'As opções são:\nBanu Haqim, Brujah, Gangrel, Caitiff, Hecata, Lasombra, Malkavian, Ministério, \
Nosferatu, Ravnos, Salubri, Toreador, Tremere, Tzimisce, Ventrue, Humanos e Ghouls\
\nVocê também pode conferir informações sobre as disciplinas! Coloca o nome delas em inglês e vai surgir um texto explicando ela.\nNão, não tá traduzido.'
)

#Handle Responses

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
        return f'{processed}:\n{all_discipline[processed]}'
    else:
        return "Digita o nome da disciplina ou do clã que você tem interesse! Tem algumas outras surpresas por aí, não desiste!"    
  
#Handling Messages
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

#Errors
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
    app.add_handler(CommandHandler('clans',clans_and_disciplines))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)