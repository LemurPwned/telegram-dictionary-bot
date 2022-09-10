
from wiktionaryparser import WiktionaryParser

parser = WiktionaryParser()
parser.set_default_language('french')
def assert_supported_lang_code(lang_code):
    if lang_code not in ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh"]:
        raise ValueError("Language code not supported")



def wikitionary_request(word):
    word = parser.fetch(word, 'french')
    # parser.exclude_part_of_speech('noun')
    # parser.include_relation('alternative forms')
    return word


class WikiRequest:
    def __init__(self, word, lang_code='fr'):
        assert_supported_lang_code(lang_code)
        self.word = word
        self.lang_code = lang_code
        self.wiki_response = wikitionary_request(word)[0]
        print(self.wiki_response)

    def __repr__(self):
        return self.style_response(self.wiki_response)

    def __str__(self):
        return self.style_response(self.wiki_response)


    def style_definition(self, definition):
        """
        Markdown style definition
        """
        part_of_speech = definition['partOfSpeech']
        definition = definition['text']
        styled_definition = f"""
        *{part_of_speech}*
        {definition}
        """
        return styled_definition

    def style_response(self, wiki_response):
        """
        Markdown style response
        """
        etymology = wiki_response['etymology']
        definitions = "\n".join([self.style_definition(definition) for definition in wiki_response['definitions']])
        styled_response = f"""
        *{self.word}*
        {etymology}\n
        {definitions}\n
        """
        return styled_response


if __name__ == "__main__":
    wikitionary_request("bonjour")
