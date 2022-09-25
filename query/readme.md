# QUERY MECHANISM DOCUMENTATION


## Special Cases (not done):

- format (legalities_table) *f, format* [object[string]] **Not sure how to approach to ensure best UX**
- mana_cost {W}{5} (main table) *m, mana* [string] **Example query: where mana_cost LIKE "%{G}{G}%" AND mana_cost LIKE "%{B}{B}%"**
- power (main table) *pow, power* [int] **Try casting to INT, if not then 0**
- loyalty (main table) *loyal, loyalty* [int] **Try casting to INT, if not then 0**
- toughness (main table) *tou, toughness* [int] **Try casting to INT, if not then 0**
- card_faces (card_faces) *is coś tam xD* **XD**

## Done:
- colors *c, color* [array]
- color_identity (color_identity) *id, identity* [array]
- cmc (main table) *cmc, mv, manavalue* [float]
- card_types (main table) *t, type* [string]
- rarity (main table) *r, rarity* [string]
- oracle_text (main table) *o, oracle* [string]
- prices (prices_table) *usd, eur, tix* [object[float]]
- games (games_table) *game* [array]
- keywords (separate table) *keyword* [array]
- released_at (main table) *date, year* [datetime]
- set + set_name (two separate columns) (main table) *e, edition, s, set* [string]


## Colors Mechanism Pseudo Code:
--color:r    -> wszystko co zawiera w sobie "r"                              [single, multi]
WHERE colors.array_value LIKE '%R%'

--color=r    -> wszystkie karty, które są czerwone                           [single]
WHERE length(colors.array_value) = 1 and instr(colors.array_value, 'R') = 1

--color=rw   -> wszystkie karty z tymi kolorami (nie mniej nie wiecej)       [multi]
WHERE length(colors.array_value) = (2 + (2-1)) AND (colors.array_value LIKE '%R%' AND colors.array_value LIKE '%W%')

--color:rw   -> wszystkie karty z zawartym i "r" i "w" (rw, rwg, rwb...)     [multi]
WHERE colors.array_value LIKE '%R%' AND colors.array_value LIKE '%W%'

--color>=rw  -> wszystkie karty z zawartym i "r" i "w" (rw, rwg, rwb...)     [multi]
WHERE colors.array_value LIKE '%R%' AND colors.array_value LIKE '%W%'

--color<=rw  -> wszystkie karty bez kolor, albo same r, albo same w, albo rw [single, multi]
WHERE (length(colors.array_value) = 1 and instr(colors.array_value, 'R') = 1) 
OR (length(colors.array_value) = 1 and instr(colors.array_value, 'W') = 1)
OR (LENGTH(colors.array_value) = 0)
OR (length(colors.array_value) = (2 + (2-1)) AND (colors.array_value LIKE '%R%' AND colors.array_value LIKE '%W%'))

--color>r    -> wszystkie karty wielokolorowe, ktore maja r (rw, rwb, rg...) [multi]
WHERE length(colors.array_value)>1 AND colors.array_value LIKE '%R%'

--color<rw    ->  wszystkie karty bez koloru [multi]
WHERE length(colors.array_value) < 3 AND (colors.array_value LIKE '%r%' OR colors.array_value LIKE '%w%' OR length(colors.array_value) = 0)

--color>rw    -> wszystkie karty wielokolorowe, ktore maja r (rw, rwb, rg...) [multi]
WHERE length(colors.array_value)>1 AND colors.array_value LIKE '%R%'
