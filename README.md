# Výzkumný úkol

## Plán:
- ~~Opravit gradientní mapy -- zeptat se jestli můžu použít knihovnu / dát dohromady bez knihovny~~
- ~~Dopsat kapitolu Návrh~~
- Doplnit do návrhu šanci / skill
- ~~Sepsat implementaci generování mapy~~
    - Doplnit použité technologie
- Podívat se na Monte Carlo (skripta: ZALG; Monte Carlo)
- ~~Rozmyslet co a jak budu implementovat~~
- Kapitola Mechaniky
    - Jednotky
        - Pohyb po mapě
        - Vyhledávání cílů v dosahu
        - Boj (útok a obrana)
    - Budovy
        - Generování surovin na konci kola
    - Hráč
        - Správa surovin (přidávání, odebírání)
        - Zpracování údržby jednotek (cena za kolo)
        - Evidence vlastněných jednotek a budov
    - Herní kolo
        - Střídání aktuálního hráče
        - Průběh tahu hráče
        - Verbování jednotek
        - Stavba budov
        - Produkcesurovin z budov
        - Zpracování údržby jednotek
- Kapitola Simulace

## 28.3.
### Uděláno:
- Kapitola implementace generování herního pole
- Hrubá osnova implementace herních mechanik a simulace
- Prototyp implementace pohybu
- Prototyp implementace boje


## 14.3.
### Uděláno:
- Podkapitola Akce
- Opravené gradientní generování
- Podkapitola Pravidla
- Kapitolu návrh už jen zkontrolovat gramaticky a zformátovat.
### Dotazy:
- Má smysl přpisovat shrnutí, nebo závěr kapitoly Návrh?
- Přeskládání kapitol. Může být Teorie; Implementace; Teorie; Implementace?

## 25.2.
### Uděláno:
- Podkapitola Objekty
- Podkapitola Akce -- teoretická část

## 10.02.
### Uděláno:
- Program:
    - náhodně generovaná výšková mapa
    - Interpolovaná výšková mapa
        - Menší náhodná mapa aplikovaná na větší mezeri interpolované
    - Gradientní výšková mapa
        - Menší matice výškových změn upravuje nulovou matici
        - Byl problém s příliš malými hodnotami -- vyřešeno normalizací
- Text:
    - Dokončení první kapitoly
        - Porovnání algoritmů -- tabulka a vysvětlení výběru
    - Kapitola Návrh:
        - Osnova kapitoly -- rozpracováno podle: https://www.inventoridigiochi.it/wp-content/uploads/2020/07/art-of-game-design.pdf
        - Úvod kapitoly -- Nejsou doplněné citace
        - První podkapitola: "Prostor" -- Nejsou doplněné citace
### Dotazy:
- Můžu používat příklady z knížky když nemají přímý vliv? Jak to citovat? -- Spíš ne?
- Přeskládání kapitol? -- Prohodit durhou a třetí kapitolu -- Zatím není podstatný

# Myšlenky diplomka:
- v prototypu budou jednotky jen objekty s různými hodnotami atributů
    - do funkčního projektu bude potřeba dělat děděné classy s různými metodamy (pro speciální schopnosti jednotek -- teoreticky bude stačit class stavitel a class valecnik ?)
