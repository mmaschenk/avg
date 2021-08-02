from django.contrib import admin
from .models import AVGRegisterline, SharepointExcelFile

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'

admin_site = MyAdminSite(name='myadmin')


def breaksublist(worklist, count):
    sublist = []
    while worklist:
        sublist.append(tuple(worklist[:count]))
        worklist = worklist[count:]
    return tuple(sublist)

# Register your models here.

labelmap = {
        'registratie_van_NAW_gegevens': "NAW",
        'registratie_van_genderinformatie': "Gender",
        'registratie_van_geboortedatum': "Geb.dat",
        'registratie_van_geboorteplaats': "Plaats", 
        'registratie_van_nationaliteit': "Nat.",
        'registratie_van_IBAN_nummer': "IBAN",
        'verwerking_van_foto': "Foto",
        'registratie_van_emailadres': "Email",
        'registratie_van_telefoonnummer': "Tel",
        'registratie_van_identificatiebewijs': "ID",
        'registratie_van_BSN_nummer': "BSN",
        'registratie_van_studienummer': "St.nr",
        'registratie_van_personeelsnummer': "P.nr.",
        'registratie_van_videobeeldinformatie': "Video",
        'registratie_van_geluidsinformatie': "Geluid",
        'registratie_van_locatie_informatie': "Loc",
        'registratie_van_financiële_informatie': "Fin",
        'registratie_van_burgerlijke_staat': "BS",
        'registratie_van_gezinssamenstelling': "Gezin",
        'registratie_van_lidmaatschap_van_een_vakbond': "Vakb",
        'registratie_van_strafrechtelijke_gegevens': "Juri",
        'registratie_van_gezondheidsgegevens': "Gez",
        'registratie_van_opleidingsinformatie': "Opl",
        'registratie_van_functie_informatie': "Functie",
        'registratie_van_seksuele_geaardheid': "Seks",
        'registratie_van_politieke_voorkeur': "Polit",
        'registratie_van_religie': "Reli",
        'registratie_van_genetische_informatie': "Gen",
        'registratie_van_biometrische_informatie': "Bio",
        'DPIA_uitgevoerd': "DPIA",
        'verwerkersovereenkomst': 'VO',
        'bevat_persoonsgegevens': 'Persoonsgegevens',
}

admin.site.site_title = 'My site'
admin.site.site_header = 'AVG Register TU Delft'

@admin.action(description="Delete all AVG registerlines!!!")
def deleteAllAVG(modeladmin, request, queryset):
    AVGRegisterline.objects.all().delete()

@admin.register(AVGRegisterline)
#@admin_site.register(AVGRegisterline)
class AVGRegisterlineAdmin(admin.ModelAdmin):

    def reg_label(name):
        labeller = lambda x : getattr( x, name)
        labeller.short_description = labelmap[name]
        labeller.admin_order_field = name
        labeller.boolean = True
        return labeller

    search_fields = ( 'verwerking', 'applicatienaam')
    
    actions = [ deleteAllAVG ]
    list_display_links = ('verwerking', 'applicatienaam',)
    list_display = ( 
        'verwerking', 'applicatienaam', 'inschatting_aantal_betrokkenen',
        reg_label('verwerkersovereenkomst'),
        reg_label('DPIA_uitgevoerd'),
        reg_label('bevat_persoonsgegevens'), 
        reg_label('registratie_van_NAW_gegevens'),
        reg_label('registratie_van_genderinformatie'),
        reg_label('registratie_van_geboortedatum'),
        reg_label('registratie_van_geboorteplaats'),
        reg_label('registratie_van_nationaliteit'),
        reg_label('registratie_van_IBAN_nummer'),
        reg_label('verwerking_van_foto'),
        reg_label('registratie_van_emailadres'),
        reg_label('registratie_van_telefoonnummer'),
        reg_label('registratie_van_identificatiebewijs'),
        reg_label('registratie_van_BSN_nummer'),
        reg_label('registratie_van_studienummer'),
        reg_label('registratie_van_personeelsnummer'),
        reg_label('registratie_van_videobeeldinformatie'),
        reg_label('registratie_van_geluidsinformatie'),
        reg_label('registratie_van_locatie_informatie'),
        reg_label('registratie_van_financiële_informatie'),
        reg_label('registratie_van_burgerlijke_staat'),
        reg_label('registratie_van_gezinssamenstelling'),
        reg_label('registratie_van_lidmaatschap_van_een_vakbond'),
        reg_label('registratie_van_strafrechtelijke_gegevens'),
        reg_label('registratie_van_gezondheidsgegevens'),
        reg_label('registratie_van_opleidingsinformatie'),
        reg_label('registratie_van_functie_informatie'),
        reg_label('registratie_van_seksuele_geaardheid'),
        reg_label('registratie_van_politieke_voorkeur'),
        reg_label('registratie_van_religie'),
        reg_label('registratie_van_genetische_informatie'),
        reg_label('registratie_van_biometrische_informatie'),    
    )
    fieldsets = (
        (None, {
            'fields': (('verwerking', 'applicatienaam'), 'doel_van_de_verwerking', 
                        'rechtmatige_grondslag', ('DPIA_uitgevoerd', 'bevat_persoonsgegevens'), 'opmerkingen')
        }),
        ('Stakeholders', {
            'fields': ( ('eigenaar', 'beheerders'), 
                        ('betrokkenen', 'inschatting_aantal_betrokkenen')),
        }),
        ('Registraties', {
            'classes': ('collapse',),
            'fields': breaksublist( 
                ('registratie_van_NAW_gegevens', 'registratie_van_genderinformatie', 'registratie_van_geboortedatum',
                'registratie_van_geboorteplaats', 'registratie_van_nationaliteit', 'registratie_van_IBAN_nummer',
                'verwerking_van_foto', 'registratie_van_emailadres', 'registratie_van_telefoonnummer',
                'registratie_van_identificatiebewijs', 'registratie_van_BSN_nummer', 'registratie_van_studienummer',
                'registratie_van_personeelsnummer', 'registratie_van_videobeeldinformatie', 'registratie_van_geluidsinformatie',
                'registratie_van_locatie_informatie', 'registratie_van_financiële_informatie', 'registratie_van_burgerlijke_staat',
                'registratie_van_gezinssamenstelling', 'registratie_van_lidmaatschap_van_een_vakbond', 'registratie_van_strafrechtelijke_gegevens',
                'registratie_van_gezondheidsgegevens', 'registratie_van_opleidingsinformatie', 'registratie_van_functie_informatie',
                'registratie_van_seksuele_geaardheid', 'registratie_van_politieke_voorkeur', 'registratie_van_religie',
                'registratie_van_genetische_informatie', 'registratie_van_biometrische_informatie',),                
                3) + ('andere_categorieën_persoonsgegevens',),            
        }),
        ('Verwerking', {
            'fields': ( ('naam_verwerker', 'ontvangers',),
                        ('in_welke_landen_worden_de_gegevens_verwerkt', 'vestigingsland_van_de_verwerker'),
                    'bewaartermijn', 'beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen',
                    'bron_waar_de_gegevens_worden_verkregen')
        }),
        ('Opslag', {
            'fields': ( 'naam_opslagmedium', )
        })
    )
    list_filter = ( 'bevat_persoonsgegevens', 'DPIA_uitgevoerd', 'verwerkersovereenkomst', 'inschatting_aantal_betrokkenen')

    empty_value_display = '-'

@admin.register(SharepointExcelFile)
class SharepointExcelFileAdmin(admin.ModelAdmin):
    list_display = ( 'uploaded', )