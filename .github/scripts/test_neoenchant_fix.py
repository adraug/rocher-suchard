"""Static packaging/scope checks for the Paxi NeoEnchant compatibility fix."""
import hashlib
import json
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "config/paxi/datapacks/rocher-suchard-neoenchant-fix"
OUTPUT_TAG = "data/rocher_suchard/tags/item/vanilla_auto_smelt_outputs.json"

class NeoEnchantVanillaFixTests(unittest.TestCase):
    def test_only_vanilla_smelting_outputs(self):
        values = json.loads((PACK / OUTPUT_TAG).read_text())["values"]
        self.assertEqual(values, [
            "minecraft:iron_ingot", "minecraft:gold_ingot",
            "minecraft:copper_ingot", "minecraft:netherite_scrap",
        ])

    def test_cleanup_is_whitelisted_and_xp_first(self):
        directory = PACK / "data/rocher_suchard/function"
        entry = (directory / "neoenchant_autosmelt_cleanup.mcfunction").read_text()
        finish = (directory / "neoenchant_autosmelt_finalize.mcfunction").read_text()
        award = (directory / "neoenchant_autosmelt_award_xp.mcfunction").read_text()
        self.assertIn("#rocher_suchard:vanilla_auto_smelt_outputs", entry)
        self.assertIn("if data entity @s Item.components.", entry)
        self.assertLess(finish.index("run function rocher_suchard:neoenchant_autosmelt_award_xp"),
                        finish.index("run data remove entity @s Item.components."))
        self.assertIn("Count int 1", award)
        self.assertIn("Value short 1", award)
        self.assertIn("minecraft:custom_data={}", finish)

    def test_packwiz_checksums(self):
        pack = tomllib.loads((ROOT / "pack.toml").read_text())
        index_file = ROOT / pack["index"]["file"]
        self.assertEqual('sha256', pack['index']['hash-format'])
        self.assertEqual(hashlib.sha256(index_file.read_bytes()).hexdigest(),
                         pack["index"]["hash"])
        entries = tomllib.loads(index_file.read_text())['files']
        indexed = {entry['file']: entry['hash'] for entry in entries}
        for path in PACK.rglob('*'):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            self.assertIn(relative, indexed)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             indexed[relative])

if __name__ == "__main__":
    unittest.main()
