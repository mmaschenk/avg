from .models import AVGRegisterline, ExternalReference
from rest_framework import serializers
from rest_framework.utils import model_meta
from collections import OrderedDict

class AVGRegisterlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AVGRegisterline
        fields = '__all__'
        exclude = [ ]
        read_only_fields = []

class EmbeddedAVGRegisterlineSerializer(AVGRegisterlineSerializer):
    id = serializers.IntegerField(label='ID', required=False)

    def create(self, validated_data):
        print("Also creating", validated_data)
        try:
            ex = AVGRegisterline.objects.get(id=validated_data['id'])
            self._created = False
        except:
            print("Couldn't")
            ex = AVGRegisterline(**validated_data)
            self._created = True
        return ex

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr not in info.relations:
                setattr(instance, attr, value)

        instance.save()
        return instance
        raise NotImplementedError('`update()` must be implemented.')

class SkipField(Exception):
    pass

class ExternalReferenceSerializer(serializers.ModelSerializer):
    avgregisterline = EmbeddedAVGRegisterlineSerializer()
    #id = serializers.IntegerField(label='ID', required=False)

    def create(self, validated_data):
        ex = ExternalReference(source=source, sourcekey=sourcekey, avgregisterline=avgregisterline)
        
        return ex

    class Meta:
        model = ExternalReference
        fields = '__all__'

    
"""
        prut = {
        "verwerking": "Ziekteverzuim administratie",
  "applicatienaam": "VerzuimXpert",
  "naam_opslagmedium": "",
  "doel_van_de_verwerking": "Ziekteverzuim  applicatie voor de bedrijfsartsen t.b.v. Wet Poortwachter",
  "rechtmatige_grondslag": "Wettelijke basis",
  "opmerkingen": "Alleen  toegang tot gegevens mits geautoriseerd. Splitsen",
  "eigenaar": "Directeur HR",
  "beheerders": "IM HR",
  "betrokkenen": "Medewerkers",
  "inschatting_aantal_betrokkenen": "5000 - 10.000",
  "registratie_van_NAW_gegevens": true,
  "registratie_van_genderinformatie": true,
  "registratie_van_geboortedatum": true,
  "registratie_van_geboorteplaats": false,
  "registratie_van_nationaliteit": false,
  "registratie_van_IBAN_nummer": false,
  "verwerking_van_foto": false,
  "registratie_van_emailadres": null,
  "registratie_van_telefoonnummer": null,
  "registratie_van_identificatiebewijs": false,
  "registratie_van_BSN_nummer": false,
  "registratie_van_studienummer": false,
  "registratie_van_personeelsnummer": true,
  "registratie_van_videobeeldinformatie": false,
  "registratie_van_geluidsinformatie": false,
  "registratie_van_locatie_informatie": false,
  "registratie_van_financiële_informatie": false,
  "registratie_van_burgerlijke_staat": false,
  "registratie_van_gezinssamenstelling": false,
  "registratie_van_lidmaatschap_van_een_vakbond": false,
  "registratie_van_strafrechtelijke_gegevens": false,
  "registratie_van_gezondheidsgegevens": true,
  "registratie_van_opleidingsinformatie": false,
  "registratie_van_functie_informatie": false,
  "registratie_van_seksuele_geaardheid": false,
  "registratie_van_politieke_voorkeur": false,
  "registratie_van_religie": false,
  "registratie_van_genetische_informatie": false,
  "registratie_van_biometrische_informatie": false,
  "andere_categorieën_persoonsgegevens": "",
  "naam_verwerker": "Otherside at Work (voorheen Empirion)",
  "verwerkersovereenkomst": true,
  "ontvangers": "",
  "in_welke_landen_worden_de_gegevens_verwerkt": "Nederland",
  "vestigingsland_van_de_verwerker": "Nederland",
  "bewaartermijn": "Vernietigen na 5 jaar 77/062",
  "beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen": "",
  "bron_waar_de_gegevens_worden_verkregen": "",
  "DPIA_uitgevoerd": null,
  "bevat_persoonsgegevens": true}
"""

