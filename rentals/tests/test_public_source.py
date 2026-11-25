import subprocess
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase


class PublicSourceTests(SimpleTestCase):
    def test_neutral_identity_asset_is_available(self):
        self.assertIsNotNone(finders.find('rentals/img/workflow-mark.svg'))

    def test_no_bundled_contracts_or_customer_exports(self):
        root = Path(settings.BASE_DIR)
        self.assertFalse((root / 'sample_data').exists())
        self.assertFalse((root / 'scripts/import_export_examples').exists())

    def test_anonymous_login_uses_neutral_identity(self):
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'Contract workflow')
        self.assertContains(response, 'workflow-mark.svg')

    def test_django_entry_points_are_importable(self):
        from django.utils.module_loading import import_string
        self.assertTrue(callable(import_string(settings.WSGI_APPLICATION)))
        self.assertTrue(callable(import_string(settings.ASGI_APPLICATION)))

    def test_environment_configuration_is_not_tracked(self):
        root = Path(settings.BASE_DIR)
        tracked = subprocess.check_output(
            ["git", "ls-files", "--", ".env", ".env.*"], cwd=root, text=True
        ).splitlines()
        self.assertEqual(tracked, [".env.example"])
