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
