# Auto Smelt datapack regression checks

Run these only in a disposable Minecraft Java 1.21.1 world. They summon test
items, use the `rs_regression` scoreboard objective and remove their tagged
entities afterwards. No test fixtures are included in Packwiz exports.

1. Copy `config/paxi/datapacks/rocher-suchard-neoenchant-fix` into the test
   world's `datapacks/` directory (vanilla), or let Paxi load it (full pack).
2. Create a separate `datapacks/rs-test/pack.mcmeta` containing:

   ```json
   {"pack":{"pack_format":48,"description":"Auto Smelt regression checks"}}
   ```

3. Copy the two `.mcfunction` files in this directory into
   `datapacks/rs-test/data/rs_test/function/`.
4. Start the server, or run `reload`. From the server console, run:

   ```text
   execute in minecraft:overworld run forceload add 0 0 31 15
   execute in minecraft:overworld run function rs_test:run
   ```

5. Allow at least 100 game ticks for the merge check. Expect all three messages
   and no `RS_TEST_FAIL` or function-loading errors:

   ```text
   RS_TEST_PASS component checks 8/8
   RS_TEST_PASS idempotent
   RS_TEST_PASS vanilla stack merge
   ```

6. Run `execute in minecraft:overworld run forceload remove 0 0 31 15`.

The eight cases cover an empty component, an ordinary ingot, foreign data,
both pending NeoEnchant markers plus foreign data, a single marker, a nested
empty compound owned by another mod, a custom name plus empty data, and both
pending markers alone. The final check confirms that a repaired old ingot and
a normal ingot actually merge into a stack of two.

This verifies Minecraft command behavior, not NeoForge/Paxi integration or the
complete modpack. Also test actual Auto Smelt mining, XP, and drop/pickup repair
of existing ingots on the updated server with normal and optimized clients.
