import logging
import re

from wiktionaryparser import WiktionaryParser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


parser = WiktionaryParser()
parser.set_default_language('french')
def assert_supported_lang_code(lang_code):
    if lang_code not in ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh"]:
        raise ValueError("Language code not supported")

def escape_markdown( text):
    """
    Helper function to escape telegram markup symbols
    """
    text = text.replace('“', '_').replace('”', '_')
    escape_chars = '\[()+-.!~>=|'
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def wikitionary_request(word):
    word = parser.fetch(word, 'french')
    return word


class WikiRequest:
    def __init__(self, word, lang_code='fr'):
        assert_supported_lang_code(lang_code)
        self.word = word
        self.lang_code = lang_code
        try:
            self.wiki_response = wikitionary_request(word)[0]
        except IndexError:
            self.wiki_response = None
            logging.error("No response from Wiktionary")
            raise ValueError("No response from Wiktionary")
        logging.debug(self.wiki_response)

    def __repr__(self):
        return self.style_response(self.wiki_response)

    def __str__(self):
        return self.style_response(self.wiki_response)


    def style_definition(self, def_no, definition):
        """
        Markdown style definition
        """
        part_of_speech = escape_markdown(definition['partOfSpeech'])
        definition = escape_markdown("\n".join(definition['text']))
        styled_definition = f"""
        {def_no}\. `{part_of_speech}`\n{definition}"""
        return styled_definition


    def style_response(self, wiki_response):
        """
        Markdown style response
        """
        etymology = escape_markdown(wiki_response['etymology'])
        definitions = "\n".join([self.style_definition(i+1, definition) for i, definition in enumerate(wiki_response['definitions'])])
        styled_response = f"""
        *`{self.word}`*\n
        __Etymology__\n
        {etymology}
        __Definitions__\n{definitions}
        """
        return styled_response


if __name__ == "__main__":
    wikitionary_request("bonjour")
