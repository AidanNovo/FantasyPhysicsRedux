# To solve circular import issues, this is a module where all the floating variables live
# There is surely a much better way to do this.

neutrino_flux = 1000  # Should vary by week in actual version, pulled from actual data

data = 0
score = 0

deck = []

max_active_cards = 5  # The max number of cards that may be in the active row


# Card rarity coefficients. Used when opening booster packs.

# Keep in mind that the "true" rarity of any type is equal to the rarity coefficient times the number of cards of that
# rarity. So if you don't make many legendary cards, they will be getting hit twice.
r_common = 10
r_uncommon = 5
r_rare = 3
r_legendary = 1