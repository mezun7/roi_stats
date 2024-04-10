from django.urls import reverse
from django.utils.html import format_html
from rest_framework import serializers

from . import views
from .models import Olympiad, Region, Participant, ParticipantResult


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('short_name',)


class OlympiadSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    codeforces_tour = serializers.SerializerMethodField()
    olymp_site = serializers.SerializerMethodField()
    contestants = serializers.SerializerMethodField()
    regions_count = serializers.SerializerMethodField()
    year_of_olympiad = serializers.SerializerMethodField()

    def get_year_of_olympiad(self, olympiad: Olympiad):
        url_olympiad = reverse(views.olympiad_result, args=[olympiad.pk])
        return format_html(f'<a href="{url_olympiad}">{olympiad.date_from.year}</a>')

    def get_contestants(self, olympiad: Olympiad):
        return Participant.objects.filter(olympiad=olympiad).count()

    def get_regions_count(self, olympiad: Olympiad):
        return Participant.objects.filter(olympiad=olympiad).values('region').distinct().count()

    def get_olymp_site(self, olympiad: Olympiad):
        if olympiad.olymp_site:
            return format_html(f'<a href="{olympiad.olymp_site}">{olympiad.olymp_site}</a>')
        return ''

    def get_codeforces_tour(self, olympiad: Olympiad):
        if olympiad.codeforces_tour:
            return format_html(f'<a href="{olympiad.codeforces_tour}">{olympiad.codeforces_tour}</a>')
        return ''

    class Meta:
        model = Olympiad
        fields = ('name',
                  'date_from',
                  'date_to',
                  'region',
                  'city',
                  'olymp_site',
                  'codeforces_tour',
                  'contestants',
                  'regions_count',
                  'year_of_olympiad',)


class OlympiadResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = (
            'olympiad',
            'participant',
            'score',
            'status',
            'rank',
            'grade',
            'student'
        )
