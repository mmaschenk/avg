from django.db import models
from django.db.models.fields import CharField

from django.db.utils import IntegrityError
from datetime import datetime
import pandas as pd
import re

# Create your models here.

class AVGRegisterline(models.Model):
    verwerking = models.CharField(null=True, max_length=256)
    applicatienaam = models.CharField(max_length=256)
    naam_opslagmedium = models.CharField(max_length=256)
    doel_van_de_verwerking = models.TextField()
    rechtmatige_grondslag = models.CharField(max_length=256)
    opmerkingen = models.TextField()
    eigenaar = models.CharField(max_length=256)
    beheerders = models.CharField(max_length=256)
    betrokkenen = models.CharField(max_length=256)
    inschatting_aantal_betrokkenen = models.CharField("# betrokkenen", max_length=256)
    registratie_van_NAW_gegevens = models.BooleanField(null=True)
    registratie_van_genderinformatie = models.BooleanField(null=True)
    registratie_van_geboortedatum = models.BooleanField(null=True)
    registratie_van_geboorteplaats = models.BooleanField(null=True)
    registratie_van_nationaliteit = models.BooleanField(null=True)
    registratie_van_IBAN_nummer = models.BooleanField(null=True)
    verwerking_van_foto = models.BooleanField(null=True)
    registratie_van_emailadres = models.BooleanField(null=True)
    registratie_van_telefoonnummer = models.BooleanField(null=True)
    registratie_van_identificatiebewijs = models.BooleanField(null=True)
    registratie_van_BSN_nummer = models.BooleanField(null=True)
    registratie_van_studienummer = models.BooleanField(null=True)
    registratie_van_personeelsnummer = models.BooleanField(null=True)
    registratie_van_videobeeldinformatie = models.BooleanField(null=True)
    registratie_van_geluidsinformatie = models.BooleanField(null=True)
    registratie_van_locatie_informatie = models.BooleanField(null=True)
    registratie_van_financiële_informatie = models.BooleanField(null=True)
    registratie_van_burgerlijke_staat = models.BooleanField(null=True)
    registratie_van_gezinssamenstelling = models.BooleanField(null=True)
    registratie_van_lidmaatschap_van_een_vakbond = models.BooleanField(null=True)
    registratie_van_strafrechtelijke_gegevens = models.BooleanField(null=True)
    registratie_van_gezondheidsgegevens = models.BooleanField(null=True)
    registratie_van_opleidingsinformatie = models.BooleanField(null=True)
    registratie_van_functie_informatie = models.BooleanField(null=True)
    registratie_van_seksuele_geaardheid = models.BooleanField(null=True)
    registratie_van_politieke_voorkeur = models.BooleanField(null=True)
    registratie_van_religie = models.BooleanField(null=True)
    registratie_van_genetische_informatie = models.BooleanField(null=True)
    registratie_van_biometrische_informatie = models.BooleanField(null=True)
    andere_categorieën_persoonsgegevens = models.TextField()
    naam_verwerker = models.CharField(max_length=256)
    verwerkersovereenkomst = models.BooleanField(null=True)
    ontvangers = models.CharField(max_length=256)
    in_welke_landen_worden_de_gegevens_verwerkt = models.CharField(max_length=256)
    vestigingsland_van_de_verwerker = models.CharField(max_length=256)
    bewaartermijn = models.TextField()
    beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen = models.TextField(db_column="beveiligingsmaatregelen")
    bron_waar_de_gegevens_worden_verkregen = models.CharField(max_length=256)
    DPIA_uitgevoerd = models.BooleanField(null=True)
    bevat_persoonsgegevens = models.BooleanField(null=True)

    def __str__(self):
        return "{}@{} [{}]".format(self.verwerking,self.applicatienaam, self.id)

class ExternalReference(models.Model):
    source = models.CharField(max_length=64)
    sourcekey = models.CharField(max_length=128)
    avgregisterline = models.ForeignKey(AVGRegisterline, on_delete=models.CASCADE)

    def __str__(self):
        return "{}:{} -> {}".format(self.source, self.sourcekey, self.avgregisterline)

class SharepointExcelFile(models.Model):
    data = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        adding = self._state.adding
        super(SharepointExcelFile, self).save(*args, **kwargs)
        filename = self.data.url        
        print(self._state.adding)
        if adding:
            print("Handling: ", filename)
            self.processexcel()
            self.processedtime = datetime.now();

    @staticmethod
    def excelboolean(excelvalue):
        if excelvalue in ['Ja', 'ja']:
            return True
        elif excelvalue in ['Nee', 'nee']:
            return False
        else:
            return None
    
    @staticmethod
    def cleanup(dataframe):
        dataframe["Verwerking"].replace({"": "-"}, inplace=True)
        dataframe["Applicatienaam"].replace({"": "-"}, inplace=True)

        dataframe['Applicatienaam'] = dataframe['Applicatienaam'].map(lambda x: re.sub(r';#.*', '', x))
        dataframe['Naam opslagmedium'] = dataframe['Naam opslagmedium'].map(lambda x: re.sub(r'#?\d+;#', '', x))
        dataframe['Betrokkenen'] = dataframe['Betrokkenen'].map(lambda x: re.sub(r'#', '', x))

    def processexcel(self):
        data = pd.read_excel(self.data.file)
        data.replace(pd.NA, '', inplace=True, regex=True)

        self.cleanup(data)

        print("What?")
        for index, row in data.iterrows():
            print('Processing row {}'.format(index))

            print('V: [{}] and [{}]'.format(row['Verwerking'],row['Applicatienaam']))

            if row['Verwerking'] == "-" and row['Applicatienaam'] == "-":
                continue

            avg = AVGRegisterline()
            avg.verwerking = row['Verwerking']
            avg.applicatienaam = row['Applicatienaam']
            avg.naam_opslagmedium = row['Naam opslagmedium']
            avg.doel_van_de_verwerking = row['Doel van de verwerking']
            avg.rechtmatige_grondslag = row['Rechtmatige grondslag']
            avg.opmerkingen = row['Opmerkingen']
            avg.eigenaar = row['Eigenaar']
            avg.beheerders = row['Beheerder(s)']
            avg.betrokkenen = row['Betrokkenen']
            avg.inschatting_aantal_betrokkenen = row['Inschatting aantal betrokkenen']
            avg.registratie_van_NAW_gegevens = self.excelboolean(row['Registratie van NAW-gegevens'])
            avg.registratie_van_genderinformatie = self.excelboolean(row['Registratie van genderinformatie'])
            avg.registratie_van_geboortedatum = self.excelboolean(row['Registratie van geboortedatum'])
            avg.registratie_van_geboorteplaats = self.excelboolean(row['Registratie van geboorteplaats'])
            avg.registratie_van_nationaliteit = self.excelboolean(row['Registratie van nationaliteit'])
            avg.registratie_van_IBAN_nummer = self.excelboolean(row['Registratie van IBAN-nummer'])
            avg.verwerking_van_foto = self.excelboolean(row['Verwerking van foto'])
            avg.registratie_van_emailadres = self.excelboolean(row['Registratie van e-mailadres'])
            avg.registratie_van_telefoonnummer = self.excelboolean(row['Registratie van telefoonnummer'])
            avg.registratie_van_identificatiebewijs = self.excelboolean(row['Registratie van identificatiebewijs'])
            avg.registratie_van_BSN_nummer = self.excelboolean(row['Registratie van BSN-nummer'])
            avg.registratie_van_studienummer = self.excelboolean(row['Registratie van studienummer'])
            avg.registratie_van_personeelsnummer = self.excelboolean(row['Registratie van personeelsnummer'])
            avg.registratie_van_videobeeldinformatie = self.excelboolean(row['Registratie van videobeeldinformatie'])
            avg.registratie_van_geluidsinformatie = self.excelboolean(row['Registratie van geluidsinformatie'])
            avg.registratie_van_locatie_informatie = self.excelboolean(row['Registratie van locatie-informatie'])
            avg.registratie_van_financiële_informatie = self.excelboolean(row['Registratie van financiële informatie'])
            avg.registratie_van_burgerlijke_staat = self.excelboolean(row['Registratie van burgerlijke staat'])
            avg.registratie_van_gezinssamenstelling = self.excelboolean(row['Registratie van gezinssamenstelling'])
            avg.registratie_van_lidmaatschap_van_een_vakbond = self.excelboolean(row['Registratie van lidmaatschap van een vakbond'])
            avg.registratie_van_strafrechtelijke_gegevens = self.excelboolean(row['Registratie van strafrechtelijke gegevens'])
            avg.registratie_van_gezondheidsgegevens = self.excelboolean(row['Registratie van gezondheidsgegevens'])
            avg.registratie_van_opleidingsinformatie = self.excelboolean(row['Registratie van opleidingsinformatie'])
            avg.registratie_van_functie_informatie = self.excelboolean(row['Registratie van functie-informatie'])
            avg.registratie_van_seksuele_geaardheid = self.excelboolean(row['Registratie van seksuele geaardheid'])
            avg.registratie_van_politieke_voorkeur = self.excelboolean(row['Registratie van politieke voorkeur'])
            avg.registratie_van_religie = self.excelboolean(row['Registratie van religie'])
            avg.registratie_van_genetische_informatie = self.excelboolean(row['Registratie van genetische informatie'])
            avg.registratie_van_biometrische_informatie = self.excelboolean(row['Registratie van biometrische informatie'])
            avg.andere_categorieën_persoonsgegevens = row['Eventueel andere categorieën persoonsgegevens indien deze geregistreerd worden']
            avg.naam_verwerker = row['Naam (sub)verwerker(s)']
            avg.verwerkersovereenkomst = self.excelboolean(row['Is er een verwerkersovereenkomst?'])
            avg.ontvangers = row['Ontvangers']
            avg.in_welke_landen_worden_de_gegevens_verwerkt = row['In welk(e) land(en) worden de gegevens verwerkt?']
            avg.vestigingsland_van_de_verwerker = row['Wat is het vestigingsland van de (sub)verwerker?']
            avg.bewaartermijn = row['Bewaartermijn']
            avg.beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen = row['Beveiligingsmaatregelen die genomen worden om de gegevens te beveiligen']
            avg.bron_waar_de_gegevens_worden_verkregen = row['Bron waar de gegevens worden verkregen']
            avg.DPIA_uitgevoerd = self.excelboolean(row['Is er een DPIA uitgevoerd?'])
            avg.bevat_persoonsgegevens = self.excelboolean(row['Bevat persoonsgegevens'])

            avg.save()
            
        return index

