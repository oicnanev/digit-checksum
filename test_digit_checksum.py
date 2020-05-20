""" ############################################################################
 ISEL - Instituto Superior de Engenharia de Lisboa.

 LEIC - Licenciatura em Engenharia Informatica e de Computadores.

 Com  - Comunicações.

 Trabalho Prático - Módulo 2
 32398 Hélder Augusto
 39619 Fábio Teixeira
 45824 Nuno Venâncio

 digit_checksum.py
############################################################################ """

import unittest
from digit_checksum import ChecksumController as Controller


class TestDigitChecksum(unittest.TestCase):
    """
    Test class that extends from the unittest.TestCase class

    Performs tests to assert all algorithms are correct
    Modify the numbers to test your own cards, bank account numbers os ISBNs

    To see more details, run in windows command line 'python -m unittest -v'
    or on linux terminal 'python3 -m unittest -v'
    """
    def setUp(self):
        self.c = Controller()

    # ######################## BILHETE DE IDENTIDADE ###########################
    # Generate Checksum tests --------------------------------------------------
    def test_bilhete_identidade_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g1', '11240601'), '7')

    def test_bilhete_identidade_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g1', '112-40-60-1'), '7')

    def test_bilhete_identidade_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g1', '11240501'), '7')

    def test_bilhete_identidade_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g1', '11240061'), '7')

    # Validate Checksum tests --------------------------------------------------
    def test_bilhete_identidade_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v1', '112406017'), True)

    def test_bilhete_identidade_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v1', '112-40-60-1 7'), True)

    def test_bilhete_identidade_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v1', '11240501 7'), True)

    def test_bilhete_identidade_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v1', '112400617'), True)

    # ######################### CONTRIBUINTE (NIF) #############################
    # Generate Checksum tests --------------------------------------------------
    def test_nif_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g1', '20990796'), '7')

    def test_nif_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g1', '209-90-79-6'), '7')

    def test_nif_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g1', '20990797'), '7')

    def test_nif_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g1', '20990769'), '7')

    # Validate Checksum tests --------------------------------------------------
    def test_nif_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v1', '209907967'), True)

    def test_nif_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v1', '209-90-79-6 7'), True)

    def test_nif_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v1', '20990797 7'), True)

    def test_nif_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v1', '209907697'), True)

    # ##################### LISBOA VIVA (passe social) #########################
    # Generate Checksum tests --------------------------------------------------
    def test_lisboa_viva_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g1', '00003230'), '1')

    def test_lisboa_viva_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g1', '000-03-23-0'), '1')

    def test_lisboa_viva_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g1', '10003230'), '1')

    def test_lisboa_viva_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g1', '00003203'), '1')

    # Validate Checksum tests --------------------------------------------------
    def test_lisboa_viva_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v1', '000032301'), True)

    def test_lisboa_viva_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v1', '000-03-23-0 1'), True)

    def test_lisboa_viva_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v1', '00003238 1'), True)

    def test_lisboa_viva_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v1', '000032031'), True)

    # ########################### CARTÃO CIDADÃO ###############################
    # Generate Checksum tests --------------------------------------------------
    def test_cartao_cidadao_generate_correct_numbers_format(self):
        # the '€' character was choosed to separate the card number from the
        # number of renews of that card, '€2' means we have the 3rd card
        self.assertEqual(self.c.process('g2', '11240601€2'), '7zx5')

    def test_cartao_cidadao_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g2', '112-40-60-1€2'), '7zx5')

    def test_cartao_cidadao_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g2', '11240602€2'), '7zx5')

    def test_cartao_cidadao_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g2', '11240610€2'), '7zx5')

    # Validate Checksum tests --------------------------------------------------
    def test_cartao_cidadao_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v2', '112406017zx5'), True)

    def test_cartao_cidadao_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v2', '11240601-7zx5'), True)

    def test_cartao_cidadao_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v2', '112406018zx5'), True)

    def test_cartao_cidadao_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v2', '112406071zx5'), True)

    # ############################### BAR CODE #################################
    # Generate Checksum tests --------------------------------------------------
    def test_bar_code_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g3', '560131209186'), '8')

    def test_bar_code_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g3', '5-601312-09186'), '8')

    def test_bar_code_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g3', '560131209187'), '8')

    def test_bar_code_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g3', '560131209168'), '8')

    # Validate Checksum tests --------------------------------------------------
    def test_bar_code_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v3', '5601312091868'), True)

    def test_bar_code_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v3', '5-601312-09186-8'), True)

    def test_bar_code_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v3', '5601312091878'), True)

    def test_bar_code_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v3', '5601312091688'), True)

    # ######### GENERIC 13 DIGITS CARD (Cartão Modelo / Continente) ############
    # Generate Checksum tests --------------------------------------------------
    def test_generic_card_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g3', '185018632278'), '1')

    def test_generic_card_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g3', '185-018-632-278'), '1')

    def test_generic_card_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g3', '185018632274'), '1')

    def test_generic_card_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g3', '185018632287'), '1')

    # Validate Checksum tests --------------------------------------------------
    def test_generic_card_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v3', '1850186322781'), True)

    def test_generic_card_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v3', '185-018-632-2781'), True)

    def test_generic_card_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v3', '1850186322741'), True)

    def test_generic_card_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v3', '1850186322871'), True)

    # ########################## SEGURANÇA SOCIAL ##############################
    # Generate Checksum tests --------------------------------------------------
    def test_seg_social_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g4', '1119538684'), '9')

    def test_seg_social_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g4', '1119 5386 84'), '9')

    def test_seg_social_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g4', '1119538685'), '9')

    def test_seg_social_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g4', '1119538648'), '9')

    # Validate Checksum tests --------------------------------------------------
    def test_seg_social_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v4', '11195386849'), True)

    def test_seg_social_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v4', '1119 5386 84 9'), True)

    def test_seg_social_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v4', '11195386859'), True)

    def test_seg_social_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v4', '11195386859'), True)

    # ######################## CREDIT / DEBIT CARDS ############################
    # Generate Checksum tests --------------------------------------------------
    def test_bank_card_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g5', '406170002779066'), '9')

    def test_bank_card_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g5', '4061 7000 2779 066'), '9')

    def test_bank_card_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g5', '406170002779069'), '9')

    def test_bank_card_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g5', '406170002779606'), '9')

    # Validate Checksum tests --------------------------------------------------
    def test_bank_card_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v5', '4061700027790669'), True)

    def test_bank_card_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v5', '4061 7000 2779 0669'), True)

    def test_bank_card_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v5', '4061700027790699'), True)

    def test_bank_card_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v5', '4061700027796069'), True)

    # ################ NÚMERO DE INFORMAÇÃO BANCÁRIA (NIB) ######################
    # Generate Checksum tests --------------------------------------------------
    def test_nib_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g6', '0035008300034799200'), '53')

    def test_nib_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g6', '0035 0083 0003 4799 200'), '53')

    def test_nib_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g6', '0035008300034799201'), '53')

    def test_nib_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g6', '0035008300034792900'), '53')

    # Validate Checksum tests --------------------------------------------------
    def test_nib_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v6', '003500830003479920053'), True)

    def test_nib_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v6', '0035 0083 0003 4799 200 53'), True)

    def test_nib_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v6', '003500830003479920153'), True)

    def test_nib_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v6', '003500830003479290043'), True)

    # ############# INTERNATIONAL BANK ACCOUNT NUMBER (IBAN) ###################
    # Generate Checksum tests --------------------------------------------------
    def test_iban_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g7', 'pt500035008300034799200'), '53')

    def test_iban_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g7', 'pt50 0035 0083 0003 4799 200'), '53')

    def test_iban_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g7', 'pt500035008300034799201'), '53')

    def test_iban_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g7', 'pt500035008300034792900'), '53')

    # Validate Checksum tests --------------------------------------------------
    def test_iban_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v7', 'pt50003500830003479920053'), True)

    def test_iban_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v7', 'pt50 0035 0083 0003 4799 200 53'), True)

    def test_iban_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v7', 'pt50003500830003479920153'), True)

    def test_iban_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v7', 'pt50003500830003479290043'), True)

    # ############ INTERNATIONAL STANDARD BOOK NUMBER 13 (ISBN-13)  ############
    # Generate Checksum tests --------------------------------------------------
    def test_isbn13_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g8', '978-0-13-235088'), '4')

    def test_isbn13_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g8', 'ISBN-13: 978-0-13-235088'), '4')

    def test_isbn13_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g8', '978-0-13-235080'), '4')

    def test_isbn13_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g8', '978-0-13-235808'), '4')

    # Validate Checksum tests --------------------------------------------------
    def test_isbn13_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v8', '978-0-13-235088-4'), True)

    def test_isbn13_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v8', 'ISBN-13: 978-0-13-235088-4'), True)

    def test_isbn13_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v8', '978-0-13-235080-4'), True)

    def test_isbn13_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v8', '978-0-13-235808-4'), True)

    # ##### INTERNATIONAL STANDARD BOOK NUMBER 10 (ISBN-10) no X character #####
    # Generate Checksum tests --------------------------------------------------
    def test_isbn10_generate_correct_numbers_format(self):
        self.assertEqual(self.c.process('g9', '0-13-235088'), '2')

    def test_isbn10_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g9', 'ISBN-10: 0-13-235088'), '2')

    def test_isbn10_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g9', '0-13-235080'), '2')

    def test_isbn10_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g9', '0-13-235808'), '2')

    # Validate Checksum tests --------------------------------------------------
    def test_isbn10_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v9', '0-13-235088-2'), True)

    def test_isbn10_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v9', 'ISBN-10: 0-13-235088-2'), True)

    def test_isbn10_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v9', '0-13-235080-2'), True)

    def test_isbn10_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v9', '0-13-235808-2'), True)

    # #### INTERNATIONAL STANDARD BOOK NUMBER 10 (ISBN-10) with X character ####
    # Generate Checksum tests --------------------------------------------------
    def test_isbn10x_generate_correct_numbers_format(self):
        # lower 'x' in the test case because generate() returns a lower 'x'
        self.assertEqual(self.c.process('g9', '1-23-456789'), 'x')

    def test_isbn10x_generate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('g9', 'ISBN-10: 1#23#456789'), 'x')

    def test_isbn10x_generate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('g9', '1-23-456780'), 'x')

    def test_isbn10x_generate_swap_digits_(self):
        self.assertNotEqual(self.c.process('g9', '1-23-456798'), 'x')

    # Validate Checksum tests --------------------------------------------------
    def test_isbn10x_validate_correct_numbers_format(self):
        self.assertEqual(self.c.process('v9', '1-23-456789-X'), True)

    def test_isbn10x_validate_incorrect_numbers_format(self):
        self.assertEqual(self.c.process('v9', 'ISBN-10: 1_23_456789_X'), True)

    def test_isbn10x_validate_one_digit_wrong(self):
        self.assertNotEqual(self.c.process('v9', '1-23-456780-X'), True)

    def test_isbn10x_validate_swap_digits_(self):
        self.assertNotEqual(self.c.process('v9', '1-23-456798-X'), True)


if __name__ == '__main__':
    unittest.main()
    # run in the on linux terminal 'python3 -m unittest -v'
    # or windows command line 'python -m unittest -v'
