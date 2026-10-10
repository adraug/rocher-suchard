# Run only in a disposable Minecraft 1.21.1 world.
kill @e[tag=rs_regression]
scoreboard objectives add rs_regression dummy
scoreboard players set passed rs_regression 0
summon minecraft:item 0 100 0 {Tags:["rs_regression","rs_iron_pending"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:3,components:{"minecraft:custom_data":{ne_auto_smelt_xp:2b,ne_auto_smelt_drops_xp:1b,other_mod:42}}}}
summon minecraft:item 4 100 0 {Tags:["rs_regression","rs_gold_pending"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:gold_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}}}}
summon minecraft:item 8 100 0 {Tags:["rs_regression","rs_copper_pending"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:copper_ingot",count:2,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}}}}
summon minecraft:item 12 100 0 {Tags:["rs_regression","rs_scrap_pending"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:netherite_scrap",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:2b,ne_auto_smelt_drops_xp:1b}}}}
summon minecraft:item 16 100 0 {Tags:["rs_regression","rs_iron_empty"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{}}}}
summon minecraft:item 20 100 0 {Tags:["rs_regression","rs_gold_normal"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:gold_ingot",count:1,components:{}}}
summon minecraft:item 24 100 0 {Tags:["rs_regression","rs_copper_foreign"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:copper_ingot",count:1,components:{"minecraft:custom_data":{other_mod:42}}}}
summon minecraft:item 28 100 0 {Tags:["rs_regression","rs_gold_orphan_xp"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:gold_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b}}}}
summon minecraft:item 32 100 0 {Tags:["rs_regression","rs_iron_orphan_flag"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_drops_xp:1b}}}}
summon minecraft:item 36 100 0 {Tags:["rs_regression","rs_scrap_nested"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:netherite_scrap",count:1,components:{"minecraft:custom_data":{other_mod:{}}}}}
summon minecraft:item 40 100 0 {Tags:["rs_regression","rs_iron_named"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{},"minecraft:custom_name":'{"text":"Keep me"}'}}}
summon minecraft:item 44 100 0 {Tags:["rs_regression","rs_diamond_markers"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:diamond",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}}}}
summon minecraft:item 48 100 0 {Tags:["rs_regression","rs_glass_empty"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:glass",count:1,components:{"minecraft:custom_data":{}}}}
function rocher_suchard:neoenchant_autosmelt_cleanup
execute if items entity @e[tag=rs_iron_pending,limit=1] contents *[minecraft:custom_data={other_mod:42}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_iron_pending,limit=1] contents *[minecraft:custom_data={other_mod:42}] run say RS_TEST_FAIL iron_pending
execute if items entity @e[tag=rs_gold_pending,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_gold_pending,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL gold_pending
execute if items entity @e[tag=rs_copper_pending,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_copper_pending,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL copper_pending
execute if items entity @e[tag=rs_scrap_pending,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_scrap_pending,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL scrap_pending
execute if items entity @e[tag=rs_iron_empty,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_iron_empty,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL iron_empty
execute if items entity @e[tag=rs_gold_normal,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_gold_normal,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL gold_normal
execute if items entity @e[tag=rs_copper_foreign,limit=1] contents *[minecraft:custom_data={other_mod:42}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_copper_foreign,limit=1] contents *[minecraft:custom_data={other_mod:42}] run say RS_TEST_FAIL copper_foreign
execute if items entity @e[tag=rs_gold_orphan_xp,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_gold_orphan_xp,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL gold_orphan_xp
execute if items entity @e[tag=rs_iron_orphan_flag,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_iron_orphan_flag,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL iron_orphan_flag
execute if items entity @e[tag=rs_scrap_nested,limit=1] contents *[minecraft:custom_data={other_mod:{}}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_scrap_nested,limit=1] contents *[minecraft:custom_data={other_mod:{}}] run say RS_TEST_FAIL scrap_nested
execute if items entity @e[tag=rs_iron_named,limit=1] contents *[!minecraft:custom_data,minecraft:custom_name='{"text":"Keep me"}'] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_iron_named,limit=1] contents *[!minecraft:custom_data,minecraft:custom_name='{"text":"Keep me"}'] run say RS_TEST_FAIL iron_named
execute if items entity @e[tag=rs_diamond_markers,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_diamond_markers,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}] run say RS_TEST_FAIL diamond_markers
execute if items entity @e[tag=rs_glass_empty,limit=1] contents *[minecraft:custom_data={}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_glass_empty,limit=1] contents *[minecraft:custom_data={}] run say RS_TEST_FAIL glass_empty
execute if score passed rs_regression matches 13 run say RS_TEST_PASS component checks 13/13
execute positioned 0 100 0 if entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:2s,Count:3}] run scoreboard players add passed rs_regression 1
execute positioned 0 100 0 unless entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:2s,Count:3}] run say RS_TEST_FAIL iron_pending XP
execute positioned 4 100 0 if entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:1s,Count:1}] run scoreboard players add passed rs_regression 1
execute positioned 4 100 0 unless entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:1s,Count:1}] run say RS_TEST_FAIL gold_pending XP
execute positioned 8 100 0 if entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:1s,Count:2}] run scoreboard players add passed rs_regression 1
execute positioned 8 100 0 unless entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:1s,Count:2}] run say RS_TEST_FAIL copper_pending XP
execute positioned 12 100 0 if entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:2s,Count:1}] run scoreboard players add passed rs_regression 1
execute positioned 12 100 0 unless entity @e[type=minecraft:experience_orb,distance=..1,nbt={Value:2s,Count:1}] run say RS_TEST_FAIL scrap_pending XP
execute if score passed rs_regression matches 17 run say RS_TEST_PASS XP values/count 4/4
# Running cleanup again must not spawn further XP orbs.
function rocher_suchard:neoenchant_autosmelt_cleanup
scoreboard players set orbs rs_regression 0
execute as @e[type=minecraft:experience_orb,x=0,y=99,z=-1,dx=49,dy=3,dz=2] run scoreboard players add orbs rs_regression 1
execute if score orbs rs_regression matches 4 run say RS_TEST_PASS XP exactly once
execute unless score orbs rs_regression matches 4 run say RS_TEST_FAIL XP duplicate/missing orbs
execute if items entity @e[tag=rs_iron_pending,limit=1] contents *[minecraft:custom_data={other_mod:42}] run say RS_TEST_PASS idempotent
# Clean up all temporary fixtures, then test natural item merging.
kill @e[tag=rs_regression]
kill @e[type=minecraft:experience_orb,x=0,y=99,z=-1,dx=49,dy=3,dz=2]
summon minecraft:item 0 100 0 {Tags:["rs_regression"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{}}}}
summon minecraft:item 0 100 0 {Tags:["rs_regression"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1}}
function rocher_suchard:neoenchant_autosmelt_cleanup
schedule function rs_test:verify_merge 100t
