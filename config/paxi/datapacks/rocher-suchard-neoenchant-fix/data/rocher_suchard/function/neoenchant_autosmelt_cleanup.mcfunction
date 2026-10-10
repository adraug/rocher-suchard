# NeoEnchant 5.14.0 can leave XP markers on dropped vanilla ore outputs.
# Never touch modded ore drops such as Create zinc, or unrelated blocks.
execute as @e[type=minecraft:item] at @s if items entity @s contents #rocher_suchard:vanilla_auto_smelt_outputs if data entity @s Item.components."minecraft:custom_data" run function rocher_suchard:neoenchant_autosmelt_finalize
