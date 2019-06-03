import json
from django.core.management import BaseCommand
from django.conf import settings

ASSETS_DIR = getattr(settings, "ASSETS_DIR")


class Command(BaseCommand):

    help = "creating small sample of data."

    def read_in_chunks(self, f, newline):
        """
        Read a bulk file in chunks.
        """

        buf = ""
        while True:
            while newline in buf:
                pos = buf.index(newline)
                yield buf[:pos]
                buf = buf[pos + len(newline):]
            chunk = f.read(4096)
            if not chunk:
                yield buf
                break
            buf += chunk

    def get_small_sample(self, file_input, file_output, count=100000):
        """
        Creating small sample of a bulk file to a smaller one of given size.
        """

        with open(file_input) as f:
            reviews = []
            review_dict = {}
            last_key = None
            for line in self.read_in_chunks(f, "\n"):
                if len(reviews) == count:
                    break
                if line == "":
                    reviews.append(review_dict)
                    review_dict = {}
                else:
                    try:
                        key, val = line.split(":", 1)
                        temp = 1
                    except:
                        review_dict[last_key] += line.replace("\n", "")
                        temp = 0
                    if temp == 1:
                        key = key.strip().replace("\n", "")
                        val = val.strip().replace("\n", "")
                        review_dict[key] = unicode(val, errors='ignore')
                        last_key = key

        with open(file_output, 'w') as outfile:
            json.dump(reviews, outfile)

    def add_arguments(self, parser):

        parser.add_argument(
            '--input_file',
            type=str,
            required=True,
            default=ASSETS_DIR + "/foods.txt",
            help='Path of file for foods reviews data.',
        )

        parser.add_argument(
            '--output_file',
            type=str,
            required=False,
            default=ASSETS_DIR + "/reviews_data.json",
            help='Path of file for small sample  dataset.',
        )

        parser.add_argument(
            '--count',
            type=int,
            required=False,
            default=100000,
            help='Size of sample data required.',
        )

    def handle(self, *args, **options):

        input_file = options.get('input_file')
        output_file = options.get('output_file')
        count = options.get('count')

        self.stdout.write(">> Wait while creating small sample of %d is in proccess!" % (count, ))
        self.get_small_sample(input_file, output_file, count)
        self.stdout.write(">> Small sample file of reviews successfully created!")
