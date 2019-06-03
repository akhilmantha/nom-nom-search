# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

from search.serializers import SearchSerializer
from search.utils import get_json_data

MAX_REVIEWS_COUNT_PER_HIT = getattr(settings, 'MAX_REVIEWS_COUNT_PER_HIT', 20)


class SearchViewset(viewsets.GenericViewSet):

    def get_queryset(self):
        return None
    
    def get_serializer_class(self):
        return SearchSerializer

    def get_indexed_data(self):
        """
        Return review's indexed data file which prepared by command run.
        """
        files = settings.FILES

        data_by_words = get_json_data(files["REVIEWS"]["INDEXED_DATA_BY_WORDS"])
        data_by_reviews = get_json_data(files["REVIEWS"]["INDEXED_DATA_By_REVIEWS"])

        return data_by_words, data_by_reviews

    def get_data(self):
        """
        Return review data from review data file.
        """
        files = settings.FILES
        data = get_json_data(files["REVIEWS"]["DATA"])
        return data

    def create(self, request, *args, **kwargs):
        query = request.data.get('query', '')
        query = query.split(" ")
        if not query or query == ['']:
            return Response(
                {"error": "Insufficient arguments"}, status=status.HTTP_400_BAD_REQUEST)

        # Load static data from files (reviews data, indexed data) to variables.
        reviews_data = self.get_data()
        indexed_data_by_words, indexed_data_by_reviews = self.get_indexed_data()

        # Get all indexes of reviews whose summary or text contains given query words.
        review_indexes = []
        [review_indexes.extend(indexed_data_by_words.get(q.lower(), [])) for q in query]

        # print(review_indexes)
        # Calculating query score for reviews get into review_indexes.
        reviews_score_data = []
        for ind in set(review_indexes):
            ind = str(ind)
            query_score = 0
            for q in query:
                query_score += indexed_data_by_reviews[ind]["words"].get(q, 0)
            query_score = query_score / len(query)
            reviews_score_data.append(
                {
                    'query_score': query_score,
                    'review_score': indexed_data_by_reviews[ind]["review_score"],
                    'id': ind
                }
            )

        # Sort score data by query_score then review_score.
        reviews_score_data = sorted(
            reviews_score_data,
            key=lambda score_data: (score_data['query_score'], score_data['review_score']),
            reverse=True
        )

        # get top k high scored data of reviews.
        reviews_data = [reviews_data[int(review['id'])] \
                        for review in reviews_score_data[:MAX_REVIEWS_COUNT_PER_HIT]]
        self.queryset = None
        return Response(reviews_data, status=status.HTTP_200_OK)
