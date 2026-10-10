# Auto Smelt datapack regression checks

Run these **only in a disposable Minecraft Java 1.21.1 world**. The tests
create item entities and XP orbs and remove nearby entities in their test area.

1. Copy `config/paxi/datapacks/rocher-suchard-neoenchant-fix` into the test
   world's `datapacks/` directory (vanilla), or let Paxi load it (full pack).
2. Create `datapacks/rs-test/pack.mcmeta`:

   ```json
   {"pack":{"pack_format":48,"description":"Auto Smelt regression checks"}}
   ```

3. Copy `run.mcfunction` and `verify_merge.mcfunction` into
   `datapacks/rs-test/data/rs_test/function/`.
4. Start the server, or use `/reload`. Then, from console:

   ```mcfunction
   execute in minecraft:overworld run forceload add 0 0 48 15
   execute in minecraft:overworld run function rs_test:run
   ```

5. After at least 100 game ticks, expect:

   ```text
   RS_TEST_PASS component checks 13/13
   RS_TEST_PASS XP values/count 4/4
   RS_TEST_PASS XP exactly once
   RS_TEST_PASS idempotent
   RS_TEST_PASS vanilla stack merge
   ```

   No `RS_TEST_FAIL` or datapack function loading errors should occur.

6. Unforce the chunks:

   ```mcfunction
   execute in minecraft:overworld run forceload remove 0 0 48 15
   ```

The 13 cases cover iron, gold, copper, and netherite scrap; exact XP value
and stack Count; empty/nonempty custom data, orphaned NeoEnchant markers,
non-XP components, non-vanilla-auto-smelt item IDs, and idempotence.
A diamond carrying markers simulates an out-of-scope modded drop without
needing Create installed.

Before merging, **also test actual mining in NeoForge + Paxi + NeoEnchant
5.14.0**, measuring XP, item stacks and old contaminated items dropped
from inventory. Create zinc must remain unchanged and unsmelted.

These are Minecraft command regression tests, not automatic in-game CI.
