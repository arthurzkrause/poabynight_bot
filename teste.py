async def character_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    from vampire_random_generator.attributes import attributes_all, available_attributes_value
    from vampire_random_generator.skills import skills_all, available_skill_value
    from vampire_random_generator.name_generator.surname import surname_list
    from vampire_random_generator.name_generator.own_name import name_list
    from vampire_random_generator.other_stats import stats_generator

    #NAME GENERATOR
    def name_surname_age():
        age = random.randint(18,130)
        
        first_name = [name.strip() for name in name_list[0].split("\n") if name.strip()]
        name_generated = random.choice(first_name)

        surnames = [surname.strip() for surname in surname_list[0].split("\n") if surname.strip()]
        first_surname_generated = random.choice(surnames)
        second_surname_generated = random.choice(surnames)

        return f"Nome:{name_generated} {first_surname_generated} {second_surname_generated}\nAge: {age}\n"

    #ATTRIBUTES
    def attributes_generator():
        result = "ATTRIBUTES\n"
        for attribute in attributes_all:
            assigned_value = random.choice(available_attributes_value)
            attributes_all[attribute] = assigned_value
            available_attributes_value.remove(assigned_value)
            result += f"{attribute}: {assigned_value}\n"

        return result

    #SKILLS
    def skill_generator(category):
        result = f"\nSKILLS:\nSkills type: {category}\n"
        values = available_skill_value[category]
        
        for atributo in skills_all:
            if not values:
                skills_all[atributo] = 0
            else:
                assigned_value = random.choice(values)
                skills_all[atributo] = assigned_value
                values.remove(assigned_value)
                result += f"{atributo}: {assigned_value}\n"

        return result

    # Choose the desired category
    chosen_category = random.choice(list(available_skill_value.keys()))

    # RUN
    vampire_generated = f'{name_surname_age()}{attributes_generator()}{skill_generator(chosen_category)}{stats_generator()}'

    await update.message.reply_text(vampire_generated)