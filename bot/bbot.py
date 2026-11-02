import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Бот міні-ігор {bot.user} успішно запущений!')
    try:
        synced = await bot.tree.sync()
        print(f"Синхронізовано {len(synced)} ігрових команд.")
    except Exception as e:
        print(e)

# --- 1. КУБИК / РОЛІ ---
@bot.tree.command(name="roll", description="Кинути гральний кубик (від 1 до 6)")
async def roll(interaction: discord.Interaction):
    result = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 **{interaction.user.display_name}** кинув(ла) кубик і випало: **{result}**!")

@bot.tree.command(name="roll100", description="Кинути кубик на 100 граней")
async def roll100(interaction: discord.Interaction):
    result = random.randint(1, 100)
    await interaction.response.send_message(f"🎯 **{interaction.user.display_name}** кинув(ла) кубик (1-100) і випало: **{result}**!")

# --- 2. ОРЕЛ ЧИ РЕШКА ---
@bot.tree.command(name="coinflip", description="Підкинути монетку (орел чи решка)")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Орел 🦅", "Решка 🪙"])
    await interaction.response.send_message(f"🪙 Монетка в повітрі... і випало: **{result}** для **{interaction.user.display_name}**!")

# --- 3. МАГІЧНА КУЛЯ (8ball) ---
@bot.tree.command(name="8ball", description="Задати запитання магічній кулі")
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = [
        "Безумовно так! ✨", "Звісно", "Навіть не сумнівайся", 
        "Складно сказати, спробуй знову 🤔", "Краще поки не розповідати", 
        "На жаль, ні ❌", "Зовсім ні", "Дуже мало шансів"
    ]
    answer = random.choice(answers)
    embed = discord.Embed(title="🎱 Магічна куля", color=discord.Color.dark_purple())
    embed.add_field(name="Запитання:", value=question, inline=False)
    embed.add_field(name="Відповідь:", value=answer, inline=False)
    await interaction.response.send_message(embed=embed)

# --- 4. ВИБІР З ВАРІАНТІВ ---
@bot.tree.command(name="choose", description="Допомогти обрати між варіантами (через кому)")
async def choose(interaction: discord.Interaction, options: str):
    choices = [opt.strip() for opt in options.split(",")]
    if len(choices) < 2:
        await interaction.response.send_message("Будь ласка, введіть хоча б два варіанти через кому! (Приклад: *Кава, Чай, Сік*)", ephemeral=True)
        return
    chosen = random.choice(choices)
    await interaction.response.send_message(f"🤔 Я думаю, що найкращий варіант для **{interaction.user.display_name}**: **{chosen}**! 🎉")

# --- 5. КАМІНЬ, НОЖИЦІ, ПАПІР ---
@bot.tree.command(name="rps", description="Зіграти в Камінь-Ножиці-Папір з ботом")
async def rps(interaction: discord.Interaction, choice: str):
    choice = choice.lower()
    options = ["камінь", "ножиці", "папір"]
    if choice not in options:
        await interaction.response.send_message("Оберіть одне з трьох: *камінь*, *ножиці* або *папір*!", ephemeral=True)
        return
    
    bot_choice = random.choice(options)
    
    # Визначаємо переможця
    if choice == bot_choice:
        result = "Нічия! 🤝"
    elif (choice == "камінь" and bot_choice == "ножиці") or \
         (choice == "ножиці" and bot_choice == "папір") or \
         (choice == "папір" and bot_choice == "камінь"):
        result = "Ви перемогли! 🎉"
    else:
        result = "Я переміг! 🤖😎"
        
    embed = discord.Embed(title="✊ ✂️ 📄 Камінь-Ножиці-Папір", color=discord.Color.blue())
    embed.add_field(name="Ваш вибір:", value=choice.capitalize(), inline=True)
    embed.add_field(name="Мій вибір:", value=bot_choice.capitalize(), inline=True)
    embed.add_field(name="Результат:", value=result, inline=False)
    await interaction.response.send_message(embed=embed)

# --- 6. КАЗИНО / РУЛЕТКА (СЛОТИ) ---
@bot.tree.command(name="slots", description="Зіграти у міні-слоти (однорукий бандит)")
async def slots(interaction: discord.Interaction):
    emojis = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
    result = [random.choice(emojis) for _ in range(3)]
    
    if result[0] == result[1] == result[2]:
        msg = " джекпот! Неймовірна перемога! 💰🎉"
        color = discord.Color.gold()
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        msg = " непогано, є збіг! ✨"
        color = discord.Color.green()
    else:
        msg = " на жаль, пощастить наступного разу! 😢"
        color = discord.Color.red()
        
    embed = discord.Embed(title="🎰 Казино Слоти", description=f"**[ {' | '.join(result)} ]**\n{interaction.user.mention},{msg}", color=color)
    await interaction.response.send_message(embed=embed)

# --- 7. ВГАДАЙ ЧИСЛО ---
@bot.tree.command(name="guess", description="Вгадай число від 1 до 10")
async def guess(interaction: discord.Interaction, number: int):
    if number < 1 or number > 10:
        await interaction.response.send_message("Будь ласка, введіть число від 1 до 10!", ephemeral=True)
        return
    secret = random.randint(1, 10)
    if number == secret:
        await interaction.response.send_message(f"🎉 Вітаю! Ви вгадали число **{secret}**!")
    else:
        await interaction.response.send_message(f"😢 На жаль, загадане число було **{secret}**, а ви обрали **{number}**.")

# --- 8. КАРТА ДНЯ ---
@bot.tree.command(name="card", description="Отримати випадкову «карту дня»")
async def card(interaction: discord.Interaction):
    cards = [
        "Туз Кубків — день наповнений коханням та емоціями 💖",
        "Колесо Фортуни — готуйтесь до несподіваних приємних змін 🎡",
        "Зірка — ваші мрії починають здійснюватися ✨",
        "Маг — чудовий день для нових звершень та проєктів 🔮",
        "Сонце — максимальний заряд позитиву та радості ☀️",
        "Сила — ваша внутрішня енергія подолає будь-які перешкоди 💪"
    ]
    await interaction.response.send_message(f"🃏 **{interaction.user.display_name}**, ваша карта дня:\n> **{random.choice(cards)}**")

# --- 9. КОМПЛІМЕНТ ВІД БОТА ---
@bot.tree.command(name="compliment", description="Отримати випадковий приємний комплімент")
async def compliment(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    phrases = [
        "сьогодні виглядає просто неперевершено! ✨",
        "має неймовірну харизму, яка зачаровує всіх навколо 🌟",
        "це людина з найдобрішим серцем на сервері 💖",
        "геній продуктивності та натхнення 🧠👑"
    ]
    await interaction.response.send_message(f"🥰 **{target.mention}** {random.choice(phrases)}")

# --- 10. БІЙ НА МЕЧАХ ---
@bot.tree.command(name="duel", description="Викликати користувача на жартівливу дуель")
async def duel(interaction: discord.Interaction, user: discord.Member):
    if user == interaction.user:
        await interaction.response.send_message("Битися із самим собою — це занадто шизофренічно навіть для пекла! 😅", ephemeral=True)
        return
    winner = random.choice([interaction.user, user])
    loser = user if winner == interaction.user else interaction.user
    await interaction.response.send_message(f"⚔️ **{interaction.user.mention}** та **{user.mention}** зійшлися у запеклому поєдинку...\n🏆 У цій битві переміг(ла) **{winner.mention}**! Вітаємо переможця, а другому дістався легкий ляпас! 🤺")

# --- 11. НАУКОВЕ ПЕРЕВІРЕННЯ КОХАННЯ ---
@bot.tree.command(name="love", description="Перевірити відсоток сумісності кохання")
async def love(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    score = random.randint(0, 100)
    if score > 80:
        comment = "Ідеальна пара! Справжнє кохання у пеклі! 💖🔥"
    elif score > 50:
        comment = "Чудовий потенціал, варто придивитися одне до одного! 😉"
    else:
        comment = "Ну... принаймні ви можете бути друзями 😅"
        
    embed = discord.Embed(title="❤️ Тест сумісності", color=discord.Color.pink())
    embed.description = f"Сумісність між **{user1.mention}** та **{user2.mention}** становить: **{score}%**!\n_{comment}_"
    await interaction.response.send_message(embed=embed)

# --- 12. ВИПАДКОВЕ КОШЕНЯ ---
@bot.tree.command(name="cat", description="Отримати миле аніме-кошеня")
async def cat(interaction: discord.Interaction):
    cats = [
        "https://media.tenor.com/J52w7z8v_24AAAAC/cute-cat.gif",
        "https://media.tenor.com/39wV7z8v_24AAAAC/cat-anime.gif"
    ]
    embed = discord.Embed(title="🐱 Мр-р-р...", color=discord.Color.orange())
    embed.set_image(url=random.choice(cats))
    await interaction.response.send_message(embed=embed)

# --- 13. ВИПАДКОВЕ АНІМЕ СЛОВО ---
@bot.tree.command(name="fact", description="Дізнатися випадковий факт")
async def fact(interaction: discord.Interaction):
    facts = [
        "Птахи — це єдині живі нащадки динозаврів 🦖",
        "Медузи на 95% складаються з води 💧",
        "Коти проводять близько 70% свого життя уві сні 😴",
        "У світі існує більше зірочок, ніж піщинок на всіх пляжах Землі ✨"
    ]
    await interaction.response.send_message(f"🧠 **Науковий факт:** {random.choice(facts)}")

# --- 14. СКАУТ ПРИГОД ---
@bot.tree.command(name="adventure", description="Вирушити у випадкову міні-пригоду")
async def adventure(interaction: discord.Interaction):
    adventures = [
        "вирушив(ла) у темний ліс і знайшов(ла) скриньку з шоколадками! 🍫",
        "зустрів(ла) мандрівного мага, який подарував порцію гарного настрою ✨",
        "заблукав(ла) у чавунному лабіринті, але знайшов(ла) вихід та смачну каву ☕",
        "виграв(ла) у дракона в карти та отримав(ла) скарби 🐉💰"
    ]
    await interaction.response.send_message(f"🗺️ **{interaction.user.mention}** {random.choice(adventures)}")

# --- 15. КОЕФІЦІЄНТ ДНЯ ---
@bot.tree.command(name="rate", description="Оцінити щось за шкалою від 1 до 10")
async def rate(interaction: discord.Interaction, item: str):
    score = random.randint(1, 10)
    await interaction.response.send_message(f"📊 Я оцінюю **«{item}»** для **{interaction.user.display_name}** на **{score}/10**! ⭐")

# --- 16. СЛОВАРИК ПЕКЛА ---
@bot.tree.command(name="slang", description="Дізнатися випадковий рандомний статус")
async def slang(interaction: discord.Interaction):
    statuses = ["Легенда сервера 👑", "Головний бунтар 😈", "Сонний котик 💤", "Любитель кави ☕", "Майстер хаосу 🌪️"]
    await interaction.response.send_message(f"🏷️ Ваш поточний статус на сервері: **{random.choice(statuses)}**")

# --- 17. СКАЗАСТИ ПРАВДУ ЧИ ДІЮ (Жартівливо) ---
@bot.tree.command(name="truth", description="Отримати запитання «Правда»")
async def truth(interaction: discord.Interaction):
    questions = [
        "Яка твоя улюблена гра на комп'ютері?",
        "Який твій улюблений смак смаколиків?",
        "Якби ти міг(ла) стати твариною на один день, ким би став(ла)?",
        "Яка була твоя найсмішніша помилка у житті?"
    ]
    await interaction.response.send_message(f"❓ **Правда для {interaction.user.mention}:** {random.choice(questions)}")

# --- 18. ПОКИДАТИ КУБИКІВ (ДВА) ---
@bot.tree.command(name="dice2", description="Кинути два гральні кубики одночасно")
async def dice2(interaction: discord.Interaction):
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    total = d1 + d2
    await interaction.response.send_message(f"🎲🎲 **{interaction.user.display_name}** кинув два кубики: **{d1}** та **{d2}** (Сума: **{total}**)")

# --- 19. АСТРОЛОГІЧНИЙ ПРОГНОЗ ---
@bot.tree.command(name="astro", description="Короткий абсурдний гороскоп на сьогодні")
async def astro(interaction: discord.Interaction):
    forecasts = [
        "Сьогодні уникайте чорних котів і надмірного споживання кави ☕",
        "Зірки кажуть, що на вас чекає несподіваний прибуток у вигляді гарного настрою ✨",
        "Чудовий день для того, щоб нічого не робити і пишатися цим 🛋️",
        "Хтось на сервері готує проти вас змову... з обіймів та компліментів 🤗"
    ]
    await interaction.response.send_message(f"🔮 **Гороскоп для {interaction.user.mention}:** {random.choice(forecasts)}")

# --- 20. КРИСТАЛ МУДРОСТІ ---
@bot.tree.command(name="wisdom", description="Отримати випадкову мудрість від бота")
async def wisdom(interaction: discord.Interaction):
    wisdoms = [
        "Хто встає раніше за всіх — той хоче спати весь день 😴",
        "Якщо проблема вирішується грошима — це не проблема, це витрати 💸",
        "Чашка кави вранці рятує світ від катастрофи ☕✨",
        "Ніколи не відкладайте на завтра те, що можна зробити післязавтра 🐢"
    ]
    await interaction.response.send_message(f"📜 **Мудрість дня:** _{random.choice(wisdoms)}_")

@bot.tree.command(name="check_eco", description="Швидка перевірка стану бота")
async def check_status(interaction: discord.Interaction):
    await interaction.response.send_message("🟢 Цей бот на зв'язку і працює стабільно!", ephemeral=True)

# Ваш токен для нового бота міні-ігор:
import os
bot.run(os.getenv('TOKEN'))