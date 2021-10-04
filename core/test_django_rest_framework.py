from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from django.test import TestCase

from core.models import AVGRegisterline as AVGR
# Create your tests here.

class AVGRegisterlineRestTestCase(TestCase):
  def setUp(self):  
    AVGR.objects.create(verwerking='Uitgifte van passen voor de laadpalen', applicatienaam='EV-Box')    
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='MyOTA')
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='CardsOnLine')
    
    pass

  
class AVGRegisterlineApiTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create(username='admin')
    AVGR.objects.create(verwerking='Uitgifte van passen voor de laadpalen', 
      applicatienaam='EV-Box', 
      naam_opslagmedium="cloud",
      doel_van_de_verwerking="registratie van kaarten die uitgegeven worden aan personen die daarmee hun auto kunnen opladen bij een laadpaal. ",
      rechtmatige_grondslag="Gerechtvaardigd belang",
      opmerkingen="geen",
      eigenaar="Directeur CRE",
      beheerders="IM CRE",
      betrokkenen="Medewerkers",
      inschatting_aantal_betrokkenen="1 - 500",
      registratie_van_NAW_gegevens=True,
      registratie_van_genderinformatie=False,
      registratie_van_geboortedatum=False,
      registratie_van_geboorteplaats=False,
      registratie_van_nationaliteit=False,
      registratie_van_IBAN_nummer=False,
      verwerking_van_foto=False,
      registratie_van_emailadres=False,
      registratie_van_telefoonnummer=None,
      registratie_van_identificatiebewijs=False,
      registratie_van_BSN_nummer=False,
      registratie_van_studienummer=False,
      registratie_van_personeelsnummer=False,
      registratie_van_videobeeldinformatie=False,
      registratie_van_geluidsinformatie=False,
      registratie_van_locatie_informatie=False,
      registratie_van_financiële_informatie=False,
      registratie_van_burgerlijke_staat=False,
      registratie_van_gezinssamenstelling=False,
      registratie_van_lidmaatschap_van_een_vakbond=False,
      registratie_van_strafrechtelijke_gegevens=False,
      registratie_van_gezondheidsgegevens=False,
      registratie_van_opleidingsinformatie=False,
      registratie_van_functie_informatie=False,
      registratie_van_seksuele_geaardheid=False,
      registratie_van_politieke_voorkeur=False,
      registratie_van_religie=False,
      registratie_van_genetische_informatie=False,
      registratie_van_biometrische_informatie=False,
      andere_categorieën_persoonsgegevens="nvt",
      naam_verwerker="EV-Box",
      verwerkersovereenkomst=None,
      ontvangers="nvt",
      in_welke_landen_worden_de_gegevens_verwerkt="Nederland",
      vestigingsland_van_de_verwerker="Nederland",
      bewaartermijn="",
      beveiligingsmaatregelen_die_genomen_worden_om_de_gegevens_te_beveiligen="Inloggen via wachtwoord en inlognaam. Bij select gezelschap beheerders belegd.",
      bron_waar_de_gegevens_worden_verkregen="Functioneel beheerder",
      DPIA_uitgevoerd=None,
      bevat_persoonsgegevens=True,
    )
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='MyOTA')
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='CardsOnLine')
    self.client.force_authenticate(user=self.user)

  def test_avglines(self):
    response = self.client.get("/api/avgregisterline/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 3)

  def test_avgline(self):
    response = self.client.get("/api/avgregisterline/1/", format='json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.data['applicatienaam'], 'EV-Box')
    print(response.data)

    print(response.content)
