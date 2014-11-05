import unittest

import numpy as np

from indicoio.local import political, sentiment, fer, facial_features, language, image_features

DIR = os.path.dirname(os.path.realpath(__file__))


class FullAPIRun(unittest.TestCase):

    def load_image(self, relpath, as_grey=False):
        image_path = os.path.normpath(os.path.join(DIR, relpath))
        image = skimage.io.imread(image_path, as_grey=True).tolist()
        return image

    def check_range(self, list, minimum=0.9, maximum=0.1, span=0.5):
        vector = np.asarray(list)
        self.assertTrue(vector.max() > maximum)
        self.assertTrue(vector.min() < minimum)
        self.assertTrue(np.ptp(vector) > span)

    def test_document_classification(self):
        categories = set(['arts'])
        text = "On Monday, president Barack Obama will be..."
        results = classification(text)
        self.assertTrue(categories < set(results.keys()))

    def test_political(self):
        political_set = set(['Libertarian', 'Liberal', 'Conservative', 'Green'])
        test_string = "Guns don't kill people, people kill people."
        response = political(test_string)

        self.assertTrue(isinstance(response, dict))
        self.assertEqual(political_set, set(response.keys()))

        test_string = "Save the whales"
        response = political(test_string)

        self.assertTrue(isinstance(response, dict))
        assert response['Green'] > 0.5

    def test_posneg(self):
        test_string = "Worst song ever."
        response = sentiment(test_string)

        self.assertTrue(isinstance(response, float))
        self.assertTrue(response < 0.5)

        test_string = "Best song ever."
        response = sentiment(test_string)
        self.assertTrue(isinstance(response, float))
        self.assertTrue(response > 0.5)

    def test_good_fer(self):
        fer_set = set(['Angry', 'Sad', 'Neutral', 'Surprise', 'Fear', 'Happy'])
        test_face = np.random.rand(48,48).tolist()
        response = fer(test_face)

        self.assertTrue(isinstance(response, dict))
        self.assertEqual(fer_set, set(response.keys()))

    def test_happy_fer(self):
        test_face = self.load_image("../data/happy.png", as_grey=True)
        response = fer(test_face)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(response['Happy'] > 0.5)

    def test_fear_fer(self):
        test_face = self.load_image("../data/fear.png", as_grey=True)
        response = fer(test_face)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(response['Fear'] > 0.25)

    def test_bad_fer(self):
        fer_set = set(['Angry', 'Sad', 'Neutral', 'Surprise', 'Fear', 'Happy'])
        test_face = np.random.rand(56,56).tolist()
        response = fer(test_face)

        self.assertTrue(isinstance(response, dict))
        self.assertEqual(fer_set, set(response.keys()))

    def test_good_facial_features(self):
        test_face = np.random.rand(48,48).tolist()
        response = facial_features(test_face)

        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 48)
        self.check_range(response)
    
    def test_good_image_features_greyscale(self):
        test_image = np.random.rand(64, 64).tolist()
        response = image_features(test_image)

        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 2048)
        self.check_range(response)

    def test_good_image_features_rgb(self):
        test_image = np.random.rand(64, 64, 3).tolist()
        response = image_features(test_image)

        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 2048)
        self.check_range(response)

    def test_language(self):
        language_set = set([
            'English',
            'Spanish',
            'Tagalog',
            'Esperanto',
            'French',
            'Chinese',
            'French',
            'Bulgarian',
            'Latin',
            'Slovak',
            'Hebrew',
            'Russian',
            'German',
            'Japanese',
            'Korean',
            'Portuguese',
            'Italian',
            'Polish',
            'Turkish',
            'Dutch',
            'Arabic',
            'Persian (Farsi)',
            'Czech',
            'Swedish',
            'Indonesian',
            'Vietnamese',
            'Romanian',
            'Greek',
            'Danish',
            'Hungarian',
            'Thai',
            'Finnish',
            'Norwegian',
            'Lithuanian'
        ])
        language_dict = language('clearly an english sentence')
        self.assertEqual(language_set, set(language_dict.keys()))
        assert language_dict['English'] > 0.25


if __name__ == "__main__":
    unittest.main()
