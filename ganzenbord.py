# ======================================

# GANZENBORD - DIEREN EDITIE

# ======================================

# Gemaakt door: [Nizar Almasri en Nassim Mounahou]

#

# Spelregels:

# - Kat verslaat Muis

# - Muis verslaat Hond

# - Hond verslaat Kat



# Uitleg:

# 1. Kies een dier met toets 1 (Kat), 2 (Hond) of 3 (Muis).

# 2. Druk op SPATIE om te gooien met twee dobbelstenen.

# 3. De pion beweegt over 63 vakjes.

# 4. Als twee dieren op hetzelfde vak staan, is er een gevecht.

#    De verliezer gaat terug naar start (vak 0).

# 5. De winnaar van een gevecht krijgt +1 punt.

# 6. Wie het laatste vak bereikt krijgt +5 punten en wint het spel.

# 7. Druk op BACKSPACE om opnieuw te beginnen.

# ======================================

import pygame

import random

# -------------------------------

# PYGAME INSTELLINGEN

# -------------------------------

pygame.init()

scherm_breedte, scherm_hoogte = 1024, 760

scherm = pygame.display.set_mode((scherm_breedte, scherm_hoogte))

pygame.display.set_caption("Ganzenbord - Dieren Editie (63 vakjes)")

klok = pygame.time.Clock()

kleine_tekst = pygame.font.Font(None, 28)

grote_tekst = pygame.font.Font(None, 40)

# -------------------------------

# SPELVARIABELEN

# -------------------------------
bord_afbeelding = pygame.image.load("Ganzenbord12.png")

bord_vakken = [

    [160, 683], [286, 683], [356, 683], [415, 683], [482, 683], [545, 683],

    [618, 683], [692, 683], [758, 683], [828, 643], [895, 598], [937, 549],

    [965, 489], [982, 430], [982, 353], [968, 283], [944, 220], [905, 167],

    [833, 111], [744, 66], [664, 62], [597, 62], [536, 62], [464, 62],

    [398, 62], [335, 62], [265, 66], [198, 94], [142, 129], [104, 174],

    [83, 227], [65, 283], [65, 367], [83, 435], [116, 491], [160, 535],

    [216, 570], [282, 587], [342, 587], [405, 587], [468, 587], [536, 587],

    [615, 587], [692, 587], [755, 578], [816, 528], [863, 458], [877, 402],

    [874, 335], [856, 283], [804, 202], [737, 160], [632, 157], [545, 157],

    [468, 157], [394, 157], [328, 157], [265, 167], [195, 223], [167, 325],

    [188, 403], [221, 454], [282, 482], [413, 456]

]

aantal_vakken = len(bord_vakken)

dieren_namen = ["Kat", "Hond", "Muis"]

dieren_kleuren = [ROOD, BLAUW, GROEN]

dieren_posities = [0, 0, 0]

dieren_scores = {"Kat": 0, "Hond": 0, "Muis": 0}

huidige_speler = 0

laatste_worp = 0

spel_winnaar = None

bericht = ""

gekozen_dier = None

verslaat = {

    "Kat": "Muis",

    "Muis": "Hond",

    "Hond": "Kat"

}

# -------------------------------

# FUNCTIES

# -------------------------------

def bepaal_gevecht_winnaar(dier1, dier2):

    """Bepaalt de winnaar tussen twee dieren."""

    if dier1 == dier2:

        return None

    if verslaat[dier1] == dier2:

        return dier1

    else:

        return dier2

def volgende_beurt(speler_nummer):

    """Geeft de volgende speler aan de beurt."""

    return (speler_nummer + 1) % 3

def verplaats_pion(speler_nummer, aantal_stappen):

    """Verplaatst een dier vooruit over het bord."""

    dieren_posities[speler_nummer] += aantal_stappen

    if dieren_posities[speler_nummer] >= aantal_vakken - 1:

        dieren_posities[speler_nummer] = aantal_vakken - 1

        return True

    return False

def controleer_gevechten():

    """Controleert of dieren op hetzelfde vak staan en verwerkt gevechten."""

    global bericht

    bericht = ""

    vak_bezetting = {}

    for speler_index, positie in enumerate(dieren_posities):

        vak_bezetting.setdefault(positie, []).append(speler_index)

    for positie, spelers_op_vak in vak_bezetting.items():

        if len(spelers_op_vak) > 1:

            for i in range(len(spelers_op_vak)):

                for j in range(i + 1, len(spelers_op_vak)):

                    speler1 = spelers_op_vak[i]

                    speler2 = spelers_op_vak[j]

                    dier1 = dieren_namen[speler1]

                    dier2 = dieren_namen[speler2]

                    winnaar_dier = bepaal_gevecht_winnaar(dier1, dier2)

                    if winnaar_dier is None:

                        continue

                    if winnaar_dier == dier1:

                        verliezer_index = speler2

                    else:

                        verliezer_index = speler1

                    dieren_scores[winnaar_dier] += 1

                    dieren_posities[verliezer_index] = 0

                    bericht = f"{winnaar_dier} wint van {dieren_namen[verliezer_index]}."

def teken_scherm():

    """Teken het spelbord, de pionnen, tekst en scores."""

    scherm.fill(WIT)

    vak_kleuren = [GRIJS, GEEL, BRUIN, (180, 220, 255), (210, 255, 210)]

    for index, (vak_x, vak_y) in enumerate(bord_vakken):

        kleur = vak_kleuren[index % len(vak_kleuren)]

        pygame.draw.rect(scherm, kleur, (vak_x - 28, vak_y - 28, 56, 56))

        pygame.draw.rect(scherm, ZWART, (vak_x - 28, vak_y - 28, 56, 56), 2)

        tekst_op_vak = kleine_tekst.render(str(index), True, ZWART)

        scherm.blit(tekst_op_vak, (vak_x - 10, vak_y - 10))

    verschuivingen = [(-12, 0), (12, 0), (0, -18)]

    for index in range(len(dieren_posities)):

        positie_index = dieren_posities[index]

        vak_x, vak_y = bord_vakken[positie_index]

        verschuiving_x, verschuiving_y = verschuivingen[index % len(verschuivingen)]

        pygame.draw.circle(scherm, dieren_kleuren[index], (vak_x + verschuiving_x, vak_y + verschuiving_y), 18)

        naam_van_dier = kleine_tekst.render(dieren_namen[index], True, ZWART)

        scherm.blit(naam_van_dier, (vak_x + verschuiving_x - 22, vak_y + verschuiving_y - 34))

    regels_tekst = [

        "Regels: Kat > Muis, Muis > Hond, Hond > Kat",

        f"Gekozen dier: {gekozen_dier if gekozen_dier else 'Nog geen keuze (1/2/3)'}"

    ]

    for i, tekst in enumerate(regels_tekst):

        tekst_render = kleine_tekst.render(tekst, True, ZWART)

        scherm.blit(tekst_render, (20, 20 + i * 22))

    if spel_winnaar is None:

        beurt_tekst = grote_tekst.render(f"Beurt van: {dieren_namen[huidige_speler]}", True, ZWART)

        scherm.blit(beurt_tekst, (20, 620))

        uitleg_tekst = kleine_tekst.render("SPATIE = gooien, BACKSPACE = nieuw spel", True, ZWART)

        scherm.blit(uitleg_tekst, (20, 660))

    else:

        winnaar_tekst = grote_tekst.render(f"{spel_winnaar} heeft gewonnen (+5 punten).", True, ZWART)

        scherm.blit(winnaar_tekst, (20, 620))

        opnieuw_tekst = kleine_tekst.render("Druk op BACKSPACE om opnieuw te beginnen.", True, ZWART)

        scherm.blit(opnieuw_tekst, (20, 660))

    if laatste_worp:

        worp_tekst = kleine_tekst.render(f"Laatste worp: {laatste_worp} ogen", True, ZWART)

        scherm.blit(worp_tekst, (400, 620))

    if bericht:

        gevecht_tekst = kleine_tekst.render(bericht, True, (120, 0, 0))

        scherm.blit(gevecht_tekst, (400, 650))

    score_regels = [

        "SCORES:",

        f"Kat: {dieren_scores['Kat']}",

        f"Hond: {dieren_scores['Hond']}",

        f"Muis: {dieren_scores['Muis']}"

    ]

    for i, regel in enumerate(score_regels):

        regel_tekst = kleine_tekst.render(regel, True, ZWART)

        scherm.blit(regel_tekst, (820, 20 + i * 24))

    pygame.display.flip()

def kies_dier():

    """Toont een scherm waar de speler een dier kan kiezen."""

    global gekozen_dier

    kiezen = True

    while kiezen:

        scherm.fill(WIT)

        titel = grote_tekst.render("Kies je dier (1, 2 of 3):", True, ZWART)

        scherm.blit(titel, (300, 120))

        for i, dier in enumerate(dieren_namen):

            optie = grote_tekst.render(f"{i+1}. {dier}", True, dieren_kleuren[i])

            scherm.blit(optie, (380, 220 + i * 70))

        uitleg = kleine_tekst.render("1 = Kat, 2 = Hond, 3 = Muis. ESC = stoppen.", True, ZWART)

        scherm.blit(uitleg, (250, 540))

        pygame.display.flip()

        for gebeurtenis in pygame.event.get():

            if gebeurtenis.type == pygame.QUIT:

                pygame.quit()

                exit()

            if gebeurtenis.type == pygame.KEYDOWN:

                if gebeurtenis.key == pygame.K_1:

                    gekozen_dier = "Kat"

                    kiezen = False

                elif gebeurtenis.key == pygame.K_2:

                    gekozen_dier = "Hond"

                    kiezen = False

                elif gebeurtenis.key == pygame.K_3:

                    gekozen_dier = "Muis"

                    kiezen = False

                elif gebeurtenis.key == pygame.K_ESCAPE:

                    pygame.quit()

                    exit()

# Start met kiezen van een dier

kies_dier()

# -------------------------------

# HOOFDLUS VAN HET SPEL

# -------------------------------

spel_is_bezig = True

frames_per_seconde = 10

while spel_is_bezig:

    for gebeurtenis in pygame.event.get():

        if gebeurtenis.type == pygame.QUIT:

            spel_is_bezig = False

        if gebeurtenis.type == pygame.KEYDOWN:

            if gebeurtenis.key == pygame.K_BACKSPACE:

                dieren_posities = [0, 0, 0]

                huidige_speler = 0

                laatste_worp = 0

                spel_winnaar = None

                bericht = ""

            if gebeurtenis.key == pygame.K_SPACE and spel_winnaar is None:

                dobbelsteen_1 = random.randint(1, 6)

                dobbelsteen_2 = random.randint(1, 6)

                laatste_worp = dobbelsteen_1 + dobbelsteen_2

                bericht = f"{dieren_namen[huidige_speler]} gooit {dobbelsteen_1} en {dobbelsteen_2}."

                gewonnen = verplaats_pion(huidige_speler, laatste_worp)

                controleer_gevechten()

                if gewonnen:

                    spel_winnaar = dieren_namen[huidige_speler]

                    dieren_scores[spel_winnaar] += 5

                    bericht = f"{spel_winnaar} heeft het eindvak bereikt en wint."

                else:

                    huidige_speler = volgende_beurt(huidige_speler)

    teken_scherm()

    klok.tick(frames_per_seconde)

pygame.quit()
