import os
import unittest
import textwrap
from StringIO import StringIO

from indicoio import config
from indicoio.config import Settings


class TestConfigureEnv(unittest.TestCase):

    def setUp(self):
        os.environ = {}

    def test_set_cloud_from_env_var(self):
        cloud = "invalid/cloud"
        os.environ["INDICO_CLOUD"] = cloud
        assert config.settings.cloud() == cloud

    def test_set_auth_from_env_var(self):
        username = "test"
        password = "password"
        os.environ["INDICO_USERNAME"] = username
        os.environ["INDICO_PASSWORD"] = password
        assert config.settings.auth() == (username, password)


class TestConfigurationFile(unittest.TestCase):

    def setUp(self):
        self.username = "test"
        self.password = "password"
        self.cloud = "localhost"
        config = """
        [auth]
        username = %s
        password = %s

        [private_cloud]
        cloud = %s
        """ % (self.username, self.password, self.cloud)

        config_file = StringIO(textwrap.dedent(config))
        self.settings = Settings(files=[config_file])
        os.environ = {}

    def test_set_cloud_from_config_file(self):
        assert self.settings.cloud() == self.cloud

    def test_set_auth_from_config_file(self):   
        assert self.settings.auth() == (self.username, self.password)        


class TestPrecedence(unittest.TestCase):

    def setUp(self):
        self.file_username = "file-username"
        self.file_password = "file-password"
        self.file_cloud = "file-cloud"

        self.env_username = "env-username"
        self.env_password = "env-password"      
        self.env_cloud = "env-cloud"
        config = """
        [auth]
        username = %s
        password = %s

        [private_cloud]
        cloud = %s
        """ % (self.file_username, self.file_password, self.file_cloud)

        config_file = StringIO(textwrap.dedent(config))
        os.environ = {
            'INDICO_CLOUD': self.env_cloud,
            'INDICO_USERNAME': self.env_username,
            'INDICO_PASSWORD': self.env_password
        }
        self.settings = Settings(files=[config_file])

    def test_set_cloud_from_config_file(self):
        assert self.settings.cloud() == self.env_cloud

    def test_set_auth_from_config_file(self):   
        assert self.settings.auth() == (self.env_username, self.env_password)        


class TestConfigFilePrecedence(unittest.TestCase):

    def setUp(self):
        self.high_priority_username = "high-priority-username"
        self.high_priority_password = "high-priority-password"
        self.high_priority_cloud = "high-priority-cloud"

        self.low_priority_username = "low-priority-username"
        self.low_priority_password = "low-priority-password"
        self.low_priority_cloud = "low-priority-cloud"

        high_priority_config = """
        [auth]
        username = %s
        password = %s

        [private_cloud]
        cloud = %s
        """ % (
            self.high_priority_username, 
            self.high_priority_password, 
            self.high_priority_cloud
        )

        low_priority_config = """
        [auth]
        username = %s
        password = %s

        [private_cloud]
        cloud = %s
        """ % (
            self.low_priority_username, 
            self.low_priority_password, 
            self.low_priority_cloud
        )

        high_priority_config_file = StringIO(textwrap.dedent(high_priority_config))
        low_priority_config_file = StringIO(textwrap.dedent(low_priority_config))

        os.environ = {}
        self.settings = Settings(files=[
            low_priority_config_file,
            high_priority_config_file
        ])

    def test_cloud_config_file_priority(self):
        assert self.settings.cloud() == self.high_priority_cloud

    def test_auth_config_file_priority(self):   
        assert self.settings.auth() == (self.high_priority_username, self.high_priority_password)        
