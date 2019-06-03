import sys
import json
import re
import string
from django.core.management import BaseCommand
from django.conf import settings

from search.utils import get_json_data

ASSETS_DIR = getattr(settings, "ASSETS_DIR")


class Command(BaseCommand):

    help = "Generate index file for small sample of reviews."

    def clean_html(self, content):
        """
        Clean any HTML tags that present in given reviews's data.
        """

        cleanrx = re.compile('<.*?>')
        cleaned_text = re.sub(cleanrx, '', content)

        removable_tags = ["(<br", "<br", "br>", "/>"]
        for tag in removable_tags:
            cleaned_text = cleaned_text.replace(tag, "")

        return cleaned_text

    def clean_words(self, word):
        """
        Remove punctuations and clean all words in string.
        """

        for char in string.punctuation:
            word = word.strip(char)
            word = word.replace(char, " ")
        return [w for w in word.split(" ") if w]

    def generate_index_by_words(self, input_file, output_file):
        """
        Generate the index in format {words: review}.
        """

        try:
            word_list = {}

            with open(input_file) as f:
                data = json.load(f)
                word_rid_obj = {}
                for i, obj in enumerate(data):
                    review_summary = obj.get('review/summary')
                    review_text = obj.get('review/text')
                    words = list(set(review_summary.split() + review_text.split()))
                    print(words)

                    temp_words = []
                    for word in words:
                        word = self.clean_html(word.lower())
                        words = self.clean_words(word)
                        temp_words += words

                    for word in temp_words:
                        if word:
                            if not word_list.has_key(word):
                                word_list[word] = []

                            if not word_rid_obj.has_key(word):
                                word_rid_obj[word] = set()
                            if i not in word_rid_obj[word]:
                                word_list[word].append(i)
                                word_rid_obj[word].add(i)
        except IOError as ioe:
            print input_file
            sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
            sys.exit(1)

        if word_list:
            with open(output_file, 'w') as outfile:
                json.dump(word_list, outfile)

    def generate_index_by_reviews(self, reviews_data, index_by_words, output_file):
        """
        Generate the index in format {review_index: {words: {}, review_score: 0.0}.
        """

        index_by_words = get_json_data(index_by_words)
        reviews_data = get_json_data(reviews_data)
        result = {}
        for word, indexes in index_by_words.items():
            for ind in indexes:
                if not result.has_key(ind):
                    result[ind] = {"words": {}, "review_score": reviews_data[ind].get("review/score", '0.0')}
                result[ind]["words"][word] = 1

        if result:
            with open(output_file, 'w') as outfile:
                json.dump(result, outfile)

    def add_arguments(self, parser):

        parser.add_argument(
            '--input_file',
            type=str,
            required=True,
            default=ASSETS_DIR+"/reviews_data.json",
            help='Path of file for small sample of reviews data file.',
        )

        parser.add_argument(
            '--output_file_1',
            type=str,
            required=False,
            default=ASSETS_DIR + "/indexed_data_1.json",
            help='Path of file for indexed data by words.',
        )

        parser.add_argument(
            '--output_file_2',
            type=str,
            required=False,
            default=ASSETS_DIR + "/indexed_data_2.json",
            help='Path of file for indexed data by reviews.',
        )

    def handle(self, *args, **options):

        input_file = options.get('input_file')
        output_file_1 = options.get('output_file_1')
        output_file_2 = options.get('output_file_2')

        self.stdout.write(">> Generating Index (1 of 2).")
        self.generate_index_by_words(input_file, output_file_1)
        self.stdout.write(">> Generating Index (2 of 2).")
        self.generate_index_by_reviews(input_file, output_file_1, output_file_2)
        self.stdout.write(">> Indexing successfully done!")
