import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luodun_kassapaatteen_rahamaara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_luodussa_kassapaatteessa_ei_myytyja_edullisia_lounaita(self):
        self.assertEqual(self.kassapaate.myytyjen_edullisten_lounaiden_lkm(), 0)

    def test_luodussa_kassapaatteessa_ei_myytyja_maukkaita_lounaita(self):
        self.assertEqual(self.kassapaate.myytyjen_maukkaiden_lounaiden_lkm(), 0)

    def test_syo_edullisesti_kateisella_lisaa_rahaa_kassaan_oikean_maaran(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_syo_maukkaasti_kateisella_lisaa_rahaa_kassaan_oikean_maaran(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)

    def test_syo_edullisesti_kateisella_palauttaa_oikean_vaihtorahan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_syo_maukkaasti_kateisella_palauttaa_oikean_vaihtorahan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_syo_edullisesti_kateisella_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.myytyjen_edullisten_lounaiden_lkm(), 1)

    def test_syo_maukkaasti_kateisella_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.myytyjen_maukkaiden_lounaiden_lkm(), 1)

    def test_syo_edullisesti_kateisella_ei_epaonnistuessaan_lisaa_kassaan_rahaa(self):
        self.kassapaate.syo_edullisesti_kateisella(235)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_syo_maukkaasti_kateisella_ei_epaonnistuessaan_lisaa_kassaan_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(395)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_syo_edullisesti_kateisella_palauttaa_rahat_epaonnistuessaan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(235), 235)

    def test_syo_maukkaasti_kateisella_palauttaa_rahat_epaonnistuessaan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(395), 395)

    def test_syo_edullisesti_kateisella_ei_epaonnistuessaan_muuta_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(235)

        self.assertEqual(self.kassapaate.myytyjen_edullisten_lounaiden_lkm(), 0)

    def test_syo_maukkaasti_kateisella_ei_epaonnistuessaan_muuta_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(395)

        self.assertEqual(self.kassapaate.myytyjen_maukkaiden_lounaiden_lkm(), 0)

    def test_syo_edullisesti_kortilla_veloittaa_oikean_summan(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 34.85)

    def test_syo_maukkaasti_kortilla_veloittaa_oikean_summan(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 33.25)

    def test_syo_edullisesti_kortilla_palauttaa_onnistuessaan_tosi(self):
        maksukortti = Maksukortti(3725)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), True)

    def test_syo_maukkaasti_kortilla_palauttaa_onnistuessaan_tosi(self):
        maksukortti = Maksukortti(3725)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), True)

    def test_syo_edullisesti_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.myytyjen_edullisten_lounaiden_lkm(), 1)

    def test_syo_maukkaasti_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.myytyjen_maukkaiden_lounaiden_lkm(), 1)

    def test_syo_edullisesti_kortilla_ei_epaonnistuessaan_veloita_mitaan(self):
        maksukortti = Maksukortti(235)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 2.35)

    def test_syo_maukkaasti_kortilla_ei_epaonnistuessaan_veloita_mitaan(self):
        maksukortti = Maksukortti(395)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(maksukortti.saldo_euroina(), 3.95)

    def test_syo_edullisesti_kortilla_ei_epaonnistuessaan_muuta_myytyjen_lounaiden_maaraa(self):
        maksukortti = Maksukortti(235)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.myytyjen_edullisten_lounaiden_lkm(), 0)

    def test_syo_maukkaasti_kortilla_ei_epaonnistuessaan_muuta_myytyjen_lounaiden_maaraa(self):
        maksukortti = Maksukortti(395)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.myytyjen_maukkaiden_lounaiden_lkm(), 0)

    def test_syo_edullisesti_kortilla_palauttaa_epaonnistuessaan_epatosi(self):
        maksukortti = Maksukortti(235)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), False)

    def test_syo_maukkaasti_kortilla_palauttaa_epaonnistuessaan_epatosi(self):
        maksukortti = Maksukortti(395)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), False)

    def test_syo_edullisesti_kortilla_ei_vaikuta_kassan_rahamaaraan(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_syo_maukkaasti_kortilla_ei_vaikuta_kassan_rahamaaraan(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_rahan_lataaminen_kortille_kasvattaa_sen_saldoa_oikein(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 1000)

        self.assertEqual(maksukortti.saldo_euroina(), 47.25)

    def test_rahan_lataaminen_kortille_lisaa_kassaan_oikean_maaran_rahaa(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1010.0)

    def test_negatiivisen_rahasumman_lataaminen_kortille_ei_onnistu(self):
        maksukortti = Maksukortti(3725)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -100)

        self.assertEqual(maksukortti.saldo_euroina(), 37.25)
