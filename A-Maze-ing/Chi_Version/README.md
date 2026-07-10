# A-Maze-ing

Maze generator in Python: perfecte mazes (één pad) of "Pac-Man"-mazes
(volledig verbonden, met lussen) op basis van een configuratiebestand.

## Gebruik

```
python3 a_maze_ing.py config.txt
```

`config.txt` is een voorbeeldconfiguratie (mag ook een andere naam/pad zijn).

## Configuratiebestand

Verplichte sleutels (`KEY=VALUE`, regels met `#` zijn commentaar):

| Key           | Betekenis                     | Voorbeeld           |
|---------------|--------------------------------|----------------------|
| WIDTH         | Breedte van de maze (cellen)  | `WIDTH=20`           |
| HEIGHT        | Hoogte van de maze            | `HEIGHT=15`          |
| ENTRY         | Ingang (x,y)                  | `ENTRY=0,0`          |
| EXIT          | Uitgang (x,y)                 | `EXIT=19,14`         |
| OUTPUT_FILE   | Naam van het uitvoerbestand    | `OUTPUT_FILE=maze.txt` |
| PERFECT       | Perfecte maze (True/False)     | `PERFECT=True`       |

Optioneel: `SEED=<int>` voor reproduceerbaarheid (anders wordt een
willekeurige seed gekozen en getoond op het scherm).

## Structuur (herbruikbare bibliotheek)

```
a_maze_ing.py        - CLI entry point + interactief menu
maze/
    config.py         - inlezen/valideren configuratiebestand
    grid.py            - Maze klasse, wand-bitmasks (N=1,E=2,S=4,W=8)
    pattern42.py       - genereert het verplichte "42"-patroon
    generator.py       - generatie-algoritmes (perfect + Pac-Man varianten)
    solver.py          - BFS kortste pad
    writer.py          - schrijft het output-bestand in het gevraagde formaat
    renderer.py        - ASCII-weergave met kleuren
```

De generatielogica in `maze/` heeft geen afhankelijkheid van de CLI en kan
dus los hergebruikt worden (bv. door een ander script of door tests).

## Output-formaat

Eén hexadecimaal cijfer per cel (bit0=Noord, bit1=Oost, bit2=Zuid, bit3=West;
1 = gesloten wand), rij per rij. Na een lege regel volgen: entry-coördinaten,
exit-coördinaten en het kortste pad als lettersequentie (N/E/S/W).

## Interactief menu (na generatie)

- `r` — nieuwe maze genereren (nieuwe seed) en tonen
- `p` — oplossingspad tonen/verbergen
- `c` — kleur van de wanden wijzigen
- `q` — stoppen

## Wat is (bewust) een vereenvoudigde aanpak

Dit is een volledig werkende basisimplementatie die alle verplichte eisen
dekt en op 40 automatische testgevallen (verschillende seeds, beide modi)
slaagt voor: coherentie van gedeelde wanden, volledige connectiviteit, geen
open vlaktes groter dan 2x2 cellen, open hoeken/midden, en minstens één
geldig pad. De heuristieken voor lussen en het minimaliseren van dead-ends
in de Pac-Man-modus zijn met opzet eenvoudig gehouden (willekeurige
kandidaat-wanden met controle achteraf) — voor zeer kleine of ongebruikelijke
afmetingen kan het de moeite waard zijn de constanten in
`generator.py` (`target_loops`, `tolerance`) bij te stellen.
