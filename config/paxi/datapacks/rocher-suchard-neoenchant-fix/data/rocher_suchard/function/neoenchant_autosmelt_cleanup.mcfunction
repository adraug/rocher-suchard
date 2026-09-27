# NeoEnchant 5.14.0 can leave its temporary Auto Smelt markers on dropped items.
# Only target item entities carrying both NeoEnchant markers, then remove the
# custom_data component so the resulting stack is identical to the smelting result.
execute as @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}}}}] run data remove entity @s Item.components."minecraft:custom_data"
