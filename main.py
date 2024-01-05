import random
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from token_username import TOKEN,BOT_USERNAME

TOKEN
BOT_USERNAME

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá, bem vindo ao Mundo das Trevas. Este é um bot do POA by Night, para mais informações, acesse \
nossas redes: https://linktr.ee/poabynight')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Versão 0.0.2\n'
        'Commands:\n'
        '/v5 X Y (X= dados normais | Y = dados de fome)\n'
        'Obs: Não dá pra usar 0 nos dados, já to de olho nesse bug. Dupla de 10 também não somam 2, fiquem de olho nos seus críticos! \n',
        'Character Generator\n'
        'Gera um personagem aleatório'
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

        first_name = [name.strip() for name in name_list[0].split("\n") if name.strip()]
        name_generated = random.choice(first_name)

        surnames = [surname.strip() for surname in surname_list[0].split("\n") if surname.strip()]
        first_surname_generated = random.choice(surnames)
        second_surname_generated = random.choice(surnames)

        return f"Nome:{name_generated} {first_surname_generated} {second_surname_generated}\nAge: {age}\n"

    # ATTRIBUTES
    def attributes_generator():
        reset_attributes_values()
        result = "ATTRIBUTES\n"
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
        result = f"\nSKILLS:\nSkills type: {category}\n"
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

        # Realiza as rolagens de dados
        result1 = roll_dice(num_dice1)
        result2 = roll_dice(num_dice2)

        # Ordena os resultados em ordem decrescente
        result1_sorted = sort_dice_results(result1)
        result2_sorted = sort_dice_results(result2)

        # Verifica se há crítico bestial
        crit_message = ""
        if "10" in result1.split(', ') and "10" in result2.split(', '):
            crit_message = "Crítico bestial!"
        elif "1" in result1.split(', ') and "1" in result2.split(', '):
            crit_message = "Fracasso bestial!"

        # Transforma as strings em listas de inteiros
        result1_list = list(map(int, result1.split(', ')))
        result2_list = list(map(int, result2.split(', ')))

        # Conta os sucessos para cada rolagem
        successes_1 = sum(1 for roll in result1_list if int(roll) >= 6)
        successes_2 = sum(1 for roll in result2_list if int(roll) >= 6)

        # Calcula o total de sucessos
        total_successes = successes_1 + successes_2

        successes = f'{total_successes} successes'

        # Cria uma mensagem de resposta
        response_message = f"Dados: {result1_sorted}\nDados de fome: {result2_sorted}\n{crit_message}\n{successes}"
        # Responde ao usuário
        await update.message.reply_text(response_message)

    else:
        # Mensagem de erro se os argumentos não forem válidos
        response_message = "Formato inválido. Use '/v5 3 1', primeiro número para dados normais e segundo para dados de fome!"

        # Responde ao usuário com mensagem de erro
        await update.message.reply_text(response_message)

def roll_dice(num_dice: int) -> str:
    # Realiza a rolagem de dados de 10 lados
    results = [random.randint(1, 10) for _ in range(num_dice)]

    # Formata os resultados como uma string
    result_str = ", ".join(map(str, results))

    return result_str

def sort_dice_results(results_str: str) -> str:
    # Converte a string de resultados em uma lista de inteiros
    results_list = list(map(int, results_str.split(", ")))

    # Ordena a lista em ordem decrescente
    results_sorted = sorted(results_list, reverse=True)

    # Formata os resultados ordenados como uma string
    result_str_sorted = ", ".join(map(str, results_sorted))

    return result_str_sorted

#Handle Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'vampiro' in processed:
        return 'Nós não usamos a palavra "Vampiro"! O que você é, um animal? Não, você é um Kindred, um Membro. Modere o linguajar!'

    if 'camarilla' in processed:
        return 'Camarilla? O que você sabe sobre a Torre de Marfim? Que segredos você esconde?'
    
    if 'anarquia' in processed:
        return 'Dizem que ela existe, mas como todo movimento juvenil, ele morre no esquecimento.'
    if 'poabynight' in processed:
        return 'Quer saber mais? www.poabynight.com.br!'
    else:
        return "Não to aqui pra conversar, mas confesso que tenho alguns surpresas se você continuar tentando."
    

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

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)