# @s: dropped vanilla ore-smelting result; run at its position.
# Both XP markers pending: award XP before removing anything.
execute if data entity @s Item.components."minecraft:custom_data".ne_auto_smelt_xp if data entity @s Item.components."minecraft:custom_data".ne_auto_smelt_drops_xp run function rocher_suchard:neoenchant_autosmelt_award_xp
# Single leftover marker: no second XP award without both markers.
execute if data entity @s Item.components."minecraft:custom_data".ne_auto_smelt_xp run data remove entity @s Item.components."minecraft:custom_data".ne_auto_smelt_xp
execute if data entity @s Item.components."minecraft:custom_data".ne_auto_smelt_drops_xp run data remove entity @s Item.components."minecraft:custom_data".ne_auto_smelt_drops_xp
# Exact empty-component match preserves other mods' nonempty custom data.
execute if items entity @s contents *[minecraft:custom_data={}] run data remove entity @s Item.components."minecraft:custom_data"
