# NeoEnchant 5.14.0 removes its Auto Smelt markers after awarding XP, but leaves
# custom_data={}. An empty component still prevents stacking with normal drops.
# Leave all nonempty data (including pending XP markers) to its owning mod.
# Item component equality is exact: unlike an NBT {} selector, this cannot match
# nonempty compounds. Also repairs old empty-data stacks when dropped again.
execute as @e[type=minecraft:item] if items entity @s contents *[minecraft:custom_data={}] run data remove entity @s Item.components."minecraft:custom_data"
