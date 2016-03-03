from kinto import __version__ as VERSION

from .support import BaseWebTest, unittest


class HelloViewTest(BaseWebTest, unittest.TestCase):

    def test_returns_info_about_url_and_version(self):
        response = self.app.get('/')
        self.assertEqual(response.json['project_name'], 'kinto')
        self.assertEqual(response.json['project_version'], VERSION)
        self.assertEqual(response.json['project_docs'],
                         'https://kinto.readthedocs.org/')
        self.assertEqual(response.json['url'], 'http://localhost/v1/')

    def test_hides_user_info_if_anonymous(self):
        response = self.app.get('/')
        self.assertNotIn('user', response.json)

    def test_returns_user_id_if_authenticated(self):
        response = self.app.get('/', headers=self.headers)
        self.assertEqual(response.json['user']['id'],
                         ('basicauth:3a0c56d278def4113f38d0cfff6db1b06b'
                          '84fcc4384ee890cf7bbaa772317e10'))

    def test_returns_bucket_id_and_url_if_authenticated(self):
        response = self.app.get('/', headers=self.headers)
        self.assertEqual(response.json['user']['bucket'],
                         '23bb0efc-e80d-829e-6757-79d41e16640f')


class HelloViewSettingTrueTest(BaseWebTest, unittest.TestCase):

    def get_app_settings(self, additional_settings=None):
        settings = super(HelloViewSettingTrueTest, self).get_app_settings(
            additional_settings
        )
        settings['experimental_collection_schema_validation'] = True
        return settings

    def test_capability_is_exposed_if_setting_is_set(self):
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertIn('schema', capabilities)
        expected = {
            "description": "Enforce a schema for collection records.",
            "url": "http://kinto.readthedocs.org/en/latest/api/1.x/"
                   "collections.html#collection-json-schema",
        }
        self.assertEqual(expected, capabilities['schema'])


class HelloViewSettingFalseTest(BaseWebTest, unittest.TestCase):

    def get_app_settings(self, additional_settings=None):
        settings = super(HelloViewSettingFalseTest, self).get_app_settings(
            additional_settings
        )
        settings['experimental_collection_schema_validation'] = False
        return settings

    def test_capability_is_exposed_if_setting_is_not_set(self):
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertEqual(dict(), capabilities)
