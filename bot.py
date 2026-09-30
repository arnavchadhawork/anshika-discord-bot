import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from keep_alive import keep_alive
import roasts

# Load environment variables (.env file se)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

# Discord Intents enable karna (Message Content zaroori hai!)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Specific trigger words pe funny / savage replies (Sabme {user} tag lagega!)
TRIGGERS = {
    "i love you": "{user} Apne baap ko bol jaake, yahan aashiqi mat jhaad chomu! 💅",
    "love you": "{user} Aukaat me reh, teri aukaat se bahar hu mai! 😎",
    "kya kar rahi ho": "{user} Tere jaise vello ko beizzat karne ka plan bana rahi hu. 🔥",
    "kaisi ho": "{user} Bahut badiya thi, jab tak tune message nahi kiya tha!",
    "single ho": "{user} Single hu par tere liye toh bilkul available nahi hu!",
    "sorry": "{user} Sorry bolne se dimaag wapis aa jayega kya tera? Chal nikal!",
    "bye": "{user} Haan nikal, dimaag ka dahi karke jaa raha hai ab!",
    "marry me": "{user} Shakal dekhi hai aaine me? Subah subah sapne dekhna band kar!",
    "kya haal hai": "{user} Tere haal se toh lakh guna behtar hu mai!",
    "hi": "{user} Hello nahi sidha nikal, kaam ki baat bol!",
    "hello": "{user} Aao padhaaro, ek aur vella insaan aa gaya sar khane!",
    "anshika": "{user} Haan bol! Anshika tere baap ki naukar nahi hai jo jab chahe aawaz de deta hai! 💅",
}

# Auto-roast enabled channels set (Channel IDs)
auto_roast_channels = set()

@bot.event
async def on_ready():
    print("=" * 45)
    print(f"🔥 Savage Girl Bot '{bot.user.name}' is ONLINE!")
    print(f"👑 ID: {bot.user.id}")
    print("=" * 45)
    
    # Bot status set karna
    activity = discord.Activity(
        type=discord.ActivityType.watching, 
        name="Sabko tag karke roast kar rahi hu 💅 | !help"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message: discord.Message):
    # Agar message bot ne khud bheja hai toh ignore karo
    if message.author == bot.user or message.author.bot:
        return

    content_lower = message.content.strip().lower()
    user_tag = message.author.mention

    # Check agar kisi ne bot ke kisi message ko 'Reply' kiya hai
    is_reply_to_bot = False
    if message.reference and message.reference.resolved:
        if isinstance(message.reference.resolved, discord.Message):
            if message.reference.resolved.author == bot.user:
                is_reply_to_bot = True

    # Check agar message me kisi dost ko tag kiya gaya hai (bot aur author ke alawa)
    friends_mentioned = [m for m in message.mentions if m != bot.user and m != message.author]

    # 1. SPECIAL FEATURE: Anshika ke sath kisi dost ko tag kiya ho ya Bot ke sath dost ko tag kiya ho
    if (("anshika" in content_lower) or (bot.user.mentioned_in(message))) and friends_mentioned:
        for friend in friends_mentioned:
            roast = roasts.get_anshika_roast(friend.mention, requester_tag=user_tag)
            await message.channel.send(roast)
        return

    # 2. SPECIAL FEATURE: Akshat Extreme Roast (agar message me akshat likha ho ya tag ho)
    if "akshat" in content_lower:
        target = friends_mentioned[0].mention if friends_mentioned else ""
        roast = roasts.get_akshat_roast(target, requester_tag=user_tag)
        await message.channel.send(roast)
        return

    # 3. Agar bot ko mention kiya ho (@Bot) ya bot ke message ka Reply diya ho
    if (bot.user.mentioned_in(message) and not message.mention_everyone) or is_reply_to_bot:
        reply = roasts.get_random_mention_reply(user_tag, user_message=message.content)
        await message.reply(reply)
        return

    # 3. Trigger words check karo (Har trigger me user tag hoga)
    for trigger, template in TRIGGERS.items():
        if trigger in content_lower:
            reply = template.format(user=user_tag)
            await message.reply(reply)
            return

    # 4. Agar is channel me Auto-Roast ON hai, aur ye command nahi hai
    if message.channel.id in auto_roast_channels and not message.content.startswith(PREFIX):
        reply = roasts.get_random_mention_reply(user_tag, user_message=message.content)
        await message.channel.send(reply)
        return

    # 4. Commands process karo
    await bot.process_commands(message)

# ================= COMMANDS ================= #

@bot.command(name="roast")
async def roast_command(ctx, member: discord.Member = None):
    """Kisi dost ko roast karne ke liye: !roast @user"""
    if member is None:
        target = ctx.author.mention
        intro = f"{target} Khud hi beizzati karwani hai toh le sun:"
    else:
        target = member.mention
        intro = f"Oye {target}, sun beizzat insaan:"

    roast_msg = roasts.get_random_roast(target)
    await ctx.send(f"{intro}\n> {roast_msg}")

@bot.command(name="attitude")
async def attitude_command(ctx):
    """Girl attitude quote sunne ke liye: !attitude"""
    user_tag = ctx.author.mention
    quote = roasts.get_attitude_quote(user_tag)
    await ctx.send(f"👑 **Rani ka hukum:**\n> *\"{quote}\"*")

@bot.command(name="autoroast")
async def autoroast_command(ctx, mode: str = None):
    """
    Is channel me har message pe auto roast on/off karein:
    !autoroast on  -> Har message par tag karke roast karegi
    !autoroast off -> Normal mode (sirf tag/reply/commands par roast)
    """
    if mode is None:
        status = "ON 🔥" if ctx.channel.id in auto_roast_channels else "OFF 💤"
        await ctx.send(f"Is channel me Auto-Roast abhi **{status}** hai.\nBadalne ke liye `!autoroast on` ya `!autoroast off` likhein.")
        return

    mode = mode.lower()
    if mode == "on":
        auto_roast_channels.add(ctx.channel.id)
        await ctx.send(f"🔥 {ctx.author.mention} Auto-Roast **ON** ho gaya! Ab jo bhi kuch likhega, usko direct tag karke beizzat karungi!")
    elif mode == "off":
        auto_roast_channels.discard(ctx.channel.id)
        await ctx.send(f"💤 {ctx.author.mention} Auto-Roast **OFF** ho gaya. Ab shanti se raho!")
    else:
        await ctx.send(f"{ctx.author.mention} Sahi option likh gadhe: `!autoroast on` ya `!autoroast off`")

@bot.command(name="anshika")
async def anshika_command(ctx, member: discord.Member = None):
    """Anshika se kisi dost ki jam ke band bajwao: !anshika @dost"""
    if member is None:
        await ctx.send(f"{ctx.author.mention} Oye gadhe, kisi dost ko tag toh kar! Jaise: `!anshika @dost` ya chat me likh `anshika @dost`")
        return
    roast = roasts.get_anshika_roast(member.mention, requester_tag=ctx.author.mention)
    await ctx.send(roast)

@bot.command(name="extremeroast", aliases=["er"])
async def extremeroast_command(ctx, member: discord.Member = None):
    """Kisi dost ko extreme level pe roast karne ke liye: !extremeroast @user ya !er @user"""
    if member is None:
        target = ctx.author.mention
    else:
        target = member.mention

    roast = roasts.get_extreme_roast(target)
    await ctx.send(roast)

@bot.command(name="help")
async def help_command(ctx):
    """Help menu dikhane ke liye"""
    embed = discord.Embed(
        title="💅 Savage Girl Bot Commands",
        description="Meri baat dhyan se sun le, sabhi responses direct @tag ke sath milenge!",
        color=0xff1493 # Deep Pink
    )
    embed.add_field(name="`!extremeroast @user` (ya `!er @user`)", value="💀 **Extreme Brutal Roast**: Khatarnak level ki beizzati!", inline=False)
    embed.add_field(name="`anshika @dost` ya `!anshika @dost`", value="🔥 **Special Target:** Anshika se kisi bhi dost ki band bajwao!", inline=False)
    embed.add_field(name="`akshat` mention karna", value="🚨 Chat me 'akshat' likho ya tag karo, special extreme roast padega!", inline=False)
    embed.add_field(name="`@Bot tag karo` / Reply do", value="Mujhe mention karo ya mere message par Reply karo, direct tag karke roast karungi!", inline=False)
    embed.add_field(name="`!roast @user`", value="Kisi bhi dost ko tag karke uski band bajwao.", inline=False)
    embed.add_field(name="`!autoroast on / off`", value="**Special Mode:** Agar ON kiya toh channel me **koi bhi kuch bhi likhega**, bot usko tag karke roast karegi!", inline=False)
    embed.add_field(name="`!attitude`", value="Mera attitude dialogue sunne ke liye.", inline=False)
    embed.add_field(name="Special Triggers", value="Chat me likho: *'hi'*, *'i love you'*, *'anshika'*, *'akshat'*, *'kaisi ho'*, *'sorry'* etc.", inline=False)
    embed.set_footer(text="Zyada shana mat bano, samjhe na! 🔥")
    await ctx.send(embed=embed)

# ================= RUN BOT ================= #

def main():
    if not TOKEN or TOKEN == "your_bot_token_here":
        print("\n❌ ERROR: Discord Token nahi mila!")
        print("Kripya '.env' file me apna DISCORD_TOKEN daalein.")
        return

    # 24/7 Hosting ke liye background web server start karega
    keep_alive()

    print("🚀 Bot starting...")
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
