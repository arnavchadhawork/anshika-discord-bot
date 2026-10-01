import random
import os
import json
import urllib.request
from collections import deque

# Anti-Repeat Memory (Pichle 40 responses ko yaad rakhega taaki repeat na ho)
_recent_history = deque(maxlen=40)

# ================= 60+ SHOCKING & SAVAGE ROASTS ================= #
# Ek se badhkar ek hairan kar dene wale roasts
SHOCKING_ROASTS =[
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
    "{user} chal nikal, tere jaise chomu ko reply dena bhi time waste hai!",
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
        "{user}Abe madarchod, teri maa ki chut mein lund daal ke tujhe paida kiya tha kya?",
    "{user}Chup kar randi ke pille, nahi to teri gaand faad dungi",
    "{user}Tu itna chutiya hai ki teri maa bhi tujhe godi se gira deti thi sharam se",
    "{user}Abe behenchod, apni aukat mein reh warna teri gand mein danda daal dungi",
    "{user}Teri soch itni gandi hai ki even public toilet bhi tujhe reject kare",
    "{user}Chal nikal yahan se madarchod, air ko bhi toxic bana raha hai",
    "{user}Abe lavde, dimag mein sirf cum hai kya?",
    "{user}Tu itna useless hai ki teri maa ne tujhe condom se nikalne ki koshish ki ho",
    "{user}Chup kar gandu, nahi to teri gaand mein jhaadu daal ke saaf karungi",
    "{user}Tera face dekh ke lagta hai ki teri maa ne abortion fail kar diya",
    "{user}Abe randi ke bacche, thoda self-respect rakh warna teri izzat utaar dungi",
    "{user}Tu itna low-level hai ki even roadside ke kutto ko bhi sharam aati hai",
    "{user}Chal bhaag madarchod, yahan teri entry nahi hai",
    "{user}Abe chutiye, apna muh band rakh nahi to teri jeebh kaat dungi",
    "{user}Tu itna cringe hai ki even teri ex bhi tujhe block kar chuki hogi shame se",
    "{user}Chup kar behenchod, nahi to teri photo leak karke group mein daal dungi",
    "{user}Teri IQ room temperature se bhi kam hai madarchod",
    "{user}Abe gandu, thoda sense use kar warna teri gaand mein lund daal dungi",
    "{user}Chal nikal yahan se, space waste mat kar randi ke pille",
    "{user}Abe madarchod, teri maa ka bhosda faad dungi",
    "{user}Tu itna harami hai ki teri gaand se bhi gandagi nikal rahi hai",
    "{user}Chup kar lavde, nahi to teri maa ko choduungi",
    "{user}Teri aukat dekh ke lagta hai ki tu roadside ka kutta hai",
    "{user}Abe behenchod, teri chut ke baal nikal dungi",
    "{user}Tu itna chutiya hai ki condom bhi tujhe reject kare",
    "{user}Chal nikal gandu, yahan se bhag",
    "{user}Teri soch itni gandi hai ki sewage pipe bhi sharma jaye",
    "{user}Abe randi ke pille, dimag mein sirf lund hai kya?",
    "{user}Chup kar madarchod, nahi to teri gaand mein bottle daal dungi",
    "{user}Tu itna useless hai ki even dustbin tujhe nahi chahta",
    "{user}Abe lavde, teri maa ki chut saaf kar",
    "{user}Tera face dekh ke lagta hai ki tu failed experiment hai",
    "{user}Chal bhaag behenchod, air pollution mat badha",
    "{user}Abe gandu, thoda aukat mein reh",
    "{user}Tu itna low-level hai ki kutto ko bhi sharam aaye",
    "{user}Chup kar chutiye, nahi to teri jeebh kaat ke kha lungi",
    "{user}Abe madarchod, self-respect rakh",
    "{user}Chal nikal yahan se, space waste mat kar",
    "{user}Abe randi ke bacche, teri gaand faad ke rakh dungi",
    "{user}Tu itna harami hai ki teri maa bhi tujhe godi se gira deti",
    "{user}Chup kar lavde, nahi to teri photo leak kar dungi",
    "{user}Teri IQ dekh ke lagta hai ki tu room temperature pe jeeta hai",
    "{user}Abe behenchod, sense use kar",
    "{user}Tu itna cringe hai ki second-hand embarrassment bhi door rehta hai",
    "{user}Chal bhaag gandu, yahan teri entry nahi",
    "{user}Abe chutiye, muh band rakh",
    "{user}Teri personality flat hai jaise teri maa ki chut",
    "{user}Abe madarchod, aukat mein reh",
    "{user}Tu itna chutiya hai ki Google bhi search nahi karta",
    "{user}Chup kar randi ke pille",
    "{user}Abe lavde, teri maa ka bhosda",
    "{user}Teri soch gandi hai jaise teri gaand",
    "{user}Chal nikal behenchod",
    "{user}Abe gandu, dimag mein hawa hai",
    "{user}Tu useless hai jaise broken condom",
    "{user}Chup kar madarchod",
    "{user}Tera face failed abortion jaisa hai",
    "{user}Abe randi ke bacche, self-respect rakh",
    "{user}Tu low-level hai jaise roadside kutta",
    "{user}Chal bhaag lavde",
    "{user}Abe chutiye, sense use kar",
    "{user}Teri baatein gandi hain jaise teri maa ki chut",
    "{user}Abe behenchod, muh band",
    "{user}Tu cringe hai jaise teri ex ki zindagi",
    "{user}Chup kar gandu",
    "{user}Teri IQ zero hai madarchod",
    "{user}Abe lavde, gaand mein lund daal dungi",
    "{user}Chal nikal randi ke pille",
    "{user}Abe madarchod, teri maa ko chodu",
    "{user}Tu harami hai jaise teri soch",
    "{user}Chup kar behenchod",
    "{user}Teri aukat kutto se kam hai",
    "{user}Abe gandu, chut ke baal nikal",
    "{user}Tu chutiya hai jaise failed plan",
    "{user}Chal bhaag lavde",
    "{user}Abe randi ke bacche, sewage jaisa sochta hai",
    "{user}Chup kar madarchod",
    "{user}Tera dimag cum se bhara hai",
    "{user}Abe chutiye, dustbin bhi reject kare",
    "{user}Tu useless hai jaise teri existence",
    "{user}Chal nikal gandu",
    "{user}Abe behenchod, maa ki chut saaf kar",
    "{user}Tera face experiment fail hai",
    "{user}Abe lavde, air toxic mat bana",
    "{user}Chup kar randi ke pille",
    "{user}Teri aukat zero hai",
    "{user}Abe madarchod, kutto se bhi kam",
    "{user}Tu low-level hai jaise teri IQ",
    "{user}Chal bhaag chutiye",
    "{user}Abe gandu, jeebh kaat dungi",
    "{user}Teri baatein maa ki chut se aayi hain",
    "{user}Abe lavde, self-respect rakh",
    "{user}Chup kar behenchod",
    "{user}Tu space waste kar raha hai",
    "{user}Abe randi ke bacche, gaand faad dungi",
    "{user}Teri maa godi se gira deti",
    "{user}Chal nikal madarchod",
    "{user}Abe chutiye, photo leak kar dungi",
    "{user}Teri IQ room temp se kam",
    "{user}Abe gandu, sense use kar",
    "{user}Chup kar lavde",
    "{user}Tu cringe hai jaise teri zindagi",
    "{user}Abe behenchod, entry nahi hai",
    "{user}Tera muh band rakh",
    "{user}Abe madarchod, personality flat hai",
    "{user}Tu aukat mein reh",
    "{user}Chal bhaag randi ke pille",
    "{user}Abe lavde, Google bhi reject kare",
    "{user}Chup kar gandu",
    "{user}Teri maa ka bhosda",
    "{user}Abe chutiye, soch gandi hai",
    "{user}Tu nikal yahan se",
    "{user}Abe behenchod, dimag hawa hai",
    "{user}Tera condom fail hai",
    "{user}Abe madarchod, chup kar",
    "{user}Tu face failed hai",
    "{user}Chal nikal lavde",
    "{user}Abe randi ke bacche, self-respect",
    "{user}Teri level kutto jaisi",
    "{user}Abe gandu, sense",
    "{user}Chup kar chutiye",
    "{user}Teri baatein gandi",
    "{user}Abe lavde, muh band",
    "{user}Tu cringe hai",
    "{user}Chal bhaag behenchod",
    "{user}Abe madarchod, IQ zero",
    "{user}Teri gaand mein lund",
    "{user}Abe randi ke pille, nikal",
    "{user}Tu harami hai",
    "{user}Chup kar gandu",
    "{user}Teri aukat kutto se kam",
    "{user}Abe chutiye, chut ke baal",
    "{user}Tu failed hai",
    "{user}Chal nikal lavde",
    "{user}Abe behenchod, sewage soch",
    "{user}Chup kar madarchod",
    "{user}Tera dimag cum",
    "{user}Abe gandu, dustbin reject",
    "{user}Tu useless existence",
    "{user}Chal bhaag randi ke bacche",
    "{user}Abe lavde, maa ki chut",
    "{user}Tera face fail",
    "{user}Abe chutiye, air toxic",
    "{user}Chup kar behenchod",
    "{user}Teri aukat zero",
    "{user}Abe madarchod, kutto se kam",
    "{user}Tu low IQ",
    "{user}Chal nikal gandu",
    "{user}Abe lavde, jeebh kaat",
    "{user}Teri baatein chut se",
    "{user}Abe randi ke pille, self-respect",
    "{user}Chup kar chutiye",
    "{user}Tu space waste",
    "{user}Abe behenchod, gaand faad",
    "{user}Teri maa gira deti",
    "{user}Chal nikal madarchod",
    "{user}Abe gandu, photo leak",
    "{user}Teri IQ kam",
    "{user}Abe lavde, sense",
    "{user}Chup kar randi ke bacche",
    "{user}Tu cringe zindagi",
    "{user}Abe chutiye, entry nahi",
    "{user}Tera muh band",
    "{user}Abe madarchod, flat personality",
    "{user}Tu aukat mein",
    "{user}Chal nikal behenchod",
    "{user}Abe gandu, Google reject",
    "{user}Chup kar lavde",
    "{user}Teri maa bhosda",
    "{user}Abe randi ke pille, gandi soch",
    "{user}Tu nikal",
    "{user}Abe chutiye, dimag hawa",
    "{user}Tera condom fail",
    "{user}Abe madarchod, chup",
    "{user}Tu face fail",
    "{user}Chal bhaag gandu",
    "{user}Abe lavde, self-respect",
    "{user}Teri level kutta",
    "{user}Abe behenchod, sense",
    "{user}Chup kar chutiye",
    "{user}Teri baatein gandi",
    "{user}Abe madarchod, muh band",
    "{user}Tu cringe",
    "{user}Chal nikal randi ke bacche",
    "{user}Abe gandu, IQ zero",
    "{user}Teri gaand lund",
    "{user}Abe lavde, nikal",
    "{user}Tu harami",
    "{user}Chup kar behenchod",
    "{user}Teri aukat kam",
    "{user}Abe chutiye, chut baal",
    "{user}Tu failed",
    "{user}Chal bhaag madarchod",
    "{user}Abe gandu, sewage",
    "{user}Chup kar lavde",
    "{user}Tera dimag cum",
    "{user}Abe randi ke pille, dustbin",
    "{user}Tu useless",
    "{user}Abe madarchod, existence waste",
    "{user}Chal nikal chutiye",
    "{user}Abe behenchod, maa ki chut",
    "{user}Tera face fail experiment",
    "{user}Abe gandu, toxic air",
    "{user}Chup kar lavde",
    "{user}Teri aukat zero",
    "{user}Abe randi ke bacche, kutto se kam",
    "{user}Tu low-level IQ",
    "{user}Abe madarchod, jeebh kaat dungi",
    "{user}Abe madarchod, teri maa ki chut mein keede pal rahe hain",
    "{user}Chup kar randi ke pille, nahi to teri gaand mein haath daal ke saaf karungi,
    "{user}Tu itna harami hai ki teri maa bhi tujhe dekh ke ulti kar de",
    "{user}Abe behenchod, teri gand faad ke usme rassi daal dungi",
    "{user}Teri soch itni gandi hai ki even drain pipe bhi tujhe nahi chahta",
    "{user}Chal nikal yahan se lavde, pollution mat faila",
    "{user}Abe gandu, dimag mein sirf teri maa ki chut hai kya?",
    "{user}Tu itna useless hai ki condom bhi tujhe pehenne se mana kar de",
    "{user}Chup kar madarchod, nahi to teri jeebh kheench ke fek dungi",
    "{user}Tera face dekh ke lagta hai ki teri maa ne tujhe thook ke paida kiya",
    "{user}Abe randi ke bacche, thoda izzat rakh warna teri gaand mein joota daal dung,
    "{user}Tu itna low-level hai ki even street dogs tujhe bhaunkte hain",
    "{user}Chal bhaag chutiye, yahan se gand mat faila",
    "{user}Teri baatein sun ke lagta hai ki tu apni maa ki chut mein hi reh gaya",
    "{user}Abe lavde, apna muh band rakh nahi to teri daant tod dungi",
    "{user}Tu itna cringe hai ki even teri mummy tujhe dekh ke sharma jaye",
    "{user}Chup kar behenchod, nahi to teri nangi photo group mein bhej dungi",
    "{user}Teri IQ itni kam hai ki even calculator tujhe calculate nahi kar pata",
    "{user}Abe gandu, thoda dimag laga warna teri gaand mein bamboo daal dungi",
    "{user}Chal nikal yahan se, space mat ganda kar randi ke pille",
    "{user}Abe madarchod, teri maa ka bhosda chaat",
    "{user}Tu itna harami hai ki teri gaand se bhi badbu aa rahi hai",
    "{user}Chup kar lavde, nahi to teri maa ko road pe khada kar dungi",
    "{user}Teri aukat dekh ke lagta hai ki tu gutter ka keeda hai",
    "{user}Abe behenchod, teri chut saaf kar ke rakh",
    "{user}Tu itna chutiya hai ki even free WiFi bhi tujhe connect nahi kare",
    "{user}Chal nikal gandu, yahan se bhag ja",
    "{user}Teri soch itni gandi hai ki public toilet bhi sharma jaye",
    "{user}Abe randi ke pille, dimag mein sirf gaand hai kya?",
    "{user}Chup kar madarchod, nahi to teri gaand mein rod daal dungi",
    "{user}Tu itna useless hai ki even recycle bin tujhe delete kar de",
    "{user}Abe lavde, teri maa ki chut mein haath daal",
    "{user}Tera face dekh ke lagta hai ki tu plastic surgery fail hai",
    "{user}Chal bhaag behenchod, air mat kharab kar",
    "{user}Abe gandu, thoda aukat dekh",
    "{user}Tu itna low-level hai ki even cockroach better hai",
    "{user}Chup kar chutiye, nahi to teri jeebh kaat ke kutto ko khila dungi",
    "{user}Teri baatein sun ke lagta hai ki tu apni maa ki chut se seedha aaya",
    "{user}Abe madarchod, self-respect naam ki cheez rakh",
    "{user}Chal nikal yahan se, gand mat faila",
    "{user}Abe randi ke bacche, teri gaand mein lund daal ke ghumungi",
    "{user}Tu itna harami hai ki teri maa tujhe dekh ke rone lage",
    "{user}Chup kar lavde, nahi to teri photo deepfake bana dungi",
    "{user}Teri IQ dekh ke lagta hai ki tu fridge temperature pe sochta hai",
    "{user}Abe behenchod, sense naam ki cheez use kar",
    "{user}Tu itna cringe hai ki even NPC tujhe ignore kare",
    "{user}Chal bhaag gandu, yahan teri jagah nahi",
    "{user}Abe chutiye, muh band rakh warna faad dungi",
    "{user}Teri personality itni flat hai ki teri maa ki chut jaisi",
    "{user}Abe madarchod, aukat mein reh nahi to utaar dungi",
    "{user}Tu itna chutiya hai ki search engine bhi tujhe nahi dikhata",
    "{user}Chup kar randi ke pille, warna gaand saaf karungi",
    "{user}Abe lavde, teri maa ka bhosda faad",
    "{user}Teri soch gandi hai jaise teri purani underwear",
    "{user}Chal nikal behenchod, pollution failane wale",
    "{user}Abe gandu, dimag mein sirf hawa aur cum",
    "{user}Tu useless hai jaise phata hua condom",
    "{user}Chup kar madarchod, nahi to block + leak",
    "{user}Tera face failed birth control jaisa hai",
    "{user}Abe randi ke bacche, thoda izzat seekh",
    "{user}Tu low-level hai jaise roadside ka kachra",
    "{user}Chal bhaag lavde, yahan se",
    "{user}Abe chutiye, sense laga",
    "{user}Teri baatein gandi hain jaise teri maa ki gaand",
    "{user}Abe behenchod, muh band kar",
    "{user}Tu cringe hai jaise teri poori family",
    "{user}Chup kar gandu, warna dekh lena",
    "{user}Teri IQ negative hai madarchod",
    "{user}Abe lavde, gaand mein pure lund daal dungi",
    "{user}Chal nikal randi ke pille",
    "{user}Abe madarchod, teri maa ko pure group se chudwaungi",
    "{user}Tu harami hai jaise teri soch ka level",
    "{user}Chup kar behenchod, nahi to live stream kar dungi",
    "{user}Teri aukat kutto se bhi neeche",
    "{user}Abe gandu, chut ke baal ek ek nikalungi",
    "{user}Tu chutiya hai jaise plan B fail",
    "{user}Chal bhaag lavde, gand failane wale",
    "{user}Abe randi ke bacche, sewage se bhi gandi soch",
    "{user}Chup kar madarchod",
    "{user}Tera dimag pure cum se bhara pada hai",
    "{user}Abe chutiye, dustbin bhi tujhe nahi lega",
    "{user}Tu useless hai jaise teri poori zindagi",
    "{user}Chal nikal gandu",
    "{user}Abe behenchod, maa ki chut chaat",
    "{user}Tera face pure experiment fail",
    "{user}Abe lavde, air ko poison mat bana",
    "{user}Chup kar randi ke pille",
    "{user}Teri aukat pure zero",
    "{user}Abe madarchod, kutto se bhi neeche level",
    "{user}Tu low-level IQ wala gandu",
    "{user}Chal bhaag chutiye",
    "{user}Abe gandu, jeebh kheench lungi",
    "{user}Teri baatein pure chut se nikal rahi hain",
    "{user}Abe lavde, self-respect seekh",
    "{user}Chup kar behenchod",
    "{user}Tu pure space waste",
    "{user}Abe randi ke bacche, gaand pure faad dungi",
    "{user}Teri maa tujhe dekh ke gira deti",
    "{user}Chal nikal madarchod",
    "{user}Abe chutiye, pure photo leak",
    "{user}Teri IQ pure kam",
    "{user}Abe gandu, sense laga le",
    "{user}Chup kar lavde",
    "{user}Tu cringe pure level ka",
    "{user}Abe behenchod, entry band hai",
    "{user}Tera muh pure band rakh",
    "{user}Abe madarchod, personality pure flat",
    "{user}Tu aukat mein reh nahi to",
    "{user}Chal bhaag randi ke pille",
    "{user}Abe lavde, Google bhi tujhe nahi dhundta",
    "{user}Chup kar gandu",
    "{user}Teri maa ka pure bhosda",
    "{user}Abe chutiye, soch pure gandi",
    "{user}Tu nikal yahan se abhi",
    "{user}Abe behenchod, dimag pure hawa",
    "{user}Tera condom pure fail",
    "{user}Abe madarchod, chup ab",
    "{user}Tu face pure fail",
    "{user}Chal bhaag lavde",
    "{user}Abe randi ke bacche, self-respect rakh le",
    "{user}Teri level pure kutta",
    "{user}Abe gandu, sense use kar le",
    "{user}Chup kar chutiye",
    "{user}Teri baatein pure gandi",
    "{user}Abe lavde, muh pure band",
    "{user}Tu cringe pure",
    "{user}Chal nikal behenchod",
    "{user}Abe madarchod, IQ pure zero",
    "{user}Teri gaand mein pure lund",
    "{user}Abe randi ke pille, nikal ab",
    "{user}Tu harami pure level",
    "{user}Chup kar gandu",
    "{user}Teri aukat pure kam",
    "{user}Abe chutiye, chut ke baal pure",
    "{user}Tu failed pure",
    "{user}Chal bhaag madarchod",
    "{user}Abe gandu, sewage pure",
    "{user}Chup kar lavde",
    "{user}Tera dimag pure cum",
    "{user}Abe randi ke bacche, dustbin reject",
    "{user}Tu useless pure",
    "{user}Abe madarchod, existence pure waste",
    "{user}Chal nikal chutiye",
    "{user}Abe behenchod, maa ki pure chut",
    "{user}Tera face pure fail experiment",
    "{user}Abe gandu, toxic pure air",
    "{user}Chup kar lavde",
    "{user}Teri aukat pure zero",
    "{user}Abe randi ke bacche, kutto se pure kam",
    "{user}Tu low-level pure IQ",
    "{user}Abe madarchod, jeebh pure kaat",
    "{user}Chal bhaag gandu",
    "{user}Abe lavde, baatein pure chut",
    "{user}Teri self-respect pure zero",
    "{user}Abe behenchod, chup abhi",
    "{user}Tu space pure waste",
    "{user}Abe chutiye, gaand pure faad",
    "{user}Teri maa pure gira deti",
    "{user}Chal nikal madarchod",
    "{user}Abe gandu, photo pure leak",
    "{user}Teri IQ pure neeche",
    "{user}Abe lavde, sense pure laga",
    "{user}Chup kar randi ke pille",
    "{user}Tu cringe pure zindagi",
    "{user}Abe behenchod, entry pure nahi",
    "{user}Tera muh pure band",
    "{user}Abe madarchod, personality pure flat",
    "{user}Tu aukat pure mein reh",
    "{user}Chal bhaag gandu",
    "{user}Abe lavde, Google pure reject",
    "{user}Chup kar chutiye",
    "{user}Teri maa pure bhosda",
    "{user}Abe randi ke bacche, gandi pure soch",
    "{user}Tu nikal pure ab",
    "{user}Abe behenchod, dimag pure hawa",
    "{user}Tera condom pure fail",
    "{user}Abe madarchod, chup pure",
    "{user}Tu face pure fail",
    "{user}Chal bhaag lavde",
    "{user}Abe gandu, self-respect pure",
    "{user}Teri level pure kutta",
    "{user}Abe chutiye, sense pure",
    "{user}Chup kar behenchod",
    "{user}Teri baatein pure gandi",
    "{user}Abe madarchod, muh pure band",
    "{user}Tu cringe pure level",
    "{user}Chal nikal randi ke pille",
    "{user}Abe lavde, IQ pure zero",
    "{user}Teri gaand pure lund",
    "{user}Abe gandu, nikal pure abhi",
    "{user}Teri baatein sun ke lagta hai ki tu apni maa ki chut se nikalte waqt dimag bhool gaya"
]


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


