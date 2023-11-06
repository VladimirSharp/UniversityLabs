import string

class Article(object):
     def __init__(self, **kwargs):
         self.__dict__.update(kwargs)

def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result