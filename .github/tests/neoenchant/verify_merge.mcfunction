execute if entity @e[tag=rs_regression,nbt={Item:{id:"minecraft:iron_ingot",count:2}}] run say RS_TEST_PASS vanilla stack merge
execute unless entity @e[tag=rs_regression,nbt={Item:{id:"minecraft:iron_ingot",count:2}}] run say RS_TEST_FAIL vanilla stack merge
kill @e[tag=rs_regression]
scoreboard objectives remove rs_regression
