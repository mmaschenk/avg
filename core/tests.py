from django.test import TestCase
from core.models import AVGRegisterline as AVGR
# Create your tests here.

class AVGRegisterlineTestCase(TestCase):
  def setUp(self):
    AVGR.objects.create(verwerking='Uitgifte van passen voor de laadpalen', 
      applicatienaam='EV-Box', 
      naam_opslagmedium="cloud",)
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='MyOTA')
    AVGR.objects.create(verwerking='Toegangsbeheer', applicatienaam='CardsOnLine')
    pass

  def test_avgline(self):
    evbox = AVGR.objects.get(applicatienaam='EV-Box')
    self.assertEqual(evbox.verwerking, 'Uitgifte van passen voor de laadpalen' )

  def test_multiple_get(self):
    try:
      toegangsbeheer = AVGR.objects.get(verwerking='Toegangsbeheer')
      self.fail("Should be multiple records")
    except AVGR.MultipleObjectsReturned:
      pass
    
  
