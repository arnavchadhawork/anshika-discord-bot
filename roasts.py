import random
import os
import json
import urllib.request
from collections import deque

# Anti-Repeat Memory (Pichle 40 responses ko yaad rakhega taaki repeat na ho)
_recent_history = deque(maxlen=40)

# ================= 60+ SHOCKING & SAVAGE ROASTS ================= #
# Ek se badhkar ek hairan kar dene wale roasts
SHOCKING_ROASTS = [
    "{user} bhai tera IQ dekh kar lagta hai ki thermometer me mercury bhi sharm se neeche gir jaye!",
    "{user} bhagwan jab dimaag baant rahe the, tab tu kahan tha? Lays ke packet me hawa gin raha tha kya?",
    "{user} teri baatein sunkar lagta hai ki shampoo ki bottle par jo 'Do Not Drink' likha hota hai, wo tere liye hi likha gaya tha!",
    "{user} tera dimaag ekdam brand new condition me hai, kyunki tune zindagi me ek baar bhi use nahi kiya!",
    "{user} tere logic sun kar toh ICU ke ventilator wale mareez bhi uth kar bol padein: 'Bhai isko pehle chup karao!'",
    "{user} tera birth certificate hospital walon ka public apology letter lagta hai!",
    "{user} tere jaiso ko dekh kar lagta hai ki Darwin ki evolution theory tere aage aakar reverse gear me chali gayi!",
    "{user} shakal se tinde jaisa lagta hai, dimaag me gobar bhara hai, aur attitude dekho jaise Ambani ka damaad ho!",
    "{user} bhai tera muh hai ya dustbin ka dhakkan? Jab khulta hai sirf gandagi aur bakwaas bahar aati hai!",
    "{user} tu dhoop me khada hoke 'light chali gayi' bolne wala namoona hai na?",
    "{user} tujhse behtar conversation toh mai apne room ki deewar se kar lu, kam se kam wo teri jaisi bakwaas toh nahi karegi!",
    "{user} teri aukaat sirf reel pe double tap karne ki hai, yahan aake gyan mat baant samjha!",
    "{user} tu wahi gadha hai na jo lift me khada hoke sochte rehta hai ki chalna kidhar se hai?",
    "{user} tere muh me daant kam aur baatein zyada hain, chup baith warna ek chammat me dimaag ghutne se bahar aa jayega!",
    "{user} itna chutiyaapa kahan se laata hai re? Kya iska koi wholesale subscription le rakha hai tune?",
    "{user} teri shakal par taras kha kar toh macchar bhi kaatne se pehle sochte honge ki 'is gareeb ko kya satayein'!",
    "{user} NASA wale space me alien dhoondh rahe hain aur yahan sabse bada ajeebo-gareeb namoona Discord pe bina dimaag ke ghoom raha hai!",
    "{user} tere dimaag me RAM 2 MB ki hai aur ghamand 1 Terabyte ka, ja pehle format karwa ke aa khud ko!",
    "{user} tu chup kar ja, warna aisa roast marungi ki tera Wi-Fi router bhi sharm se disconnect ho jayega!",
    "{user} tere paas dimaag hota toh tu aisi harkatein nahi karta, par kya karein kismat hi kharab hai teri!",
    "{user} tu bolta hai toh lagta hai dimaag chhutti pe gaya hua hai aur muh bina license ke gaadi chala raha hai!",
    "{user} aukaat 2G network jaisi hai aur baatein tu 5G speed me fek raha hai, nikal pehli fursat me!",
    "{user} agar bewakoofi ka koi aadhar card banta, toh tu usme brand ambassador hota!",
    "{user} teri shakal dekh ke toh mirror bhi bolta hoga: 'Bhai aaj ke liye itna torture kaafi hai!'",
    "{user} tu wahi hai na jo microwave ke aage khada hoke bolta hai: 'TV pe serial kab aayega?'",
    "{user} tere jaise logon ki wajah se hi sanitizer ki bottle pe 99.9% likha hota hai, kyunki 0.1% tere jaise bach jaate hain!",
    "{user} itna sasta nasha karke aata hai kya chat me? Ek dhang ki line nikal nahi rahi muh se!",
    "{user} tujhe paida karke tere doctor ne bhi tere baap se sorry bola hoga ki 'humse galti ho gayi!'",
    "{user} teri baatein sunkar Google assistant ne bhi khud ko uninstall kar liya!",
    "{user} tu wahi sample hai jo dukan pe bika nahi toh showroom ke bahar kachre me fek diya gaya tha!",
    "{user} tere muh pe mask lagana toh samaj seva ka kaam hoga, kam se kam duniya teri bakwaas se bachegi!",
    "{user} tere logic sun kar Einstein ne kabr me 360 degree palti maar li hogi!",
    "{user} tu aaina dekhna band kar de, warna wo bhi depression me aakar toot jayega!",
    "{user} dimaag bech ke aam khaye the ya bachpan me sar ke bal gir gaya tha floor pe?",
    "{user} tere paas bolne ko kuch sensible nahi hota toh keyboard pe hathoda maar ke type karta hai kya?",
    "{user} tu wahi hai na jo exam me roll number bhi galat likh ke aata tha?",
    "{user} itna vella kaise hai re tu? Ghar wale tujhe subah jhadu maar ke bahar nahi nikalte kya?",
    "{user} tu chup chap kone me baith aur saans le bas, bolne ki koshish bilkul mat kar!",
    "{user} tere jokes par toh ICU ka sabse serious mareez bhi rone lagega!",
    "{user} teri aukat dekh ke toh footpath ka kutta bhi rasta badal leta hai!",
    "{user} tere jaise logon ka aana hi Discord ke servers ka sabse bada downgrade hai!",
    "{user} tere sar me dimaag hai ya sirf Airtel ka sim card laga rakha hai 2G speed wala?",
    "{user} tu jab bolta hai, lagta hai universe ka IQ achanak se 50 points gir gaya!",
    "{user} teri dimaag ki batti jalne se pehle hi fuse ho chuki hai, electrician bula le jaldi!",
    "{user} tu wahi hai na jo pani peete waqt bhi choke kar jata hai?",
    "{user} tere sath 2 minute baat kar lo toh headache ki tablet advance me leni padti hai!",
    "{user} tere muh se bas hawa nikal rahi hai, content 0% aur bakwaas 100%!",
    "{user} chal nikal, tere jaise chomu ko reply dena bhi time waste hai!"
    # ================ 20+ EXTREME GIRL ROASTS ================ #
# Ladki bot style - bahut heavy gaaliyan
    "{user} Madarchod, teri maa ki chut mein apna haath daal ke uska ras nikaal lungi",
    "{user} Behenchod kutte, teri behen ki gaand itni faadungi ki woh chal nahi payegi",
    "{user} Bhosdike, teri maa ko nanga karke uski chuchiyaan daba ke uske muh mein thookungi",
    "{user} Randi ke pille, teri gaand mein itna lund ghusaaungi ki teri aankhein nikal jayengi",
    "{user} Madarchod saale, teri behen ki chut phaad ke uske andar apna mooth daal dungi",
    "{user} Kutte ki aulad, teri maa ki chut ka pani nikal ke usko muh pe lagaaungi",
    "{user} Behen ke laude, teri randi maa ko road pe chodte hue sabko dikhaungi",
    "{user} Harami, teri behen ki chuchiyaan kaat ke uske muh mein thukungi",
    "{user} Bhosdiwale, teri maa ki gaand mein lohe ka danda daal ke usko jalaungi",
    "{user} Madarchod, teri behen ko zor se chod ke uske muh se geeli awaaz nikalwaungi",
    "{user} Randi ke bacche, teri gaand itni faadungi ki tu baith nahi payega",
    "{user} Behenchod, teri maa ki chut mein kachra bhar ke usko sadne dungi",
    "{user} Kutte, teri behen ki chut ka ras pee ke uske muh pe thookungi",
    "{user} Bhosdike saale, teri maa ko utha ke uski chut pe apna haath maarti rahungi",
    "{user} Madarchod harami, teri behen ko nanga ghumake uski gaand sabko dikhaungi",
    "{user} Randi ke jhaantu, teri maa ki chuchiyaan daba ke uske muh mein lund ghusaaungi",
    "{user} Behen ke laude, teri gaand mein itna maal daalungi ki tu chillata rahega",
    "{user} Kutte ki aulad, teri behen ki chut phaad ke uske bacche nikaal lungi",
    "{user} Madarchod, teri maa ko chodte hue uske muh se gaali nikalwaungi",
    "{user} Bhosdiwale kamine, teri behen ki gaand faad ke uske andar apna thook daal dungi",


# ================= DYNAMIC COMBO GENERATOR (8,000+ UNIQUE COMBINATIONS) ================= #
# Har baar alag prefix + roast + punchline judkar naya roast banta hai
OPENERS = [
    "Arey oh dimaag se paidal {user},",
    "Sun be 2G network ke jamane ke {user},",
    "Oye circus ke joker {user},",
    "Bhai {user} teri shakal dekh ke lagta hai ki",
    "Arey footpath ke hero {user},",
    "Oye WhatsApp forward ke raja {user},",
    "Arey dimaag ke andhe {user},",
    "Sun be saste Aashiq {user},",
    "Oye sample piece {user},",
    "Arey vello ke sardar {user},"
]

BURNS = [
    "tujhe bhagwan ne dimaag ke naam pe sirf hawa bhari thi,",
    "tera logic sun kar calculator ne bhi error dikha diya hai,",
    "teri baatein sun kar mere phone ka speaker bhi khoon ke aansu ro raha hai,",
    "teri shakal aaine me dekh kar camera ka lens bhi blast ho jayega,",
    "tujhe dekh kar lagta hai ki school me sab tujhe blackboard saaf karne ke liye rakhte the,",
    "tere dimaag me gobar ke alawa koi teesri cheez install nahi ho sakti,",
    "teri aukaat sirf free ke Wi-Fi pe reels dekhne ki hai,",
    "tujhe dekh kar lagta hai doctor ne delivery ke time dimaag hospital me hi chhod diya tha,",
    "tu jab muh kholta hai na toh pollution level Delhi se bhi zyada badh jata hai,",
    "tere logic ke aage toh anpadh aadmi bhi sharminda ho jaye,"
]

CLOSERS = [
    "isliye chup chap kone me ja aur aaram kar!",
    "ab dobara yahan apna ganda muh mat dikhana!",
    "ja jaake thande paani se muh dho ke aa pehle!",
    "samjha na? Nikal pehli fursat me!",
    "aur zyada hero mat ban warna aisi beizzati karungi ki screen off karke rona padega!",
    "chal bhag yahan se, dimaag mat chaat!",
    "warna aisi band bajaungi ki pure server me muh dikhane layak nahi rahega!",
    "aur haan, aage se mujhe tag karne ki himmat mat karna!"
]

def generate_combo_roast(user_tag):
    """Combines Opener + Burn + Closer to create thousands of unique burns"""
    op = random.choice(OPENERS).format(user=user_tag)
    burn = random.choice(BURNS)
    closer = random.choice(CLOSERS)
    return f"{op} {burn} {closer}"

# ================= AI ROAST GENERATOR (OPTIONAL GEMINI KEY) ================= #
def get_ai_roast(user_tag, user_message):
    """
    Agar .env me GEMINI_API_KEY ho toh real-time AI se ek dum fresh, shocking roast banwayega!
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = (
            f"You are a sassy, savage, funny Delhi girl on Discord with sharp attitude and hilarious insults. "
            f"A user tagged as '{user_tag}' wrote this message: '{user_message}'. "
            f"Reply with a shocking, hilarious, highly creative and savage Hindi/Hinglish roast specifically targeting what they said. "
            f"Keep it within 1 to 2 punchy lines. Make sure you start or include their tag '{user_tag}'. "
            f"Do not be polite. Be brutally funny, savage and shocking in pure Desi meme style!"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 1.0, "maxOutputTokens": 100}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ai_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return ai_text
    except Exception as e:
        # Fallback to local deck if AI fails or times out
        return None

# ================= MAIN SELECTION (ANTI-REPEAT GUARANTEE) ================= #

def get_shocking_roast(user_tag, user_message=""):
    """
    Har baar naya, bina repeat hone wala shocking roast nikalta hai!
    """
    # 1. Try AI agar API key available ho
    if user_message:
        ai_reply = get_ai_roast(user_tag, user_message)
        if ai_reply:
            return ai_reply

    # 2. Pick from Anti-repeat deck or Combo generator
    # 50% chance shocking pre-made list, 50% chance dynamic combo generator
    for _ in range(50):
        if random.random() < 0.5:
            template = random.choice(SHOCKING_ROASTS)
            roast = template.format(user=user_tag)
        else:
            roast = generate_combo_roast(user_tag)

        # Check agar ye pichle 40 responses me nahi aaya hai
        if roast not in _recent_history:
            _recent_history.append(roast)
            return roast

    # Agar pool exhaust hone lage toh koi bhi naya combo generate karo
    fallback = generate_combo_roast(user_tag)
    _recent_history.append(fallback)
    return fallback

def get_random_mention_reply(user_tag, user_message=""):
    return get_shocking_roast(user_tag, user_message)

def get_random_roast(target_name):
    return get_shocking_roast(target_name)

def get_attitude_quote(user_tag):
    quotes = [
        "{user} Mera attitude meri marzi, jalti hai toh side se nikal!",
        "{user} Rule number 1: Mai hamesha sahi hu. Rule number 2: Agar galat hu toh Rule number 1 padh jaake!",
        "{user} Tujhse baat karne ka tax lagna chahiye, pura time waste karta hai!",
        "{user} Mai ladki hu koi public Wi-Fi nahi jo har koi connect hone aa jaye, 10 foot dur reh!",
        "{user} Bandi mai classy hu, par teri shaklein dekh ke roast apne aap nikal aata hai!"
    ]
    return random.choice(quotes).format(user=user_tag)

# ================= ANSHIKA SPECIAL FRIEND ROASTS ================= #

ANSHIKA_SPECIAL_ROASTS = [
    "🔥 Oye {friend}, {requester} ne Anshika ko bola hai teri aisi-taisi karne ke liye! Sun be dimaag se paidal chomu: Bhagwan ne tujhe dimaag diya tha ya galti se Lays ke packet me hawa pack karke bhej di thi?",
    "🔥 {friend} sun be gadhe, Anshika bol rahi hai: Teri shakal tinde jaisi aur dimaag me gobar bhara hai! {requester} ke samne hero banne ki koshish mat kar samjha?",
    "🔥 Anshika ka direct order hai {friend} ke liye: Tu wahi sample hai na jo dukan pe bika nahi toh sadak pe kachre ke dabbe me fek diya gaya tha!",
    "🔥 Oye {friend}, Anshika bol rahi hai: Tera birth certificate hospital walon ka sabse bada apology letter tha! Chup chap nikal yahan se warna aisi band bajaungi ki screen off karke rona padega!",
    "🔥 {friend} sun, {requester} ne Anshika ko bulaya hai teri band bajane: Tera IQ dekh kar toh thermometer ka mercury bhi sharm se doob mare! Nikal pehli fursat me!",
    "🔥 Anshika bol rahi hai {friend}: Aukaat teri 2G network jaisi hai aur baat tu 5G me karega? Ja pehle thande paani se muh dho ke aa!",
    "🔥 {friend} Anshika ne specially bola hai tere liye: Tu dhoop me khada hoke 'light chali gayi' bolne wala namoona hai, chup chap baith warna pure server me aisi beizzati karungi ki muh dikhane layak nahi rahega!",
    "🔥 Oye {friend}, Anshika kehti hai: Tujhe dekh kar toh Darwin ki evolution theory ne bhi reverse gear laga liya tha gadhe!",
    "🔥 Anshika ka paigaam sun {friend}: Tu jab muh kholta hai na, lagta hai sewer pipe blast ho gaya hai! Chup chap kone me baith aur muh band rakh!",
    "🔥 Oye {friend}, Anshika bol rahi hai: {requester} ne tujhe tag karke apni zindagi ka sabse bada ahsaan kiya hai tere pe, warna tere jaisi shakal ko toh kutta bhi na dekhe!"
]

def get_anshika_roast(friend_tag, requester_tag="Kisine"):
    """Anshika specially kisi dost ki band bajane ke liye"""
    template = random.choice(ANSHIKA_SPECIAL_ROASTS)
    return template.format(friend=friend_tag, requester=requester_tag)

# ================= EXTREME ROASTS & AKSHAT SPECIAL ================= #

EXTREME_ROASTS = [
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Oye sun be dimaag ke andhe, bhagwan ne jab tujhe banaya tha na, tab lagta hai 'Brain' ka plug lagana bhool gaye the aur 'Bakwaas' ka switch full speed pe on chhod diya tha! Chup baith warna aisi band bajaungi ki phone switch-off karke rona padega!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Teri shakal dekh ke toh mirror bhi bolta hoga: 'Bhai aaj ke liye itna torture kaafi hai, phone side rakh de!' Tera birth certificate dekh kar toh delivery doctor ne bhi apne clinic pe taala laga diya hoga!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Agar tu dimaag bechne nikle na, toh tera dimaag market me sabse mehenga bikega... kyunki wo 100% Brand New, Unused aur Factory-Sealed box pack hai!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Tu wahi sample hai na jo dhoop me chashma lagane ke baad chillata hai: 'Arey light chali gayi!' Shakal tinde jaisi, dimaag gobar se bhara hua aur attitude dekho jaise Ambani ka akele ka waris ho!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> NASA wale space me ajeeb creatures dhoondh rahe hain, unhe pata hi nahi ki universe ka sabse bada 404 Error yahan Discord pe bina dimaag ke ghoom raha hai!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Tera logic sun kar toh ICU ka coma patient bhi uth ke chappal utha lega! Teri aukaat 2G network ki bhi nahi hai aur baatein 5G speed me fek raha hai, nikal pehli fursat me!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Tu jab bolta hai na, aisa lagta hai universe ka average IQ achanak se 50 points gir gaya! Tere sar me dimaag nahi, sirf chips ke packet ki hawa bhari hui hai!",
    "💀 **EXTREME ROAST FOR {target}** 💀\n> Tere sath 2 minute baat karne ke baad Saridon ki poori strip advance me khaani padti hai! Chup chap kone me baith aur muh pe black tape laga le samjha na!"
]

AKSHAT_SPECIAL_ROASTS = [
    "🚨 **AKSHAT EXTREME ROAST DETECTED** 🚨\n> Oye Akshat {target}, sun be vello ke sardar! Bhagwan ne jab dimaag baanta tha na, tab tu line me khada hoke momos ki chutney maang raha tha kya? Shakal tinde jaisi aur dimaag ghutne me leke ghoomta hai tu!",
    "🚨 **AKSHAT EXTREME ROAST DETECTED** 🚨\n> Akshat {target}, tera dimaag aur band pada hua ATM dono ek barabar hain, dono me se kisi kaam ka kuch nahi nikalta! Zindagi me ek dhang ka kaam kiya nahi aur yahan hero banne aa gaya!",
    "🚨 **AKSHAT EXTREME ROAST DETECTED** 🚨\n> Oye Akshat {target}, teri aukaat sirf WhatsApp ke good morning messages forward karne ki hai! Tere jaise namoone ko dekh kar toh Darwin ki evolution theory ne bhi rasta badal liya tha!",
    "🚨 **AKSHAT EXTREME ROAST DETECTED** 🚨\n> Akshat {target} bhai, tu chup hi raha kar! Tu jab muh kholta hai na, toh lagta hai Delhi ka sewer line blast ho gaya ho. Ja pehle thande paani se muh dho ke aa!",
    "🚨 **AKSHAT EXTREME ROAST DETECTED** 🚨\n> Oye Akshat {target}, Anshika bol rahi hai: Tujh par time waste karna matlab keypad wale mobile me GTA 5 chalane jaisa impossible aur bewakoofana hai! Nikal pehli fursat me!"
]

def get_extreme_roast(target_name):
    """Ultra-brutal extreme roast"""
    template = random.choice(EXTREME_ROASTS)
    return template.format(target=target_name)

def get_akshat_roast(target_name, requester_tag="Kisine"):
    """Akshat special extreme roast"""
    template = random.choice(AKSHAT_SPECIAL_ROASTS)
    return template.format(target=target_name, requester=requester_tag)


