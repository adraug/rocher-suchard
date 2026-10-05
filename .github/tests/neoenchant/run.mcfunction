# Run only in a disposable Minecraft 1.21.1 test world.
kill @e[tag=rs_regression]
scoreboard objectives add rs_regression dummy
scoreboard players set passed rs_regression 0
summon minecraft:item 0 100 0 {Tags:["rs_regression","rs_empty"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{}}}}
summon minecraft:item 3 100 0 {Tags:["rs_regression","rs_normal"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{}}}
summon minecraft:item 6 100 0 {Tags:["rs_regression","rs_foreign"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{other_mod:42}}}}
summon minecraft:item 9 100 0 {Tags:["rs_regression","rs_pending"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b,other_mod:42}}}}
summon minecraft:item 12 100 0 {Tags:["rs_regression","rs_single"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b}}}}
summon minecraft:item 15 100 0 {Tags:["rs_regression","rs_nested"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{other_mod:{}}}}}
summon minecraft:item 18 100 0 {Tags:["rs_regression","rs_named"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{},"minecraft:custom_name":'{"text":"Keep me"}'}}}
summon minecraft:item 21 100 0 {Tags:["rs_regression","rs_markers"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}}}}
function rocher_suchard:neoenchant_autosmelt_cleanup
execute if items entity @e[tag=rs_empty,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_empty,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL empty
execute if items entity @e[tag=rs_normal,limit=1] contents *[!minecraft:custom_data] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_normal,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_FAIL normal
execute if items entity @e[tag=rs_foreign,limit=1] contents *[minecraft:custom_data={other_mod:42}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_foreign,limit=1] contents *[minecraft:custom_data={other_mod:42}] run say RS_TEST_FAIL foreign
execute if items entity @e[tag=rs_pending,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b,other_mod:42}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_pending,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b,other_mod:42}] run say RS_TEST_FAIL pending
execute if items entity @e[tag=rs_single,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_single,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b}] run say RS_TEST_FAIL single
execute if items entity @e[tag=rs_nested,limit=1] contents *[minecraft:custom_data={other_mod:{}}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_nested,limit=1] contents *[minecraft:custom_data={other_mod:{}}] run say RS_TEST_FAIL nested
execute if items entity @e[tag=rs_named,limit=1] contents *[!minecraft:custom_data,minecraft:custom_name='{"text":"Keep me"}'] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_named,limit=1] contents *[!minecraft:custom_data,minecraft:custom_name='{"text":"Keep me"}'] run say RS_TEST_FAIL named
execute if items entity @e[tag=rs_markers,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}] run scoreboard players add passed rs_regression 1
execute unless items entity @e[tag=rs_markers,limit=1] contents *[minecraft:custom_data={ne_auto_smelt_xp:1b,ne_auto_smelt_drops_xp:1b}] run say RS_TEST_FAIL markers
execute if score passed rs_regression matches 8 run say RS_TEST_PASS component checks 8/8
function rocher_suchard:neoenchant_autosmelt_cleanup
execute if items entity @e[tag=rs_empty,limit=1] contents *[!minecraft:custom_data] run say RS_TEST_PASS idempotent
kill @e[tag=rs_regression]
summon minecraft:item 0 100 0 {Tags:["rs_regression"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1,components:{"minecraft:custom_data":{}}}}
summon minecraft:item 0 100 0 {Tags:["rs_regression"],NoGravity:1b,PickupDelay:200s,Item:{id:"minecraft:iron_ingot",count:1}}
function rocher_suchard:neoenchant_autosmelt_cleanup
schedule function rs_test:verify_merge 100t
