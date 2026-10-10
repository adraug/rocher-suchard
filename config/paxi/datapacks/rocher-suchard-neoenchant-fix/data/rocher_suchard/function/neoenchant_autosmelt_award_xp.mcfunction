# @s: vanilla ore drop with both pending NeoEnchant Auto Smelt XP markers.
# Match NeoEnchant XP: Value = XP per item; Count = item stack count.
summon minecraft:experience_orb ~ ~ ~ {Value:0s,Tags:["rs_autosmelt_orb_tmp"]}
execute store result entity @n[type=minecraft:experience_orb,tag=rs_autosmelt_orb_tmp,distance=..1] Count int 1 run data get entity @s Item.count
execute store result entity @n[type=minecraft:experience_orb,tag=rs_autosmelt_orb_tmp,distance=..1] Value short 1 run data get entity @s Item.components."minecraft:custom_data".ne_auto_smelt_xp
tag @n[type=minecraft:experience_orb,tag=rs_autosmelt_orb_tmp,distance=..1] remove rs_autosmelt_orb_tmp
