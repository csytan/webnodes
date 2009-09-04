# Google imports
from google.appengine.ext import db


LANG_PAIRS = {
    'AFRIKAANS' : 'af',
    'ALBANIAN' : 'sq',
    'AMHARIC' : 'am',
    'ARABIC' : 'ar',
    'ARMENIAN' : 'hy',
    'AZERBAIJANI' : 'az',
    'BASQUE' : 'eu',
    'BELARUSIAN' : 'be',
    'BENGALI' : 'bn',
    'BIHARI' : 'bh',
    'BULGARIAN' : 'bg',
    'BURMESE' : 'my',
    'CATALAN' : 'ca',
    'CHEROKEE' : 'chr',
    'CHINESE' : 'zh',
    'CHINESE_SIMPLIFIED' : 'zh-CN',
    'CHINESE_TRADITIONAL' : 'zh-TW',
    'CROATIAN' : 'hr',
    'CZECH' : 'cs',
    'DANISH' : 'da',
    'DHIVEHI' : 'dv',
    'DUTCH': 'nl',  
    'ENGLISH' : 'en',
    'ESPERANTO' : 'eo',
    'ESTONIAN' : 'et',
    'FILIPINO' : 'tl',
    'FINNISH' : 'fi',
    'FRENCH' : 'fr',
    'GALICIAN' : 'gl',
    'GEORGIAN' : 'ka',
    'GERMAN' : 'de',
    'GREEK' : 'el',
    'GUARANI' : 'gn',
    'GUJARATI' : 'gu',
    'HEBREW' : 'iw',
    'HINDI' : 'hi',
    'HUNGARIAN' : 'hu',
    'ICELANDIC' : 'is',
    'INDONESIAN' : 'id',
    'INUKTITUT' : 'iu',
    'ITALIAN' : 'it',
    'JAPANESE' : 'ja',
    'KANNADA' : 'kn',
    'KAZAKH' : 'kk',
    'KHMER' : 'km',
    'KOREAN' : 'ko',
    'KURDISH': 'ku',
    'KYRGYZ': 'ky',
    'LAOTHIAN': 'lo',
    'LATVIAN' : 'lv',
    'LITHUANIAN' : 'lt',
    'MACEDONIAN' : 'mk',
    'MALAY' : 'ms',
    'MALAYALAM' : 'ml',
    'MALTESE' : 'mt',
    'MARATHI' : 'mr',
    'MONGOLIAN' : 'mn',
    'NEPALI' : 'ne',
    'NORWEGIAN' : 'no',
    'ORIYA' : 'or',
    'PASHTO' : 'ps',
    'PERSIAN' : 'fa',
    'POLISH' : 'pl',
    'PORTUGUESE' : 'pt-PT',
    'PUNJABI' : 'pa',
    'ROMANIAN' : 'ro',
    'RUSSIAN' : 'ru',
    'SANSKRIT' : 'sa',
    'SERBIAN' : 'sr',
    'SINDHI' : 'sd',
    'SINHALESE' : 'si',
    'SLOVAK' : 'sk',
    'SLOVENIAN' : 'sl',
    'SPANISH' : 'es',
    'SWAHILI' : 'sw',
    'SWEDISH' : 'sv',
    'TAJIK' : 'tg',
    'TAMIL' : 'ta',
    'TAGALOG' : 'tl',
    'TELUGU' : 'te',
    'THAI' : 'th',
    'TIBETAN' : 'bo',
    'TURKISH' : 'tr',
    'UKRAINIAN' : 'uk',
    'URDU' : 'ur',
    'UZBEK' : 'uz',
    'UIGHUR' : 'ug',
    'VIETNAMESE' : 'vi'
}

class Translator(db.Model):
    language_pairs = db.StringListProperty()
    rates = db.ListProperty(int)

class LanguagePair(db.Model):
    translator = db.StringProperty()
    from_lang = db.StringProperty()
    to_lang = db.StringProperty()
    rate = db.IntegerProperty()
    specialty = db.StringProperty()

class TranslationJob(db.Model):
    fr_lang = db.StringProperty()
    to_lang = db.StringProperty()
    text = db.TextProperty()
    translated_text = db.TextProperty(default='')
    client = db.StringProperty()
    translator = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    complete = db.BooleanProperty(default=False)
    
    @classmethod
    def translator_jobs(cls, user):
        query = cls.all()
        query.filter('translator =', user.id)
        return query.fetch(100)
        
    @classmethod
    def client_jobs(cls, user):
        query = cls.all()
        query.filter('client =', user.id)
        return query.fetch(100)
        
    def id(self):
        return int(self.key().id())