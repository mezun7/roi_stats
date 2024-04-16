from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path

from roi.forms import RegionCsvImportForm, OlympiadResultCsvImportForm
from roi.importer.olympiad_results_import import import_olympiad_results, import_olympiads
from roi.importer.region_aliases_import import import_region_aliases
from roi.importer.regions_import import import_regions
from roi.models import Student, Region, Olympiad, Task, ParticipantResult, Participant, RegionAlias


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patranomic')
    search_fields = ('surname', 'name', 'patronomic')
    sortable_by = ('surname', 'name', 'patronomic')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'region_code')
    search_fields = ('name', 'region_code')
    sortable_by = ('name', 'region_code')

    change_list_template = 'entities/region_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-regions-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            import_regions(request.FILES["csv_file"])
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = RegionCsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/region_csv_form.html", payload
        )


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_from', 'date_to', 'region', 'city')
    search_fields = ('name', 'region__short_name', 'city', 'date_from__year')
    sortable_by = ('date_from', 'date_to')
    list_filter = ('date_from', 'region')
    autocomplete_fields = ('region',)
    change_list_template = 'entities/olympiad_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-olympiad-results-csv/', self.import_csv),
            path('import-olympiads/', self.import_olympiads_csv)
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = OlympiadResultCsvImportForm(request.POST, request.FILES)
            olympiad = None
            if form.is_valid():
                olympiad = form.cleaned_data['olympiad']
                import_olympiad_results(request.FILES["csv_file"], olympiad)
            #
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = OlympiadResultCsvImportForm(initial={"olympiad": Olympiad.objects.all().order_by('-date_from').first()})
        payload = {"form": form}
        return render(
            request, "admin/olympiad_result_csv_form.html", payload
        )

    def import_olympiads_csv(self, request):
        if request.method == "POST":
            form = RegionCsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                import_olympiads(request.FILES["csv_file"])
            #
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = RegionCsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/region_csv_form.html", payload
        )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('alias', 'name', 'olympiad')
    search_fields = ('name', 'olympiad__name', 'alias')
    list_filter = ('olympiad',)
    autocomplete_fields = ('olympiad',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('student', 'olympiad', 'region', 'status', 'grade')
    list_filter = ('region', 'status', 'grade', 'olympiad')
    autocomplete_fields = ('student', 'olympiad', 'region')
    search_fields = ('student__surname', 'student__name', 'olympiad__name', 'olympiad__date_from__year')


@admin.register(ParticipantResult)
class ParticipantResultAdmin(admin.ModelAdmin):
    list_display = ('participant', 'task', 'score')
    sortable_by = ('participant__student__surname',)
    autocomplete_fields = ('participant', 'task')
    search_fields = ('participant__surname', 'participant__name', 'olympiad__name', 'task__name')


@admin.register(RegionAlias)
class RegionAliasAdmin(admin.ModelAdmin):
    list_display = ('region', 'alias')
    search_fields = ('region', 'alias__name')
    list_filter = ('region',)
    change_list_template = 'entities/region_aliases_change_list.html'
    autocomplete_fields = ('region',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-region-aliases-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            import_region_aliases(request.FILES["csv_file"])
            #
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = RegionCsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/region_csv_form.html", payload
        )