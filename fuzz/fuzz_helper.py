from thefuzz import fuzz

def get_ratio(str1 : str, str2 : str):
    return fuzz.ratio(str1, str2)

def get_partial_ratio(str1 : str, str2 : str):
    return fuzz.partial_ratio(str1, str2)