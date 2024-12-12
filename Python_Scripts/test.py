from collections import namedtuple
import re

test_string = "ivar,lottman,i.lottman@hanze.nl"

def make_ntuple_from_csvtring(string):
    """
    input waarde string (comma separated string)
    value error bij input error 
    named tuple returnd
    person [naam achternaam email rol]
    rol default guest
    regex code https://uibakery.io/regex-library/email-regex-python
    """
    result_tuple = namedtuple("persoon", ["naam", "achternaam", "email", "rol"])
    email_reg = r"^\S+@\S+\.\S+$"

    if type(string) != str:
        raise ValueError
    if type(string) is None:
        raise ValueError
    if "," not in string:
        raise ValueError

    split_string = string.split(",")
    if len(split_string) > 4:
        raise ValueError
    if len(split_string) < 4:
        split_string.append("Guest")
    if split_string[3] not in ["Admin", "Guest", "User"]:
        raise ValueError


    if re.match(email_reg, split_string[2]) == None:
        raise ValueError

    return_tuple = result_tuple(split_string[0], split_string[1], split_string[2], split_string[3])
    print(return_tuple)
    return result_tuple

make_ntuple_from_csvtring(test_string)
