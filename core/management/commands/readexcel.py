from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import AVGRegisterline

import pandas as pd
import re


def excelboolean(excelvalue):
    if excelvalue in ['Ja', 'ja']:
        return True
    elif excelvalue in ['Nee', 'nee']:
        return False
    else:
        return None

def cleanup(dataframe):
    dataframe["Verwerking"].replace({"": "-"}, inplace=True)
    dataframe["Applicatienaam"].replace({"": "-"}, inplace=True)

    dataframe['Applicatienaam'] = dataframe['Applicatienaam'].map(lambda x: re.sub(r';#.*', '', x))
    dataframe['Naam opslagmedium'] = dataframe['Naam opslagmedium'].map(lambda x: re.sub(r'#?\d+;#', '', x))
    dataframe['Betrokkenen'] = dataframe['Betrokkenen'].map(lambda x: re.sub(r'#', '', x))

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('excelfile', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print("Doing it")
        data = pd.read_excel(options['excelfile'])
        data.replace(pd.NA, '', inplace=True, regex=True)

        cleanup(data)

        for index, row in data.iterrows():   
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
            avg.registratie_van_NAW_gegevens = excelboolean(row['Registratie van NAW-gegevens'])
            avg.registratie_van_genderinformatie = excelboolean(row['Registratie van genderinformatie'])
            avg.registratie_van_geboortedatum = excelboolean(row['Registratie van geboortedatum'])
            avg.registratie_van_geboorteplaats = excelboolean(row['Registratie van geboorteplaats'])
            avg.registratie_van_nationaliteit = excelboolean(row['Registratie van nationaliteit'])
            avg.registratie_van_IBAN_nummer = excelboolean(row['Registratie van IBAN-nummer'])
            avg.verwerking_van_foto = excelboolean(row['Verwerking van foto'])
            avg.registratie_van_emailadres = excelboolean(row['Registratie van e-mailadres'])
            avg.registratie_van_telefoonnummer = excelboolean(row['Registratie van telefoonnummer'])
            avg.registratie_van_identificatiebewijs = excelboolean(row['Registratie van identificatiebewijs'])
            avg.registratie_van_BSN_nummer = excelboolean(row['Registratie van BSN-nummer'])
            avg.registratie_van_studienummer = excelboolean(row['Registratie van studienummer'])
            avg.registratie_van_personeelsnummer = excelboolean(row['Registratie van personeelsnummer'])
            avg.registratie_van_videobeeldinformatie = excelboolean(row['Registratie van videobeeldinformatie'])
            avg.registratie_van_geluidsinformatie = excelboolean(row['Registratie van geluidsinformatie'])
            avg.registratie_van_locatie_informatie = excelboolean(row['Registratie van locatie-informatie'])
            avg.registratie_van_financiële_informatie = excelboolean(row['Registratie van financiële informatie'])
            avg.registratie_van_burgerlijke_staat = excelboolean(row['Registratie van burgerlijke staat'])
            avg.registratie_van_gezinssamenstelling = excelboolean(row['Registratie van gezinssamenstelling'])
            avg.registratie_van_lidmaatschap_van_een_vakbond = excelboolean(row['Registratie van lidmaatschap van een vakbond'])
            avg.registratie_van_strafrechtelijke_gegevens = excelboolean(row['Registratie van strafrechtelijke gegevens'])
            avg.registratie_van_gezondheidsgegevens = excelboolean(row['Registratie van gezondheidsgegevens'])
            avg.registratie_van_opleidingsinformatie = excelboolean(row['Registratie van opleidingsinformatie'])
            avg.registratie_van_functie_informatie = excelboolean(row['Registratie van functie-informatie'])
            avg.registratie_van_seksuele_geaardheid = excelboolean(row['Registratie van seksuele geaardheid'])
            avg.registratie_van_politieke_voorkeur = excelboolean(row['Registratie van politieke voorkeur'])
            avg.registratie_van_religie = excelboolean(row['Registratie van religie'])
            avg.registratie_van_genetische_informatie = excelboolean(row['Registratie van genetische informatie'])
            avg.registratie_van_biometrische_informatie = excelboolean(row['Registratie van biometrische informatie'])
            avg.andere_categorieën_persoonsgegevens = row['Eventueel andere categorieën persoonsgegevens indien deze geregistreerd worden']
            avg.naam_verwerker = row['Naam (sub)verwerker(s)']
            avg.verwerkersovereenkomst = excelboolean(row['Is er een verwerkersovereenkomst?'])
            avg.ontvangers = row['Ontvangers']
            avg.in_welke_landen_worden_de_gegevens_verwerkt = row['In welk(e) land(en) worden de gegevens verwerkt?']
            avg.vestigingsland_van_de_verwerker = row['Wat is het vestigingsland van de (sub)verwerker?']
            avg.bewaartermijn = row['Bewaartermijn']
            avg.beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen = row['Beveiligingsmaatregelen die genomen worden om de gegevens te beveiligen']
            avg.bron_waar_de_gegevens_worden_verkregen = row['Bron waar de gegevens worden verkregen']
            avg.DPIA_uitgevoerd = excelboolean(row['Is er een DPIA uitgevoerd?'])
            avg.bevat_persoonsgegevens = excelboolean(row['Bevat persoonsgegevens'])

            avg.save()
