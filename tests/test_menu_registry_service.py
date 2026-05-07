"""Unit tests for MenuRegistryService (no live Supabase)."""

import unittest
from unittest.mock import MagicMock, patch

from services.menu_registry_service import MenuRegistryService


class MenuRegistryServiceUnitTests(unittest.TestCase):
    def test_menu_has_any_action_false_for_empty_modules(self):
        self.assertFalse(MenuRegistryService.menu_has_any_action([]))
        self.assertFalse(MenuRegistryService.menu_has_any_action([{"module_code": "X", "actions": []}]))

    def test_menu_has_any_action_true(self):
        self.assertTrue(
            MenuRegistryService.menu_has_any_action(
                [{"module_code": "X", "actions": [{"action_key": "A"}]}]
            )
        )

    def test_fetch_uses_production_filter_on_query_builder(self):
        captured: dict[str, list] = {"filters": []}

        class Q:
            def eq(self, col, val):
                captured["filters"].append((col, val))
                return self

            def execute(self):
                m = MagicMock()
                m.data = []
                return m

        q = Q()
        client = MagicMock()
        client.table.return_value.select.return_value = q

        svc = MenuRegistryService(client)
        svc.fetch_menu_modules("rid-1", "PRODUCTION")

        self.assertIn(("environment_scope", "PRODUCTION"), captured["filters"])
        self.assertIn(("visible", True), captured["filters"])
        self.assertIn(("enabled", True), captured["filters"])
        self.assertIn(("role_id", "rid-1"), captured["filters"])

    @patch.dict("os.environ", {"EDS_MENU_ENVIRONMENT_SCOPE": "INVALID"}, clear=False)
    def test_resolve_scope_invalid(self):
        from services.menu_registry_service import resolve_menu_environment_scope as r

        scope, err = r()
        self.assertIsNone(scope)
        self.assertEqual(err, "MENU_ENVIRONMENT_SCOPE_INVALID")

    @patch.dict("os.environ", {"EDS_MENU_ENVIRONMENT_SCOPE": "PRODUCTION"}, clear=False)
    def test_resolve_scope_production(self):
        from services.menu_registry_service import resolve_menu_environment_scope as r

        scope, err = r()
        self.assertEqual(scope, "PRODUCTION")
        self.assertIsNone(err)


if __name__ == "__main__":
    unittest.main()
