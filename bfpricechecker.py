from wikiapi import Price

price = Price()

coal = price.load_price("Coal")
adamant = price.load_price("Adamantite ore")
adamant_bar = price.load_price("Adamantite bar")
iron = price.load_price("Iron ore")
steel_bar = price.load_price("Steel bar")
rune = price.load_price("Runite ore")
rune_bar = price.load_price("Runite bar")
stamina_pot = price.load_price("Stamina potion(4)")

steel_num = 4600
adamant_num = 2200
rune_num = 1850

coffer_rate = 72000

steel_profit =((steel_bar - (iron + coal)))*steel_num - (stamina_pot * 9) - coffer_rate
adamant_profit = ((adamant_bar - (adamant + (coal*3)))*adamant_num) - (stamina_pot * 9) - coffer_rate
rune_profit = ((rune_bar - (rune + (coal*4)))*rune_num) - (stamina_pot * 9) - coffer_rate

print(f'rune: {rune_profit} gp per hour.\nadamant: {adamant_profit} gp per hour.\nsteel: {steel_profit} gp per hour.')


