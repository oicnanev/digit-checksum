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

import os
import string
import time
import random


# ############################ CONTROLLER ######################################
class ChecksumController(object):
    """
    Controller Class

    Makes the connection between the View and the Model classes
    """

    # CONSTRUCTOR --------------------------------------------------------------
    def __init__(self):
        """
        Contructor

        Instantiates the view and the model
        """
        self.model = ChecksumModel()
        self.view = ChecksumView(self)

    # PUBLIC METHODS -----------------------------------------------------------
    def main(self):
        """
        None -> None

        Starts the view

        :return: None (void in Java)
        """
        self.view.mainloop()

    def process(self, operation, digits):
        """
        str, str -> str

        Process the user choices made in the view

        :param operation: an alpha-numeric value representing the algorithm to
                          preform
        :param digits: the digits upon preform the algorithm
        :return: processed data to pass to the view
        """
        # remove spaces from non ISBN-13 digits
        if int(operation[1]) < 9:
            digits = ''.join(digits.split())

        try:
            if operation[0] == 'v':  # validation operations
                return self.__validate(digits, operation[1])
            else:  # generation operations
                return self.__generate(digits, operation[1])
        except AssertionError as e:
            return e.__cause__

    @staticmethod
    def validate_user_input(user_input, valid_input_chars, max_num_digits,
                            min_num_digits, max_input_len, min_input_len):
        """
        str, str, int, int, int, int -> bool

        Validates user input

        :param user_input: data input from the user
        :param valid_input_chars: chars permitted in the input from the user
        :param max_num_digits: the maximum length of the numeric digits the user
                               input should have
        :param min_num_digits: the minimum length of the numeric digits the user
                               input should have
        :param max_input_len: the maximum length of the user input
        :param min_input_len: the minimum length of the user input
        :return: True if the user input follows all the rules, False otherwise
        """
        # check for bad characters and count numeric digits in user input
        nums = 0
        for char in user_input:
            if char not in valid_input_chars:
                return False
            if char in string.digits:
                nums += 1

        if 'isbn-10' in user_input.lower() or 'isbn 10' in user_input.lower() \
                or 'isbn-13' in user_input.lower() or \
                'isbn 13' in user_input.lower():
            nums -= 2

        # Assert imputed numeric digits are equal to len_numeric digits
        if not (min_num_digits <= nums <= max_num_digits):
            return False

        # Assert user input length is between the min and max limits
        return min_input_len <= len(user_input) <= max_input_len

    @staticmethod
    def get_digits_attributes(operation):
        """
        str -> str

        Validates user input according to the type of operation, ,i.e. 'g1'
        means generate checksum digit for 'Bilhete de Identidade'

        :param operation: chars 'g' generate or 'v' validate followed by [1-9]
        :return: the user input after perform validation
        """
        # dictionary of key = two char user choice, first 'g' or 'v' for
        # generate or validate; and value, a list with [len numeric digits, max
        # permitted user input length, min permitted user input length]
        lens = {'g1': [8, 8, 8], 'g2': [8, 8, 8], 'g3': [12, 16, 12],
                'g4': [10, 15, 10], 'g5': [15, 18, 15], 'g6': [19, 27, 19],
                'g7': [21, 32, 23], 'g8': [12, 23, 15], 'g9': [9, 23, 9],
                'v1': [9, 10, 9], 'v2': [10, 13, 12], 'v3': [13, 17, 13],
                'v4': [11, 11, 11], 'v5': [16, 19, 16], 'v6': [21, 28, 21],
                'v7': [23, 29, 25], 'v8': [13, 26, 17], 'v9': [10, 24, 10]}

        # inputs permitted for the specific user choice, i.e. 'Bilhete de
        # Identidade' valid inputs are only numbers, 'Cartão de Cidadão', valid
        # inputs are numbers, letters, some punctuation symbols and spaces, etc
        valid_inputs = '1234567890'
        symbols = '.: -_'

        if operation[0] == 'g' and operation[1] in '356' or \
                operation[0] == 'v' and operation[1] in '1356':
            valid_inputs += symbols
        elif operation[0] == 'g' and operation[1] in '789' or \
                operation[0] == 'v' and operation[1] in '2789':
            valid_inputs += symbols + string.ascii_letters

        return valid_inputs, lens[operation][0], lens[operation][1], \
            lens[operation][2]

    # PRIVATE METHODS ----------------------------------------------------------
    def __generate(self, digits, digit_type):
        """
        str, str, str -> str

        Generates the checksum digit for a given set of digits

        :param digits: the digits upon perform the checksum algorithm
        :param digit_type: the card / ISBN type
        :return: checksum digit
        """
        # remove character symbols and spaces from the number
        if digit_type == '8' or digit_type == '9':
            digits = self.__format_number(digits, isbn_type=True)
        else:
            digits = self.__format_number(digits)

        # chose the correspondent algorithm
        if digit_type == '1':
            checksum = self.model.algorithm_pt_identity_card(digits)
        elif digit_type == '2':
            digits = digits.split('€')
            checksum = self.model.algorithm_pt_citizen_card(digits[0],
                                                            digits[1])
        elif digit_type == '3':
            checksum = self.model.algorithm_bar_codes(digits)
        elif digit_type == '4':
            checksum = self.model.algorithm_pt_social_security(digits)
        elif digit_type == '5':
            checksum = self.model.algorithm_bank_card(digits)
        elif digit_type == '6':
            checksum = self.model.algorithm_bank_account(digits)
        elif digit_type == '7':
            assert (digits[:4]) == 'pt50'
            checksum = self.model.algorithm_bank_account(digits[4:])
        elif digit_type == '8':
            checksum = self.model.algorithm_isbn13(digits)
        elif digit_type == '9':
            checksum = self.model.algorithm_isbn10(digits)
        else:
            return ValueError

        return checksum

    def __validate(self, digits, digits_type):
        """
        str -> bool

        Checks the validity of a number according to that number type algorithm

        :param digits  - the digits of the number (sometimes could be characters)
        :param digits_type the type of the number to validate
        :return true if the number is correct, false otherwise
        """
        # remove character symbols and spaces from the number
        if digits_type == '8' or digits_type == '9':
            digits = self.__format_number(digits, isbn_type=True)
        else:
            digits = self.__format_number(digits)

        # separate checksum digit(s) from the rest of digits and check if the
        # given digit(s) equals the computed one(s)
        if digits_type == '2':  # PT citizen card
            # dictionary of key char and value value
            val_char_dict = dict(zip([c for c in string.ascii_uppercase],
                                     [i for i in range(25, -1, -1)]))

            # get the numeric value of the chars
            val_1 = val_char_dict[digits[-3].upper()]
            val_2 = val_char_dict[digits[-2].upper()]

            # a sring containg the character '€' and the number of renews
            issues = '€' + str(val_1 * 26 + val_2)
            return digits[-4:] == self.__generate(digits[:-4] + issues, digits_type)

        elif digits_type == '6' or digits_type == '7':  # NIB and IBAN
            return digits[-2:] == self.__generate(digits[:-2], digits_type)

        else:
            return digits[-1] == self.__generate(digits[:-1], digits_type)

    @staticmethod
    def __format_number(digits, isbn_type=False):
        """
        str -> str

        Removes punctuation character and spaces form the card number

        :param digits: the card digits
        :return: the card digits without character symbols
        """
        symbols = string.punctuation
        digits = digits.lower()

        if isbn_type:
            digits = digits.replace('isbn-13:', '')
            digits = digits.replace('isbn-10:', '')
            digits = digits.replace('isbn:', '')
            digits.strip()  # remove leading and tailing spaces
            for char in digits:
                if char in symbols:
                    digits = digits.replace(char, ' ')
        else:
            for char in digits:
                if char in symbols:
                    digits = digits.replace(char, '')

        return digits


# ################################ VIEW ########################################
class ChecksumView(object):
    """
    View Class

    Command line interface, to grab user inputs and show program outputs
    """

    # CONSTRUCTOR --------------------------------------------------------------
    def __init__(self, controller):
        """
        Constructor

        :param controller: an instance of the Controller class
        """
        self.controller = controller

    # PUBLIC METHOD ------------------------------------------------------------
    def mainloop(self):
        """
        None -> None

        Shows the user the different steps so him can make choices and introduce
        the digits to generate or validate checksum digits

        :return: None (Java void)
        """
        # presents the program banner
        self.__show_banner()

        running = True

        while running:
            # user_choice choice is 'g'(generate) or 'v' (validate)
            user_choice = self.__generate_or_validate()

            # user_choice choice is now 'g' or 'v' followed by a number [1-9]
            user_choice += self.__digit_type(user_choice)

            # imputed digits by the user
            user_digits = self.__digits(user_choice)

            # number of previous renovations (only for citizen card)
            if user_choice == 'g2':
                issues = self.__citizen_card_n_previous_renovations()
                user_digits += '€' + issues

            # show the result returned by the controller
            self.__get_result(user_choice, user_digits)

            # ask user if wants to exit
            running = self.__continue_or_exit()

    # PRIVATE METHODS (called by main) -----------------------------------------
    @staticmethod
    def __show_banner():
        """
        None -> None

        Shows the program banner

        :return: None
        """
        # absolute directory path where this script is executed
        path_dir = os.path.dirname(os.path.abspath(__file__))

        # open and print the file banner.txt (must be in the same directory
        # of this script) use the keyword 'with' so the stream is automatically
        # closed after use
        with open(f'{path_dir}{os.sep}banner.txt', 'r', encoding='utf8') as file:
            line = file.readline()
            while line:
                print(line, end='')
                line = file.readline()

    def __generate_or_validate(self):
        """
        None -> str

        Ask user to choose between generate a checksum digit or validate a
        complete number

        :return: the user input after perform validate
        """
        input_message = ' What kind of operation do you want to perform? ' \
                        'Enter [g] for generate or [v] to validate: '

        return self.__validate_user_input('GgVv', input_message, 0, 0, 1)

    def __digit_type(self, user_choice):
        """
        str -> str

        Shows user the message to input the type of operation he wants to preform

        :param user_choice: char 'g' generate or 'v' validate
        :return: the user input after perform validation
        """
        options = self.__options()  # the different algorithm options

        if user_choice == 'g':
            input_message = f' Generate checksum digit(s) for:\n{options}'
        else:
            input_message = f' Validate :\n{options}'

        return self.__validate_user_input('123456789', input_message, 1, 1, 1)

    def __digits(self, operation_choice):
        """
        str -> str

        Validates user input according to the type of operation, ,i.e. 'g1'
        means generate checksum digit for 'Bilhete de Identidade'

        :param operation_choice: chars 'g' generate or 'v' validate followed by
                                [1-9] witch represents the type of digits
        :return: the user input after perform validation
        """
        # attribs is a list containing [string of valid character inputs,
        # min numeric digits length, max permitted user input length,
        # min permitted user input length]
        attribs = self.controller.get_digits_attributes(operation_choice)

        if operation_choice == 'v9':  # Because of digit X in ISBN-10
            min_num_digits_len = attribs[1] - 1
        else:
            min_num_digits_len = attribs[1]

        return self.__validate_user_input(attribs[0], ' Enter the digits: ',
                                          attribs[1], min_num_digits_len,
                                          attribs[2], attribs[3])

    def __get_result(self, user_choice, user_digits):
        """
        str, str -> None

        Sends the user imputed data to the controller and shows the result

        :param user_choice: 'g' generate or 'v' validate followed by [1-9]
        :param user_digits: user introduced digits
        :return: None
        """
        # Default error message. LOL, trick user to don't see a bug but an
        # implementation
        trial_msg = '\n Operation not available in trial mode. To acquire the ' \
                    'full version please contact us\n'

        # result returned by the controller
        result = self.controller.process(user_choice, user_digits)

        # show a fake progress bar before presenting the result to the user
        self.__progress_bar(' Processing: ', '100% Done!')

        # show result
        if type(result) == str:
            print(f'\n The validation digit is: {result}')
        elif result is True:  # boolean True
            print('\n The number entered is VALID')
        elif not result:
            print('\n The number entered is INVALID.')
        else:  # ERROR !!!!
            print(f'{trial_msg}{result}')

    def __continue_or_exit(self):
        """
        None -> bool

        Sends a bool to mainloop to end or continue the program

        :return: False if the user wants to exit, True otherwise
        """
        input_message = ' Exit? Yes [y] or No [n]: '
        _quit = self.__validate_user_input('YyNn', input_message, 0, 0, 1)

        # To exit, the main loop, return false
        if _quit == 'y':
            self.__progress_bar(' Quiting! ', ' Bye!', delay=.005, steps=77,
                                show_percentage=False)
            print()
            return False
        return True

    # PRIVATE METHODS (called by other private methods) ------------------------
    def __validate_user_input(self, valid_inputs, input_message,
                              max_num_digits_len, min_num_digits_len,
                              max_input_len, min_input_len=1):
        """
        str, str, int, int, int -> str

        In a while loop form grabs user input and only exits that loop after
        the input was validated correct

        :param valid_inputs: chars permitted in the input from the user
        :param input_message:
        :param max_num_digits_len: the maximum length of the numeric digits the
                                   user input should have
        :param min_num_digits_len: the minimum length of the numeric digits the
                                   user input should have
        :param max_input_len: the maximum length of the user input
        :param min_input_len: the minimum length of the user input
        :return: the user input
        """
        user_input = ''
        while not self.controller.validate_user_input(user_input, valid_inputs,
                                                      max_num_digits_len,
                                                      min_num_digits_len,
                                                      max_input_len,
                                                      min_input_len):
            if user_input != '':
                print(' Wrong input!!! ')

            print()
            user_input = input(input_message)

        return user_input.lower()

    @staticmethod
    def __options():
        """
        None -> str

        String containing the different algorithm options

        :return: the different algorithm options
        """
        return '\n' \
               ' * Bilhete de Identidade (NBI) / Contribuinte (NIF) / Lisboa Viva ---- [1]\n' \
               ' * Cartão de Cidadão (NCC) ------------------------------------------- [2]\n' \
               ' * Bar Codes / Generic 13 Digit Cards -------------------------------- [3]\n' \
               ' * Segurança Social (NISS) ------------------------------------------- [4]\n' \
               ' * Cartão de Bancário (CCN / DCN) ------------------------------------ [5]\n' \
               ' * Identificação Bancária (NIB) -------------------------------------- [6]\n' \
               ' * International Banck Acount Number (IBAN) -------------------------- [7]\n' \
               ' * International Standard Book Number (ISBN-13) ---------------------- [8]\n' \
               ' * International Standard Book Number (ISBN-10) ---------------------- [9]\n' \
               ' \n Enter an option: '

    def __citizen_card_n_previous_renovations(self):
        """
        None -> str

        Shows user the message to input how many times renewed the citizen card

        :return: the user input
        """
        input_message = ' How many times did you renew the card?: '
        return self.__validate_user_input('0123456789', input_message, 3, 1, 3)

    @staticmethod
    def __progress_bar(start_message, end_message, delay=.1, steps=10,
                       show_percentage=True):
        """
        str, str, [float], [int], [bool] -> None

        Shows a progress bar

        :param start_message: message to show in the begin of the progress bar
        :param end_message: message to show in the end of the progress bar
        :param delay: velocity by step in milliseconds
        :param steps: number of different steps
        :param show_percentage: boolean to show percentage of progress
        :return: None
        """
        print(start_message, end='', flush=True)
        percentage = 0
        for i in range(steps):
            if show_percentage:
                dot = '.' * random.randint(3, 7)
                print(f'{int(percentage)}%{dot}', end='', flush=True)
            else:
                print('.', end='', flush=True)
            time.sleep(delay)
            percentage += 100 / steps
        print(end_message)


# ############################### MODEL ########################################
class ChecksumModel(object):
    """
    Model class

    Calculates the checksum digit for Portuguese personal identification cards,
    'Cartão de Cidadão' and 'Bilhete de Identidade'; and International Standard
    Book Number (ISBN) in the ISBN-13 format
    Generates the checksum digit for new card, bank account or book numbers or
    validates if a given card, bank account or book numbers are correct
    """

    # CONSTRUCTOR --------------------------------------------------------------
    def __init__(self):
        """Constructor"""

    # PUBLIC METHODS -----------------------------------------------------------
    @staticmethod
    def algorithm_pt_identity_card(digits):
        """
        str -> int

        Calculates the control digit of 'Bilhete de Identidade'

        :param digits: the card number
        :return the checksum digit
        """
        # throw error if card digits length is not 8
        assert len(digits) == 8

        # List of factors to multiply by the card digits.
        # Starts with 9 and decrements the length of card_digits times
        # range(start, [stop], [step])
        factors = [i for i in range(9, 1, -1)]

        # _sum = 9*m7 + 8*m6 + 7*m5 + 6*m4 + 5*m3 + 4*m2 + 3*m1 + 2*m0
        _sum = sum([int(digits[i]) * factors[i] for i in
                    range(len(digits))])

        # remainder of integer division
        rem = _sum % 11

        # because the remainder could be 10 and is only one control digit we
        # return the last index of the string (11 - remainder). If remainder is
        # 10, return 0
        return str(11 - rem)[-1]

    def algorithm_pt_citizen_card(self, digits, n_past_issues):
        """
        str, [str] -> str

        Calculates the checksum digits and the issue chars of 'Cartão de Cidadão'

        :param digits: the card digits
        :param n_past_issues: number of times the card was previously renewed
        :return the last 4 characters of 'Cartão de Cidadão':
                first is the first checksum digit, the same as 'Bilhete de
                Identidade'
                second and third represent the issue number
                fourth is the second checksum digit
        """
        assert len(digits) == 8

        # first control digit
        ctrl_1 = self.algorithm_pt_identity_card(digits)

        # generate issue chars
        issue_chars = self.__generate_citizen_card_issue_chars(n_past_issues)

        # sum calculations to use to generate the second control digit
        _sum = self.__citizen_card_final_sum_algorithm(digits, issue_chars, ctrl_1)

        # second control digit
        ctrl_2 = 10 - (_sum % 10)

        return str(ctrl_1) + issue_chars.lower() + str(ctrl_2)[0]

    @staticmethod
    def algorithm_pt_social_security(digits):
        """
        str -> str

        Calculates the checksum digit for portuguese Social Security card
        :param digits: the card digits
        :return: the checksum digit
        """
        assert len(digits) == 10

        # first 10 prime numbers
        prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        # reverse card digits
        reversed_digits = digits[::-1]

        # 2*m9 + 3*m8 + 5*m7 + 7*m6 + 11*m5 + 13*m4 + 17*m3 + 19*m2 + 23*m1 + 29*m0
        _sum = sum([int(reversed_digits[i]) * prime_nums[i] for i in
                    range(len(reversed_digits))])

        # remainder of integer division
        rem = _sum % 10

        return str(9 - rem)

    @staticmethod
    def algorithm_bank_card(digits):
        """
        str -> str

        Calculates the checksum digit for bank cards (only for card numbers of
        length 16, i.e. VISA, MasterCard, Diners Club)

        :param digits: the card digits
        :return: the checksum digit
        """
        assert len(digits) == 15

        # Put digits in reverse order
        reversed_digits = digits[::-1]

        # Multiply the digits in odd positions (1, 3, 5, etc.) by 2 and
        # subtract 9 to all any result higher than 9
        odd_pos_digits = [int(c) * 2 for c in reversed_digits[::2]]
        even_pos_digits = [int(c) for c in reversed_digits[1::2]]
        odd_pos_digits = [i - 9 if i > 9 else i for i in odd_pos_digits]

        # Add all the numbers together
        _sum = sum(odd_pos_digits) + sum(even_pos_digits)

        # The check digit (the last number of the card) is the amount that you
        # would need to add to get a multiple of 10 (Modulo 10)
        rem = _sum % 10

        # index the string to the first digit to return 0 in case of remainder
        # equals 0 (10 - 0 = 10)
        return str(10 - rem)[0]

    @staticmethod
    def algorithm_bank_account(digits):
        """
        str -> str

        Calculates the checksum digit for bank cards (only for card numbers of
        length 16, i.e. VISA, MasterCard, Diners Club)

        :param digits: the account digits
        :return: the checksum digits (2 digits)
        """
        assert len(digits) == 19

        # list of factors
        factors = [73, 17, 89, 38, 62, 45, 53, 15, 50, 5, 49, 34, 81, 76, 27,
                   90, 9, 30, 3]

        # multiply each digit of the bank account by its corresponding factor
        # sum all digits en the end
        _sum = sum([factors[i] * int(digits[i]) for i in range(len(factors))])

        # remainder of the integer division by 97
        rem = _sum % 97

        return str(98 - rem)

    @staticmethod
    def algorithm_isbn10(digits):
        """
        str -> str

        Calculates the ISNB 10 checksum digit

        :param digits: the ISBN number
        :return: the checksum digit
        """
        # remove spaces
        digits = ''.join(digits.split())

        # check if length is correct
        assert len(digits) == 9

        # list of factors from 10 to 2
        factors = [c for c in range(10, 1, -1)]

        # multiply each digit by the corresponding factor, then sum all
        _sum = sum([int(digits[i]) * factors[i] for i in range(len(digits))])

        # remainder of integer division by 11
        _rem = _sum % 11

        # ini case of 10, return the character 'X'
        if _rem == 1:
            return 'x'
        else:
            return str(11 - _rem)

    @staticmethod
    def algorithm_isbn13(digits):
        """
        str -> str

        Calculates the ISNB 13 checksum digit

        :param digits: the ISBN number
        :return: the checksum digit
        """
        # list formed with ISBN number elements:
        # [prefix, group identifier, publisher identifier, title identifier]
        isbn_list = digits.split()

        # assert length of isbn number are 12
        assert sum([len(i) for i in isbn_list]) == 12

        # assert prefix number is 978 or 979
        assert isbn_list[0] in ['978', '979']

        # assert language group identifier
        assert len(isbn_list[1]) < 6

        # compute the check digit
        isbn_str = ''.join(isbn_list)  # join all digits in a string
        sum_odd_digits = sum([int(isbn_str[c]) for c in range(len(isbn_str))
                              if c % 2 == 0])
        sum_even_digits = sum([int(isbn_str[c]) * 3 for c in
                               range(len(isbn_str)) if c % 2 != 0])
        _sum = sum_odd_digits + sum_even_digits

        # remainder of integer division
        rem = _sum % 10

        return str(10 - rem)[0]

    @staticmethod
    def algorithm_bar_codes(digits):
        """
        str -> str

        Calculates checksum digit for length 13 bar codes

        :param digits: the bar code number
        :return: the checksum digit
        """
        # assert length of isbn number are 12
        assert len(digits) == 12

        # compute the check digit
        sum_odd_digits = sum([int(digits[c]) for c in range(12) if c % 2 == 0])
        sum_even_digits = sum([int(digits[c]) * 3 for c in range(12) if c % 2
                               != 0])
        _sum = sum_odd_digits + sum_even_digits

        # remainder of integer division
        rem = _sum % 10

        return str(10 - rem)[0]

    # PRIVATE METHODS ----------------------------------------------------------
    @staticmethod
    def __generate_citizen_card_issue_chars(n_past_issues):
        """
        int -> str

        Calculates the corresponding issue chars according to the number of
        previous card renews

        :param n_past_issues: the number of previous card renews
        :return: the issue chars, i.e. ZZ, ZY, etc.
        """
        chars = [c for c in string.ascii_uppercase]
        values = [i for i in range(25, -1, -1)]  # list of values from 25 to 0

        # dict is a pair key, value dictionary, a structure similar to java
        # hashmap and / or MATLAB Map
        # zip is an iterator that associates elements of one list with elements
        # of another
        # dict(zip(list_of_keys, list_of_values))
        char_val_dict = dict(zip(values, chars))

        # calculate first char
        # str.join(lst) joins elements from a list in a string
        char1 = ''.join([char_val_dict[int(n_past_issues) // 26]
                         if n_past_issues > '25' else 'Z'])

        # calculate second char
        # dict[key] returns the value associated to that key
        char2 = str(char_val_dict[int(n_past_issues) % 26])

        return char1 + char2

    @staticmethod
    def __citizen_card_final_sum_algorithm(digits, issue_chars,
                                           first_checksum_digit):
        """
        str, str, str -> int

        Sums the 'Cartão de Cidadão' digits in a specific way (algorithm)

        :param digits: the card number without checksum digits and issue characters
        :param issue_chars: the issue characters
        :param first_checksum_digit: the first checksum digit
        :return: the algorithmic sum of the card number
        """
        # list of all uppercase latin alphabet chars
        chars = [c for c in string.ascii_uppercase]

        # list of values from 10 to 35
        values = [i for i in range(10, 36)]

        # dict of pairs key, value -> char : numeric value
        char_val_dict = dict(zip(chars, values))

        # we need to read the card number from right to left, [:] mean indexing
        # from the begin to end with one more :-1 means in reverse order
        reversed_digits = digits[::-1]

        # sum the odd digits and the first issue char
        odd_digits = [int(c) for c in reversed_digits[::2]]
        odd_digits.append(char_val_dict[issue_chars[0].upper()])
        _sum1 = sum(odd_digits)

        # multiply by 2 the even digits and the second issue char, one by one
        even_digits = [int(c) for c in reversed_digits[1::2]]
        even_digits.append(int(first_checksum_digit))
        even_digits.append(char_val_dict[issue_chars[1].upper()])
        double_even_digits = [2 * i for i in even_digits]

        # remove 9 from the numbers with more than one digit
        normalize_even_digits = [i - 9 if i > 9 else i for i in double_even_digits]

        # sum the obtained digits
        _sum2 = sum(normalize_even_digits)

        return _sum1 + _sum2


if __name__ == '__main__':
    """ Program initialization """
    run = ChecksumController()
    run.main()

"""
WEBOGRAPHY
    ASCII ART for banner
    http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
    
    'Bilhete de Identidade', 'Cartão de Cidadão', NIF e NISS
    https://cienciapatodos.webnode.pt/news/a-matematica-do-cart%C3%A3o-de-cidad%C3%A3o-(partes-i-e-ii)/
    https://repositorio.uac.pt/bitstream/10400.3/3359/1/Atl%c3%a2ntico_Expresso_RT7A.pdf
    
    International Standard Book Numbers (ISBN-10 and ISBN-13)
    https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html 
    
    Número do cartão bancário Débito / Crédito
    https://www.freeformatter.com/credit-card-number-generator-validator.html#howToValidate
    
    IBAN NIB
    https://www.bportugal.pt/sites/default/files/anexos/documentos-relacionados/international_bank_account_number_pt.pdf
    
    ISBN 10 and ISBN 13
    https://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13_check_digit_calculation
"""
