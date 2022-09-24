# QUERY MECHANISM DOCUMENTATION

## Priority List:
- color_identity (color_identity) *id, identity* [array] **Piotr please clarify**

- set + set_name (two separate columns) (main table) *e, edition, s, set* [string]



- prices (prices_table) *usd, eur, tix* [object[float]]


- games (games_table) *game* [array]
- format (legalities_table) *f, format* [object[string]]
- keywords (separate table) *keyword* [array]
- mana_cost {W}{5} (main table) *m, mana* [string]
- power (main table) *pow, power* [int]
- toughness (main table) *tou, toughness* [int]
- loyalty (main table) *loyal, loyalty* [int]
- released_at (main table) *date, year* [datetime] 
- card_faces (card_faces) *is coś tam xD*

## Done:
- colors *c, color*
- cmc (main table) *cmc, mv, manavalue* [float]
- card_types (main table) *t, type* [string]
- rarity (main table) *r, rarity* [string]
- oracle_text (main table) *o, oracle* [string]