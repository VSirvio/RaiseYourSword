import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_on_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_kortin_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(2571)

        self.assertEqual(self.maksukortti.saldo_euroina(), 35.71)

    def test_rahan_ottaminen_vahentaa_saldoa_oikein(self):
        self.maksukortti.ota_rahaa(528)

        self.assertEqual(self.maksukortti.saldo_euroina(), 4.72)

    def test_rahan_ottaminen_ei_vaikuta_saldoon_jos_saldo_ei_riita(self):
        self.maksukortti.ota_rahaa(1001)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_onnistunut_rahan_ottaminen_palauttaa_tosi(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1000), True)

    def test_epaonnistunut_rahan_ottaminen_palauttaa_epatosi(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1001), False)
