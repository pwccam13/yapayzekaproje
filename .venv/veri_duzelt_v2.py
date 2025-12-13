import os


def verileri_onar():
    print("Veri tabanı onarılıyor...")

    trait_map = {
        "Lux": "Poke / Mage", "Hecarim": "Skirmisher / Engage", "Janna": "Enchanter / Disengage",
        "Zeri": "Hypercarry / Mobile",
        "Ezreal": "Poke / Mobile", "Fiora": "Duelist / Splitpush", "Darius": "Lane Bully / Juggernaut",
        "Kai'Sa": "Assassin / Hypercarry",
        "Draven": "Lane Bully / Snowball", "Camille": "Duelist / Diver", "Graves": "Skirmisher / Carry",
        "Akali": "Assassin / Mobile",
        "Talon": "Assassin / Roam", "Nidalee": "Assassin / Poke", "Fizz": "Assassin / Burst",
        "Qiyana": "Assassin / AD Burst",
        "Lucian": "Lane Bully / Burst", "Nami": "Enchanter / Engage", "Kassadin": "Scaling / Mage",
        "Sylas": "Skirmisher / Magic",
        "Kennen": "Teamfight / Engage", "Zoe": "Poke / Burst", "Bard": "Roam / Utility", "Ekko": "Assassin / Diver",
        "Akshan": "Marksman / Roam", "Jhin": "Utility / Sniper", "Jinx": "Hypercarry / Reset",
        "Vayne": "Hypercarry / Tank Buster",
        "Katarina": "Assassin / Reset", "Yasuo": "Skirmisher / Critical", "Tristana": "Hypercarry / Siege",
        "Diana": "Assassin / Diver",
        "Ahri": "Mage / Mobile", "Viego": "Skirmisher / Reset", "Mordekaiser": "Juggernaut / Magic",
        "LeBlanc": "Assassin / Mage",
        "Vel'Koz": "Poke / True Damage", "Lee Sin": "Playmaker / Skirmisher", "Trundle": "Splitpush / Duelist",
        "Veigar": "Scaling / Control Mage",
        "Twitch": "Hypercarry / Stealth", "Rakan": "Engage / Playmaker", "Master Yi": "Hypercarry / Skirmisher",
        "Karthus": "Power Farm / Mage",
        "Swain": "Sustain / Mage", "Caitlyn": "Sniper / Trap", "Poppy": "Tank / Disengage",
        "Lulu": "Enchanter / Protect",
        "Riven": "Skirmisher / Mobile", "Soraka": "Enchanter / Heal", "Vladimir": "Scaling / Sustain",
        "Zed": "Assassin / Shadow",
        "Fiddlesticks": "Mage / Ambush", "Seraphine": "Enchanter / Mage", "Vex": "Mage / Anti-Dash",
        "Varus": "Poke / Utility",
        "Aatrox": "Juggernaut / Drain", "Yone": "Skirmisher / Critical", "Thresh": "Engage / Playmaker",
        "Sion": "Tank / Splitpush",
        "Kayn": "Skirmisher / Assassin", "Jarvan IV": "Engage / Diver", "Naafiri": "Assassin / Pack",
        "Xerath": "Poke / Artillery",
        "Anivia": "Control / Zone", "Rell": "Engage / Tank", "Brand": "Mage / DoT", "Vi": "Diver / Lockdown",
        "Illaoi": "Juggernaut / Zone", "Orianna": "Control / Mage", "Kalista": "Kite / Rend",
        "Blitzcrank": "Hook / Burst",
        "Miss Fortune": "Bullet Hell / ADC", "Renekton": "Fighter / Lane Bully", "Ambessa": "Skirmisher / Mobility",
        "Jayce": "Poke / Form Switch",
        "Udyr": "Juggernaut / Stance", "Yuumi": "Enchanter / Untargetable", "Aurelion Sol": "Scaling / Mage",
        "Tryndamere": "Splitpush / Undying",
        "Syndra": "Burst / Control", "Quinn": "Roam / Marksman", "Braum": "Tank / Warden",
        "Nocturne": "Assassin / Global",
        "Sett": "Juggernaut / Haymaker", "Rengar": "Assassin / One-shot", "Karma": "Enchanter / Poke",
        "Samira": "Hypercarry / Combo",
        "Aphelios": "Hypercarry / Weapon Master", "Hwei": "Mage / Versatile", "Kled": "Skirmisher / Engage",
        "Garen": "Juggernaut / Execute",
        "Pyke": "Assassin / Support", "Kayle": "Scaling / Hypercarry", "Kha'Zix": "Assassin / Isolation",
        "Shyvana": "Juggernaut / Dragon",
        "Galio": "Tank / Magic Shield", "Gnar": "Transformation / Engage", "Milio": "Enchanter / Cleanse",
        "Malphite": "Tank / Engage",
        "Kog'Maw": "Hypercarry / Artillery", "Volibear": "Juggernaut / Diver", "Lillia": "Skirmisher / Speed",
        "Viktor": "Control / Scaling",
        "Gangplank": "Zone / Barrel", "Taric": "Enchanter / Invulnerability", "Skarner": "Tank / Suppress",
        "Smolder": "Scaling / ADC",
        "Urgot": "Juggernaut / Ranged", "Xin Zhao": "Diver / Duelist", "Neeko": "Mage / Trickster"
    }

    # Liste formatı: "İsim|Puan|Rol|Şampiyon"
    ham_veri = """Avalanche#TRdog|2136|Destek|Lux
marjua#merx|2121|Orman|Hecarim
mxch1n3#1790|1866|Destek|Janna
Ucka#God|1797|Nisanci (ADC)|Zeri
Leansy#TR2|1622|Nisanci (ADC)|Ezreal
Diluc#モラン|1620|Ust Koridor|Fiora
Clavar la Espada#5151|1608|Ust Koridor|Darius
sharingan eyez#333|1580|Nisanci (ADC)|Kai'Sa
ColdPalmer#TR2|1570|Nisanci (ADC)|Draven
ladriv#001|1565|Ust Koridor|Camille
selfmade#531|1539|Orman|Graves
forty seven#47X|1403|Orta Koridor|Akali
Wistaria#1107|1401|Ust Koridor|Fiora
mxcxhxx#xxx|1388|Orta Koridor|Talon
ash#lost|1387|Orman|Nidalee
괴수 8호#0930|1371|Orta Koridor|Fizz
Memories#TOKİO|1368|Orta Koridor|Qiyana
luciddrxam#xxxx|1325|Orta Koridor|Talon
Deniz#2025|1281|Nisanci (ADC)|Lucian
mpd n xtc#422mg|1276|Ust Koridor|Fiora
adeline#789|1239|Destek|Nami
Puca#ali|1237|Orman|Hecarim
Jaquen#TR2|1217|Orta Koridor|Kassadin
Reaix#00011|1209|Orta Koridor|Sylas
Pavard#666|1207|Ust Koridor|Kennen
ClutchNツ#0000|1207|Orta Koridor|Zoe
HIGAN 此岸#答えは沈黙|1202|Destek|Bard
Humble Zeref#1007|1200|Orman|Ekko
Alex Mercer#1v9|1179|Orta Koridor|Talon
Yavuzmacun#2412|1149|Orman|Graves
Violent#733|1139|Orta Koridor|Akshan
SONMENZİL#TR1|1120|Nisanci (ADC)|Jhin
Runa#emo|1108|Destek|Lux
ZOR YARIŞIRLAR#1818|1106|Nisanci (ADC)|Jinx
Yui#S0RA|1101|Nisanci (ADC)|Vayne
kanami#dream|1096|Destek|Lux
Vecta#0001|1088|Orta Koridor|Katarina
bok tv mensubu#messi|1083|Orta Koridor|Yasuo
kia sama#0843|1068|Nisanci (ADC)|Lucian
Eloha#111|1054|Nisanci (ADC)|Tristana
dueno#sxru|1044|Orman|Diana
Arvem#2407|1034|Destek|Lux
Apolyo#3672|1033|Orta Koridor|Ahri
gitme bebe#777|1033|Destek|Bard
Kira#sss1|1030|Orman|Viego
KOKO#DEG|1028|Ust Koridor|Mordekaiser
InsertIn#TR1|1022|Nisanci (ADC)|Ezreal
carnyx#4444|1021|Nisanci (ADC)|Jhin
Lotus#Nera|1017|Orta Koridor|LeBlanc
Old Faker#9102|1016|Destek|Vel'Koz
Uyuttuğum adama#VURMA|1016|Orta Koridor|Zoe
Solarcix#REAL|1015|Orman|Lee Sin
gerizekali mal#hzrn|1015|Orta Koridor|Qiyana
Diass#Aks|1011|Ust Koridor|Trundle
yy mb we 15#dlra|1010|Orman|Viego
mein kmpf#888|1006|Orta Koridor|Akali
itsdripbaby#111|1003|Nisanci (ADC)|Draven
Muteki#fool|997|Orta Koridor|Veigar
kaka kafa calimi#meto|996|Nisanci (ADC)|Twitch
Rakan God#Rakan|991|Destek|Rakan
why u mad#god|990|Orman|Master Yi
Coverit#TOXIC|984|Orman|Karthus
HÖÖÖÖÖÖÖÖÖÖÖÖ#Swain|973|Destek|Swain
Sw4q#1734|959|Nisanci (ADC)|Caitlyn
TEHLİKELİ KEDİ#Yavuz|955|Nisanci (ADC)|Caitlyn
ŞAMPİYONLUK 1 #TR1|951|Orman|Poppy
joji#XDD|946|Destek|Lulu
Dark Magician#19035|946|Orta Koridor|LeBlanc
dc gg pepeler#36963|945|Orta Koridor|Yasuo
SA BEN DOPA#21gr|942|Nisanci (ADC)|Vayne
woo walk#igris|941|Ust Koridor|Riven
Beni Şaşırttın#ˉˉˉ|939|Destek|Soraka
Sunless#暗い空|936|Orta Koridor|Vladimir
Swiislor#6292|935|Orta Koridor|Akshan
DİØ BRANDØ#TR1|935|Nisanci (ADC)|Kai'Sa
kick tireurennu#13xu|930|Orta Koridor|Zed
Lxnt#Bruh|930|Orman|Fiddlesticks
gadas#TR1|918|Ust Koridor|Camille
Drew#EUW2|917|Orta Koridor|Sylas
Catriona#diva|916|Destek|Seraphine
LOBBY ADMIN#XYZ|916|Orta Koridor|Talon
Aelisia#7777|912|Nisanci (ADC)|Vayne
Cıva#LoL|911|Ust Koridor|Mordekaiser
CT Siparus TNT#TR1|909|Nisanci (ADC)|Draven
Twtv PyrisTTT#123|908|Orta Koridor|Yasuo
suki#ad237|907|Nisanci (ADC)|Lucian
zorbadırgüzellik#11111|905|Orman|Lee Sin
THOMY#BIG|901|Orman|Diana
Clay#Peony|901|Ust Koridor|Fiora
Kings Never Die#769|899|Orta Koridor|Vex
k mid1#1111|891|Orta Koridor|LeBlanc
loath veiled ire#111|891|Orta Koridor|Katarina
lame en peine#0000|888|Nisanci (ADC)|Varus
kucuk kiz#ppi|887|Destek|Janna
yunik#00001|885|Ust Koridor|Aatrox
Spot#TR1|883|Orta Koridor|Yone
Luante#0000|883|Ust Koridor|Kennen
Vlessok#TR1|880|Nisanci (ADC)|Twitch
Thank you next#TR1|879|Orta Koridor|Qiyana
Goddess Wind#CAT|878|Orta Koridor|Yasuo
Snophén#Nami|877|Destek|Nami
ÇAPINIZ YETMEZ#7777|877|Nisanci (ADC)|Lucian
El Amarna#TR01|876|Destek|Soraka
wka#888ii|875|Orta Koridor|Katarina
Parlak Pasif#LGBT|872|Destek|Janna
FKKemikKıranFK#FKLLR|869|Orta Koridor|Sylas
Miyuk#RAMO|867|Orman|Bel'Veth
nightcore#clshr|867|Orta Koridor|Naafiri
Ata#369|865|Orman|Taliyah
Ygtrêce#TR1|865|Orman|Gragas
your goth soraka#sup|865|Destek|Soraka
Helvete#6ix|864|Nisanci (ADC)|Draven
daewi#nox|864|Orta Koridor|Katarina
Akûma Undomîell#QeQ|864|Orta Koridor|Katarina
zvxdcvbf#y5dgs|862|Orta Koridor|Talon
Naofumi lwatani#TR1|861|Destek|Leona
Kisuke#1v9Qi|855|Orta Koridor|Qiyana
очень темно#черны|855|Orta Koridor|Zed
Kick Qorath#40312|851|Orman|Rengar
a waltz for you#ˇˆˇ|849|Nisanci (ADC)|Tristana
sakasiz#saka|848|Ust Koridor|Irelia
maskelibalo1156#9797|847|Orman|Viego
kerimflex#000|847|Orta Koridor|Talon
Maple#JQKA|847|Orman|Rengar
mamisavage#xxxxx|847|Orta Koridor|Sylas
emolaf#111|845|Orta Koridor|Qiyana
Sangre#Aeon|845|Nisanci (ADC)|Vayne
aizel#999WN|845|Nisanci (ADC)|Draven
foe#foe1|843|Nisanci (ADC)|Draven
Foreflay#9999|843|Destek|Thresh
Siravia#diva|843|Nisanci (ADC)|Vayne
BeNTeK#YaTo|836|Ust Koridor|Sion
Şeftali#プディング|835|Destek|Lulu
i hate what i am#bloxa|834|Orman|Hecarim
qanaryq#TR1|833|Destek|Thresh
Uira#222|832|Orta Koridor|Ahri
Musthic#AKU|830|Orta Koridor|Ziggs
JerryRaynor#3536|828|Orman|Kayn
KING#CRUEL|828|Orman|Diana
renias#TR1|825|Nisanci (ADC)|Jhin
SOL BNB ADA BTC#rich|825|Orman|Jarvan IV
breakcore#clshr|825|Orta Koridor|Naafiri
yuıoy#TR1|820|Destek|Xerath
CİHAT SARSILMAZ#11111|819|Orman|Viego
Loki#0651|819|Ust Koridor|Darius
Kaharu#TR1|817|Orman|Kayn
on my own#1111|816|Nisanci (ADC)|Kai'Sa
Kuddusi Baba#GAİLE|815|Destek|Bard
Sıeáth#TR1|814|Orta Koridor|Yasuo
inside my heart#66666|814|Orta Koridor|Qiyana
Lady Arwen#Solvi|813|Orta Koridor|Anivia
Otenazy#TR068|813|Destek|Xerath
Rüzgar#rüz|813|Orta Koridor|Yasuo
PAIN TOLERANCE#1905|812|Nisanci (ADC)|Kai'Sa
Sypnax#999|811|Orta Koridor|LeBlanc
nerdaliisback#9108|810|Orman|Lee Sin
bluest flame#1204|810|Destek|Lux
Idk Complicated#jihun|809|Nisanci (ADC)|Aphelios
ÇiftçiBob#lol|806|Destek|Brand
Ohnakinong#TR1|805|Ust Koridor|Riven
smolpaweum#smlpw|804|Orman|Vi
Jaime Lannister#NOBLE|803|Orman|Viego
tears#369|803|Orta Koridor|Qiyana
Necrotyle#necro|803|Ust Koridor|Illaoi
deathcade#333|802|Nisanci (ADC)|Tristana
Atode#lord|800|Ust Koridor|Riven
Hustrucha#001|798|Nisanci (ADC)|Vayne
antichrist#733|798|Orman|Bel'Veth
dc gg rlp#Li123|797|Orta Koridor|Talon
Shape#epahs|797|Ust Koridor|Mordekaiser
Bukroshee#神です|795|Destek|Soraka
Yuisha#0229|794|Destek|Nami
Mirzâ#Siel|794|Nisanci (ADC)|Jhin
ryangosling#night|793|Nisanci (ADC)|Ezreal
hll#TR1|792|Orta Koridor|Orianna
Madé#drkn|791|Destek|Janna
Medwin#384|791|Nisanci (ADC)|Kalista
OGC Gloryiuz#3131|791|Destek|Blitzcrank
LXSING DREAMS#19323|789|Orman|Master Yi
Fifth Evangelist#JSB|789|Nisanci (ADC)|Miss Fortune
kaneki#wh1te|788|Orta Koridor|Yasuo
Kâim Bey#TR1|788|Orta Koridor|Anivia
DH Duellant#TR1|787|Ust Koridor|Renekton
pablosky#qss|787|Orman|Karthus
ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ#888|787|Ust Koridor|Ambessa
ata jungle#nvl|786|Orta Koridor|Talon
Rushh#TR1|786|Nisanci (ADC)|Vayne
paranoya#1006|786|Orta Koridor|Qiyana
cain#1912|786|Orta Koridor|Zed
JimiDede#TR1|785|Ust Koridor|Jayce
okkDislslt#123|784|Orta Koridor|Qiyana
god bless u#pump|782|Ust Koridor|Riven
Kind#HB1|782|Orman|Ekko
zwenix즈웨#sae|781|Nisanci (ADC)|Kai'Sa
sonsahabe3169#teala|781|Orman|Udyr
Lexter#0001|780|Destek|Thresh
Lion Media#88888|779|Orta Koridor|Sylas
NAMAZ KIL #TR1|778|Orman|Lee Sin
uzak dur#lllll|777|Nisanci (ADC)|Vayne
Qyzo#MICO|770|Nisanci (ADC)|Kai'Sa
Ridd#B11F|767|Nisanci (ADC)|Jinx
Equinox#Asol|765|Orta Koridor|Aurelion Sol
Kinetsu#Sooth|764|Ust Koridor|Riven
edru#soe|763|Orta Koridor|Vladimir
call me boss#TBMM|763|Ust Koridor|Tryndamere
good for you#404|762|Destek|Yuumi
Sakin#WOW|760|Orta Koridor|Kassadin
çökelek holding#xDDDD|758|Orta Koridor|Zed
wrath#303|757|Ust Koridor|Mordekaiser
issey miyake#3446|756|Nisanci (ADC)|Lucian
Moon#711|756|Orta Koridor|Syndra
Jardel#1283|753|Orta Koridor|Vladimir
KZN Miraj#Birci|753|Ust Koridor|Ornn
Beloved Husky#TR1|750|Ust Koridor|Gwen
Dragut#p4u|744|Orta Koridor|Hwei
SenTELLo Şamil#TR1|744|Orman|Zac
Dr Sabine#TR1|738|Nisanci (ADC)|Vayne
The Rheronis#TR1|735|Ust Koridor|Shen
Despair#1881|733|Orman|Diana
Reqsa#Rank1|731|Orman|Kayn
Whip#111|725|Orman|Evelynn
Odoridase#123|721|Orta Koridor|Yasuo
Majo莲花#血雨探花|721|Ust Koridor|Rumble
Neo irfunny baby#TR3|719|Orman|Taliyah
IXIecutioner#Emre|717|Orman|Ekko
Sunny IV#TR1|715|Orta Koridor|Zoe
ZAFER TÜRİZM#Hsthg|715|Orman|Diana
surf#3290|714|Ust Koridor|Tryndamere
angelic#lure|712|Destek|Lux
sunhaki#274x|712|Orta Koridor|Vladimir
自分を憎む#999|708|Orta Koridor|Yasuo
İçinde Gezdiren#YUMOŞ|707|Destek|Yuumi
BestrafeMich#Recht|706|Nisanci (ADC)|Jinx
debronee#888|704|Orta Koridor|Katarina
Calámity#asf|704|Orta Koridor|Zed
kid a mnesia#null|703|Orta Koridor|Ahri
Ryu#もう一つ|702|Ust Koridor|Fiora
Lynn#7770|697|Orman|Viego
hilal yelekci#9595|692|Ust Koridor|Camille
Scorth#2906|691|Nisanci (ADC)|Kai'Sa
KAJUN LORDU#CAJUN|690|Orman|Rek'Sai
MF ÁweShøck#sage|689|Nisanci (ADC)|Miss Fortune
Emilia LeBlanc#argnt|683|Orta Koridor|LeBlanc
SuspectB#3162|682|Destek|Blitzcrank
old but gold#007|680|Nisanci (ADC)|Caitlyn
Sakin Kal Arda#12345|678|Orta Koridor|Syndra
AlwaysandForever#alwys|677|Ust Koridor|Quinn
iLLeqaLFaTaL1Ty#TR1|677|Orta Koridor|Zed
beauty in your#eyess|674|Destek|Braum
VEST#vest7|673|Orman|Nocturne
45 cm biceps#Lym|672|Orman|Viego
Luxtly#Kaisa|672|Nisanci (ADC)|Kai'Sa
valeria#baby|669|Destek|Lulu
levila#tr2|666|Ust Koridor|Sett
TrueAlpha Rengar#Alpha|664|Orman|Rengar
Fasulyesineee#1507|664|Orta Koridor|Yasuo
groza#221|664|Orta Koridor|Qiyana
Schurrle#CAMLC|660|Destek|Karma
tsuki akari#7778|658|Orta Koridor|Syndra
Alwaysboredlol#TR1|657|Nisanci (ADC)|Samira
BİLLURLU OYUNCU#TR1|657|Destek|Nami
Katatonia#555|656|Nisanci (ADC)|Aphelios
Maggie Rhee#0602|655|Destek|Lux
yoruldum#4080|654|Orta Koridor|Sylas
LEZBİYEN MURAT#TR1|651|Orta Koridor|Hwei
lost you#ash|651|Orta Koridor|Yasuo
khaelth#ffs|650|Destek|Lulu
kirmizi recete#361|649|Ust Koridor|Irelia
PSYCH0K1LL3R#333|648|Nisanci (ADC)|Xayah
ğğğğğğğğğğğğğğğğ#üüüüü|647|Nisanci (ADC)|Ezreal
kicktv lawilol#lwi|646|Orman|Lee Sin
Beeevt#3131|646|Ust Koridor|Kled
KALOBITAR FUN R1#MADEN|645|Ust Koridor|Garen
Exymian#TR1|644|Destek|Thresh
Herif#1100|641|Orta Koridor|Zed
ozzy#rog|641|Nisanci (ADC)|Samira
Monerâ#Tr61|640|Destek|Thresh
Coursin#TR1|640|Destek|Pyke
Mahatma LeKLa#reng|639|Orman|Rengar
değiştim#00000|634|Orta Koridor|Sylas
serikatil#ttt|634|Destek|Rakan
StaB#31sj|634|Ust Koridor|Kayle
PİDE#PİG|632|Ust Koridor|Renekton
800kMidSallll#TR1|632|Orta Koridor|Yasuo
Zeta#963|632|Orman|Nidalee
FL LookLikeGod#DOES|627|Orman|Kha'Zix
Elandel#TR1|626|Orman|Graves
beztebya888#4545|621|Orta Koridor|Galio
AmeIia#TR1|621|Orman|Shyvana
Xedz#TR1|619|Orta Koridor|Zed
SoothSayer35#EUW|618|Ust Koridor|Riven
Pegassuss#TR1|617|Orta Koridor|Zed
darkse1d#00000|616|Orta Koridor|Akshan
Muhammekaiser#TR571|615|Ust Koridor|Mordekaiser
Estorea#TR1|614|Destek|Lux
inco#exo|614|Orman|Ekko
GLOXINIA SAMA#242|614|Ust Koridor|Jayce
The Salvatore#099|613|Nisanci (ADC)|Lucian
Lulugs#5601|613|Orta Koridor|Corki
dolleyicikıral2#s1k3r|612|Destek|Janna
Muteki#RK7|612|Orta Koridor|Veigar
seco#1111|611|Nisanci (ADC)|Jinx
杀手1#coc|610|Orta Koridor|Talon
Conqueror#Roseツ|609|Nisanci (ADC)|Draven
arcarcarcarc#0808|609|Orman|Hecarim
aden7#zxc|607|Nisanci (ADC)|Kai'Sa
sun eater#TR2|606|Nisanci (ADC)|Twitch
Risphaze#GOD|605|Orman|Hecarim
DOBRAFAZA#4666|604|Orman|Karthus
DΞSTΛN#TR35|603|Nisanci (ADC)|Samira
Nomad#gdxer|598|Ust Koridor|Darius
uA VictorOsimhen#GS1|598|Ust Koridor|Malphite
六六六六六六六#kog|598|Nisanci (ADC)|Kog'Maw
Kaann#3636|597|Orta Koridor|Anivia
MrNowan#BABY|596|Ust Koridor|Gnar
Turk1shStars#3060|595|Orta Koridor|Yasuo
TARANTUNA#3169|594|Destek|Milio
emınem#3162|594|Orman|Taliyah
Eda Clawthorne#1104|592|Destek|Lux
195CM107KG21CM#TC1|589|Ust Koridor|Rumble
1LVLTOCHALLENGER#TR007|587|Orta Koridor|Katarina
MuhakemeYeteneği#TR1|586|Orta Koridor|Fizz
Godfrey#ŞAŞKN|586|Ust Koridor|Sett
Enama#Mad|585|Nisanci (ADC)|Lucian
dqp#lol|584|Ust Koridor|Tryndamere
KGB M A R S#1453|583|Orta Koridor|Zed
asdfqwrdsfgqwe#qweqw|583|Orta Koridor|Qiyana
mirina#mel|582|Orta Koridor|Katarina
End Of Life EO#TR1|581|Nisanci (ADC)|Samira
Shinya#666|578|Destek|Janna
LonelyWolf123#TR1|577|Orta Koridor|Talon
manifest1#999|576|Nisanci (ADC)|Xayah
MertcanKeskin#TR1|575|Ust Koridor|Aatrox
Yasena#TR1|574|Destek|Rakan
lil peep turkiye#622|574|Destek|Janna
Pompacı Ediz#Ediz|573|Nisanci (ADC)|Nilah
Fhype#TR1|571|Orta Koridor|Yasuo
elonda dans#q77|570|Nisanci (ADC)|Samira
Nista#VFW|568|Ust Koridor|Kled
aspect#lowke|568|Orta Koridor|Talon
Floodchuk#Ryze|567|Orta Koridor|Ryze
Kengu#TR1|566|Orta Koridor|Vladimir
Gesshoku#tsukı|565|Orta Koridor|Yasuo
Rhioni1#TR1|563|Nisanci (ADC)|Lucian
Carryrina#TR1|563|Orta Koridor|Katarina
twc smrfng1#twc|563|Orta Koridor|Neeko
Afiel#TR1|563|Ust Koridor|Irelia
Bir Yıldız Kaisa#3131|560|Nisanci (ADC)|Kai'Sa
Onsra#0104|560|Orta Koridor|Zed
draconian#death|559|Destek|Lux
Myst#TR2|557|Orta Koridor|LeBlanc
Cikey#TR1|556|Orman|Volibear
yolu yok#dxmn|556|Orta Koridor|Sylas
Starlight#EUWS|555|Orman|Volibear
nicole#十十十|553|Destek|Seraphine
casual#ties|552|Orman|Bel'Veth
Ðiø Ðella Førest#TR1|551|Orman|Lillia
Eilish#Doll|550|Nisanci (ADC)|Jhin
SARHOŞ OBEZ#2008|548|Orman|Gragas
highasf#愛愛愛|548|Orta Koridor|Talon
Aqua#lumi|546|Destek|Lulu
Relax Darling#3344|546|Orta Koridor|Katarina
Aphelios v2#Aphe|545|Nisanci (ADC)|Aphelios
Frieren#Staff|543|Orman|Diana
Stnbl#TR1|542|Orta Koridor|Yasuo
ŞAHBET#ŞAHBO|542|Nisanci (ADC)|Vayne
creaox#acc1|541|Nisanci (ADC)|Kai'Sa
Rillyeith#TR1|538|Ust Koridor|Sion
ZehriMar BIG#HYPE|538|Orta Koridor|Zed
Istag#88888|536|Orta Koridor|Yasuo
yulina#808|535|Destek|Nami
Playboi Carti#yvI|534|Nisanci (ADC)|Kai'Sa
tune#roe|533|Destek|Lux
ANKA#boks|532|Orman|Gragas
Neo ZeTHRIV#TR1|532|Orman|Gragas
Memur 1#GMO|531|Nisanci (ADC)|Vayne
JadeRoc#KÜRDO|529|Destek|Thresh
GodLikeFriqher#grind|529|Orta Koridor|Vladimir
hindsight#171|528|Nisanci (ADC)|Zeri
Sick#911|528|Orta Koridor|Zed
Through Shadows#TR1|528|Orta Koridor|Zed
Zetinac#000|528|Orta Koridor|Akali
sek1m#king|527|Nisanci (ADC)|Lucian
Kim Chaewon#Kibir|525|Ust Koridor|Aatrox
xxxva#1938|524|Nisanci (ADC)|Kai'Sa
BakireGül#Nurdi|523|Destek|Lux
Taso BABA#LMFAO|522|Orman|Diana
Zyr Bahçeleri#TR1|522|Destek|Rell
Kendıne Gwen#TR1|521|Orta Koridor|Azir
DredRS#TR1|520|Orta Koridor|Katarina
Kounen#chaos|518|Orman|Kayn
katana#xxd|515|Orta Koridor|Yone
Shigaraki#MRT|515|Orta Koridor|Cassiopeia
Zievel#zort|513|Orman|Diana
Renegoush#TR1|511|Destek|Swain
hamburgersewerim#444|510|Orman|Kha'Zix
DikDuranPisVuran#3733|508|Ust Koridor|Camille
sonumu getir#212|508|Ust Koridor|Jax
FreshKiller#GOD|507|Nisanci (ADC)|Caitlyn
THE MACHİNE#6886|507|Orman|Evelynn
Rodblac#Ghost|506|Destek|Xerath
Solded#SLDED|506|Orman|Bel'Veth
Byleth#999|505|Nisanci (ADC)|Tristana
Challenger Bot#TR2|505|Nisanci (ADC)|Vayne
devilish#1000|503|Orta Koridor|Zed
BabyClassQ#TR1|503|Nisanci (ADC)|Samira
Slimeslimeoglu#TR31|502|Ust Koridor|Garen
CHA OLUP SALICAM#Tedi|501|Orman|Kayn
Fawklê#TR1|501|Nisanci (ADC)|Zeri
i will cherish u#4GET十|500|Orta Koridor|Qiyana
Khaslana#Kaos|500|Ust Koridor|Riven
KIKA#Now|500|Destek|Lux
mystique#xxxxx|500|Orman|Graves
young lust#666|499|Destek|Soraka
Şafi in İsrael#Şafi|499|Destek|Vel'Koz
honor fizz#TR1|499|Orta Koridor|Fizz
eng50DOM6Ps2p60#engel|499|Orta Koridor|Qiyana
ALPERN NAPIYOSON#ADC|496|Nisanci (ADC)|Kai'Sa
heeeey guuys#fbgn|494|Orta Koridor|Katarina
Çekirdek#テオビ|494|Destek|Soraka
NICK WOLTEMADE#DRAKE|493|Orta Koridor|Yasuo
Desir Hermann#4810|493|Orta Koridor|Annie
EzVayneQQ#TR1|492|Ust Koridor|Fiora
ceku#baIim|491|Destek|Janna
Holløw#TR1|491|Destek|Nami
Boss429#006|489|Destek|Karma
let me handle#8390|488|Destek|Thresh
Ballıca Teksas#15ff|488|Orman|Gragas
sergio ramos#93RMA|487|Orta Koridor|Yasuo
Rug Seller#TR1|486|Destek|Tahm Kench
MEĞZAME#TR1|486|Ust Koridor|Camille
FUСΚYOULIKEIСAN#asf|486|Orman|Kindred
odium#numen|485|Destek|Soraka
Bahçevelli#1010|484|Orta Koridor|Zoe
Seymix#993|483|Orta Koridor|Yasuo
IIIIIIllIIll#llIII|483|Ust Koridor|Nasus
Eternal Wild#TR1|482|Ust Koridor|Nasus
Ladyboy Ahmet#1903|482|Destek|Karma
탑 코리도 킹#1901|480|Orta Koridor|Vladimir
09 01 2010#026|480|Orman|Master Yi
6KaraKoyun#Koyun|480|Orta Koridor|Katarina
pozitifim#0005|480|Orman|Bel'Veth
K1NG DOĞUKAN#TR1|479|Nisanci (ADC)|Kai'Sa
cube sheker#TR12|479|Orman|Nidalee
Ekkota#mami|478|Orman|Ekko
D0KI#TR61|478|Ust Koridor|Riven
BAMBOLEO#TR31|477|Orta Koridor|Viktor
valentina#fae|477|Destek|Janna
mental breakdown#iron4|477|Ust Koridor|Fiora
Bishu#TR1|475|Orta Koridor|Vladimir
Ettelly#TR1|475|Ust Koridor|Irelia
sophie germain#1111|474|Destek|Janna
Bounifiort#TR1|474|Orta Koridor|Anivia
EX7#3783|474|Orta Koridor|Zed
ByPeJuRa#KGT|473|Nisanci (ADC)|Kai'Sa
AGoNY#HLE|472|Destek|Rell
Chemistries#TR1|472|Orta Koridor|Anivia
stfu and play#anann|472|Orta Koridor|Katarina
DIZØKILL#TR1|472|Orman|Viego
dobro vecer#zephx|471|Destek|Lulu
batu123#jgdif|471|Orta Koridor|Yasuo
DULTÜCCARI#NGC|471|Destek|Soraka
081096251199#0802|471|Orta Koridor|Yasuo
TARDE SETT TUTE#BOSS|470|Ust Koridor|Sett
ELAK#XXXXX|470|Orta Koridor|Galio
ManyaqBoy#TR31|470|Orta Koridor|Yasuo
Öykie#Lady|469|Orta Koridor|Ahri
Dieruth#1907|465|Nisanci (ADC)|Jinx
Bück Dîch#1310|464|Ust Koridor|Darius
NEEKO TANRISI#GOD|464|Orta Koridor|Neeko
Area T Rex#0305|463|Destek|Lux
Jackz#TR1|463|Ust Koridor|Gangplank
beypazari iceyim#neyse|463|Destek|Thresh
C O N Q U E S T#1788|463|Orman|Kha'Zix
öldühttp#kimya|461|Orta Koridor|Aurora
gemici#370|461|Destek|Taric
Tyurvalembas#3152|460|Orman|Skarner
EDG wx 3334532#xxx|459|Orta Koridor|Sylas
Shasho#4444|459|Nisanci (ADC)|Jhin
Tekin#000|459|Nisanci (ADC)|Xayah
ｙｏｒｉｃｈｉ#11111|458|Destek|Lulu
TWKING#619|458|Nisanci (ADC)|Twitch
Lesi0n#TR1|458|Nisanci (ADC)|Smolder
KeyBlade#KUN|458|Orta Koridor|Yasuo
lower your head#DDD|457|Orta Koridor|Sylas
Canay#TR1|455|Ust Koridor|Urgot
Pain#Kayn|454|Orman|Kayn
olek#31sa|453|Nisanci (ADC)|Jhin
ozzykaratren#1907|453|Nisanci (ADC)|Kalista
TÜRBANLI DAMITAN#3162|453|Nisanci (ADC)|Aphelios
Sativa#7080|451|Nisanci (ADC)|Twitch
MRJack#388|451|Orta Koridor|Zed
Mâây#888ii|449|Destek|Lux
arzhel#green|448|Destek|Lux
deepinlovekathie#707|447|Orman|Xin Zhao
Russell Adler#İblis|446|Orman|Nocturne
Miyuna#sago|446|Nisanci (ADC)|Kai'Sa
JackalShow#TR1|445|Nisanci (ADC)|Vayne
Sihirdar Adım#TR2|444|Ust Koridor|Fiora
Code Lyoko#2010|441|Orta Koridor|Aurelion Sol"""

    # Verileri yaz
    with open("sıralama.txt", "w", encoding="utf-8") as f:
        # Satırları böl
        lines = ham_veri.strip().split("\n")

        for line in lines:
            if not line.strip(): continue
            parts = line.split("|")

            if len(parts) >= 4:
                ad = parts[0].strip()
                puan = parts[1].strip()
                rol = parts[2].strip()  # DÜZELTİLDİ: Artık doğru indekste
                sampiyon = parts[3].strip()  # DÜZELTİLDİ: Artık doğru indekste

                # Özellik bul
                ozellik = trait_map.get(sampiyon, f"Main: {sampiyon}")

                # CSV Formatında yaz
                f.write(f"{ad}, {puan}, {rol}, {ozellik}\n")

    print(f"[BAŞARILI] {len(lines)} oyuncu 'sıralama.txt' dosyasına DOĞRU formatta kaydedildi!")
    print("Ana oyunu tekrar çalıştırabilirsin.")


if __name__ == "__main__":
    verileri_onar()