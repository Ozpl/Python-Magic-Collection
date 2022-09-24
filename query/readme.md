# QUERY MECHANISM DOCUMENTATION

## Priority List:

- set + set_name (two separate columns) (main table) *e, edition, s, set* [string]

## Special Cases (not done):
- color_identity (color_identity) *id, identity* [array] **Piotr please clarify**
- format (legalities_table) *f, format* [object[string]] **Not sure how to approach to ensure best UX**
- mana_cost {W}{5} (main table) *m, mana* [string] **Not sure how to approach to ensure best UX**
- power (main table) *pow, power* [int] **Power might be string?**
- loyalty (main table) *loyal, loyalty* [int] **Loyalty might be "X"?**
- toughness (main table) *tou, toughness* [int] **Power might be string?**
- card_faces (card_faces) *is coś tam xD* **XD**

## Done:
- colors *c, color*
- cmc (main table) *cmc, mv, manavalue* [float]
- card_types (main table) *t, type* [string]
- rarity (main table) *r, rarity* [string]
- oracle_text (main table) *o, oracle* [string]
- prices (prices_table) *usd, eur, tix* [object[float]]
- games (games_table) *game* [array]
- keywords (separate table) *keyword* [array]
- released_at (main table) *date, year* [datetime]


