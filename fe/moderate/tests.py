from django.test import TestCase
from .main import *

# Create your tests here.
class MyTestCase(TestCase):

    def setUp(self):
        self.comment = """
        I’m having so much trouble understanding the contents. 
        I spend so long just trying to understand 1 lecture cause 
        I keep repeating certain parts or spending hours watching YouTube 
        explanations, to the point where when I do finally somewhat get 
        what’s going on, I’m behind by 2 lectures already."
        """
        self.stopWords = "I am is are the a in"
    
    def tearDown(self):
        pass

    def test_scraping(self):
        pass

    def test_unit_sentiment_analysis(self):
        #text preprocessing
        cleaned1 = text_preprocessing([self.comment])[0]
        cleaned2 = text_preprocessing([self.stopWords])[0]

        self.assertGreater(len(cleaned1), 0) #ensure non-stopwords remain
        self.assertEqual(len(cleaned2), 0) #ensure all stopwords removed

        #model prediction
        rating1 = RFR_AI_model_predict([self.comment])[0]
        rating2 = RFR_AI_model_predict([self.stopWords])[0]
        self.assertTrue(1 <= rating1 <= 10) #check rating falls within range 0 - 10
        self.assertTrue(1 <= rating2 <= 10) #check rating falls within range 0 - 10

    def test_integration_sentiment_analysis(self):
        avg_rating = RFR_avg_rating([self.comment]) #integrate text-preprocessing and model prediction
        self.assertTrue(1 <= float(avg_rating) <= 10) #check rating falls within range 0 - 10

    def test_unit_emotion(self):
        dict1 = {"a": 1, "b": 0}
        dict2 = {"a": 2, "b": 3}
        self.assertEqual(merge_dict(dict1, dict2), {"a":3, "b":3}) #ensure merging done correctly

        self.assertEqual(list(get_emotion_dict(self.comment).keys()), ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']) #ensure all emotions present in comment

    def test_integration_emotion(self):
        emotions = emotion_chart([self.comment]) #integrate merge_dict and get_emotion_dict

        self.assertEqual(sum(emotions), 1) #ensure total breakdown equals to number of entry
        self.assertEqual(len(emotions), 5) #ensure 5 values, each for one emotion

        self.assertTrue(type(convert_emotion_chart_to_str(emotions)) is str) #ensure final output in a string

    def test_system_testing_scraping_sentiment(self):
        pass

#if __name__ == '__main__':
#    TestCase.main()