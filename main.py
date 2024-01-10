import random, copy
from typing import Final
from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokentoken.token_username import TOKEN,BOT_USERNAME
from vampire_random_generator.disciplines_functions import all_discipline
from vampire_random_generator.clans_text import clan_description
from vampire_random_generator.eater_eggs import easter_eggs_test, controle_updates

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
        'Versão 1.2.5\n'
        'COMANDOS:\n'
        '- /v5 X Y (X= Total de Dados | Y = Total de Dados de Fome)\n'
        '- /character_generator: Gera um personagem aleatório com Skills, Attributes e Disciplinas\n'
        '- Tenha informações sobre os clãs e disciplinas! É só digitar o nome deles na conversa!\n'
        ' Quer saber quando foi a última atualização? Digita: updates\n\n'
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
    #OBS: Tentei fazer com que o bot fornecesse um personagem aleatório de um clã específico mudando só a variável "clan" ao ser digitado "/character_generator ventrue". Não consegui e deixo isso pro meu eu do futuro.

    # NAME GENERATOR
    def name_surname_age():
        age = random.randint(18, 60)

        name_generated = random.choice(name_list)

        first_surname_generated = random.choice(surname_list)
        second_surname_generated = random.choice(surname_list)

        return f"Nome:\n{name_generated} {first_surname_generated} {second_surname_generated}\nIdade: {age}\n"


    # ATTRIBUTES GENERATOR
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

    # SKILLS GENERATOR - usa quase tudo que tá em vampir_random_generator.other_stats
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
    text = update.message.text
    # Divide o texto em partes usando espaços como delimitador
    args = text.split()

    # Verifica se há pelo menos dois argumentos
    if len(args) == 3 and args[1].isdigit() and args[2].isdigit():
        # Converte os argumentos para inteiros
        total_de_dados = int(args[1])
        dado_de_fome = int(args[2])

        # Verifica se os números são diferentes de zero -------------------------OK
        if total_de_dados == 0 and dado_de_fome == 0:
            print("Vai rolar zero dados pra que?")
            return
        elif total_de_dados == 0:
            print("Como assim o total de dados é 0 e você quer rolar alguma coisa?")
            return
        # Verifica se o dado de fome é zero ------------------------OK
        elif dado_de_fome == 0:
            # Se sim, rola o segundo número sem interferências
            result_dado_de_fome = 0
            result_total_de_dados = roll_dice(total_de_dados)
            sorted_total_de_dados = sort_dice_results(result_total_de_dados)
            ten_critic= double_ten_successes(sorted_total_de_dados)
            successes_dices = sum(1 for roll in result_total_de_dados if int(roll) >= 6)+ten_critic
            
            response_message = f"Dados: {', '.join(map(str, sorted_total_de_dados))}\nDados de fome: 0\n{successes_dices} sucessos\n"
        # Verifica se o DADO DE FOME é maior que o TOTAL DE DADOS  ------------------- ok
        elif dado_de_fome >= total_de_dados:
            # Se sim, rola o segundo número sem interferências
            result_total_de_dados = 0
            result_dado_de_fome = roll_dice(total_de_dados)
            sorted_dados_de_fome = sort_dice_results(result_dado_de_fome)
            ten_critic = double_ten_successes(sorted_dados_de_fome)
            successes_dices = sum(1 for roll in result_dado_de_fome if int(roll) >= 6)+ten_critic
            bestial = check_for_double_ten(sorted_dados_de_fome)

            response_message = f"Dados: 0\nDados de fome: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} sucessos\n{bestial}"
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
                bestial = "Crítico bestial!"
            elif 1 in sorted_total_de_dados and 1 in sorted_dados_de_fome:
                bestial = "Fracasso bestial!"

            response_message = f"Dados: {', '.join(map(str, sorted_total_de_dados))}\nDados de fome: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} sucessos\n{bestial}"

            
        await update.message.reply_text(response_message)

    else:
        # Mensagem de erro se os argumentos não forem válidos
        response_message = f"Quer usar os dados?\nJoga no formato '/v5 4 1'!\n\nNo exemplo:\n4 é o Total de Dados\n1 é o Total de Dados de Fome!\n\nO resultado aparecerá como:\nDados: resulto.\nDados de fome: resultado."

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
        crit_message = "Crítico bestial!"
    elif 1 in critic_list and 1 in critic_list:
        crit_message = "Fracasso bestial!\n"
    return crit_message
    
def roll_dice(num_dice):
    # Realiza a rolagem de dados de 10 lados
    results = [random.randint(1, 10) for _ in range(num_dice)]

    return results

def sort_dice_results(results_list):
    # Ordena a lista em ordem decrescente - Acho que isso não é necessário, mas é aquilo, já tá feito
    results_sorted = sorted(results_list, reverse=True)

    return results_sorted

async def clans_and_disciplines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Quer saber mais sobre os clãs e as suas disciplinas?\nÉ só digitar o nome deles \
aqui no chat que você vai ter algumas informações sobre eles! \
Não precisa digitar /clans_and_disciplines!\n\n'
'As opções são:\nBanu Haqim\nBrujah\nGangrel\nCaitiff\nHecata\nLasombra\nMalkavian\nMinistério\n\
Nosferatu\nRavnos\nSalubri\nToreador\nTremere\nTzimisce\nVentrue\nHumanos e Ghouls\
\n\nVocê também pode conferir informações sobre as disciplinas!\nColoca o nome delas em inglês e vai surgir um texto explicando ela.\nNão, não tá traduzido.'
)

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
    
    #Updates - controle de atualizações - vampire_random_generator / easter_eggs
    elif "updates" in processed:
        resultado_formatado = "\n".join(controle_updates)
        return resultado_formatado
    else:
        return "Digita o nome da disciplina ou do clã que você tem interesse! Tem algumas outras surpresas por aí, não desiste!"    
  
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
    app.add_handler(CommandHandler('clans',clans_and_disciplines))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)