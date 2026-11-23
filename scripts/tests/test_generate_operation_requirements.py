import importlib.util
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("gen", HERE.parent / "generate-operation-requirements.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


class OperationRequirementsTest(unittest.TestCase):
    def setUp(self):
        self.reqs, self.total, self.missing = gen.collect(
            yaml.safe_load((HERE / "fixtures/openapi-fixture.yaml").read_text())
        )

    def test_any_of_without_all(self):
        self.assertEqual((["thing:admin", "thing:view"], [], False), self.reqs["listThings"])

    def test_all_of_splits_out_of_any_of(self):
        self.assertEqual((["thing:approve", "thing:audit"], ["thing:create"], False), self.reqs["createThing"])

    def test_authenticated_sentinel(self):
        self.assertEqual(([], [], True), self.reqs["whoAmI"])

    def test_missing_extension_left_out(self):
        self.assertNotIn("noExtension", self.reqs)
        self.assertEqual(["noExtension"], self.missing)
        self.assertEqual(4, self.total)

    def test_render_is_sorted_and_deterministic(self):
        out = gen.render("com.x.sdk", self.reqs)
        self.assertEqual(out, gen.render("com.x.sdk", dict(reversed(list(self.reqs.items())))))
        self.assertLess(out.index('"createThing"'), out.index('"listThings"'))
        self.assertLess(out.index('"listThings"'), out.index('"whoAmI"'))
        self.assertIn('"createThing", new OperationRequirement(List.of("thing:approve", "thing:audit"), '
                      'List.of("thing:create"), false)', out)
        self.assertIn('"whoAmI", new OperationRequirement(List.of(), List.of(), true)', out)
        self.assertNotIn("noExtension", out)


if __name__ == "__main__":
    unittest.main()
