import urllib

from django.utils import simplejson

SERVICE = 'http://boss.yahooapis.com/ysearch/web/v1/'
APP_ID = 'jok5ElTV34F7l3n2fMji6h97QWxbS_sNyz9g30PqKoC0v.QmOMDNSUlwRXevUnk-'

def search(query, start=0, count=10, site=None):
    url = SERVICE + query
    if site:
        url += '+site:' + site
    url += '?appid=' + APP_ID + '&format=json'
    url += '&count=' + str(count) + '&start=' + str(start)
    
    json = urllib.urlopen(url).read()
    data = simplejson.loads(json)
    return data['ysearchresponse']

"""
{
    "ysearchresponse": {
        "responsecode": "200",
        "nextpage": "\/ysearch\/web\/v1\/foo?format=json&count=10&appid=jok5ElTV34F7l3n2fMji6h97QWxbS_sNyz9g30PqKoC0v.QmOMDNSUlwRXevUnk-&start=10",
        "totalhits": "3518126",
        "deephits": "75800000",
        "count": "10",
        "start": "0",
        "resultset_web": [{
            "abstract": "The terms foobar, <b>foo<\/b>, bar, and baz, are common placeholder names (also referred <b>...<\/b> <b>Foo<\/b> has entered the English language as a neologism and is considered by many to <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=115qs9cce\/**http%3A\/\/en.wikipedia.org\/wiki\/Foo",
            "date": "2009\/06\/09",
            "dispurl": "<b>en.wikipedia.org<\/b>\/wiki\/<b>Foo<\/b>",
            "size": "36712",
            "title": "foobar - Wikipedia, the free encyclopedia",
            "url": "http:\/\/en.wikipedia.org\/wiki\/Foo"
        },
        {
            "abstract": "Official site for the rock band <b>Foo<\/b> Fighters, with news, tour dates, discography, store, community, and more.",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=110rq1p6j\/**http%3A\/\/www.foofighters.com\/",
            "date": "2009\/06\/13",
            "dispurl": "www.<b>foofighters.com<\/b>",
            "size": "7950",
            "title": "<b>Foo<\/b> Fighters",
            "url": "http:\/\/www.foofighters.com\/"
        },
        {
            "abstract": "Definition of <b>foo<\/b> at Dictionary.com with free online dictionary, pronunciation, <b>...<\/b> For, it seems, the word `<b>foo<\/b>' itself had an immediate prewar history in comic <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=11nnm0jlo\/**http%3A\/\/dictionary.reference.com\/browse\/foo%3Fjss=0",
            "date": "2009\/06\/01",
            "dispurl": "<b>dictionary.reference.com<\/b>\/browse\/<wbr><b>foo<\/b>?jss=0",
            "size": "96703",
            "title": "<b>foo<\/b> definition | Dictionary.com",
            "url": "http:\/\/dictionary.reference.com\/browse\/foo?jss=0"
        },
        {
            "abstract": "<b>Foo<\/b> Fighters is an American rock band formed by singer\/guitarist\/drummer Dave <b>...<\/b> Prior to the release of <b>Foo<\/b> Fighters in 1995, Grohl drafted Nate Mendel (bass) <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=11rvgke53\/**http%3A\/\/en.wikipedia.org\/wiki\/index.html%3Fcurid=570280",
            "date": "2009\/05\/24",
            "dispurl": "<b>en.wikipedia.org<\/b>\/wiki\/index.html?<wbr>curid=570280",
            "size": "108739",
            "title": "<b>Foo<\/b> Fighters - Wikipedia, the free encyclopedia",
            "url": "http:\/\/en.wikipedia.org\/wiki\/index.html?curid=570280"
        },
        {
            "abstract": "Just as economists sometimes use the term 'widget' as the ultimate substitute for 'something' that is being measured, programmers tend to use the term '<b>foo<\/b>' <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=12mn91mq6\/**http%3A\/\/searchcio-midmarket.techtarget.com\/sDefinition\/0,,sid183_gci212139,00.html",
            "date": "2009\/06\/07",
            "dispurl": "<b>searchcio-midmarket.techtarget.com<\/b>\/<wbr>sDefinition\/<b>...<\/b>",
            "size": "62269",
            "title": "What is <b>foo<\/b>? - a definition from Whatis.com",
            "url": "http:\/\/searchcio-midmarket.techtarget.com\/sDefinition\/0,,sid183_gci212139,00.html"
        },
        {
            "abstract": "<b>foo<\/b> 1. interj. Term of disgust. 2. [very common] Used very generally as a sample name for absolutely anything, esp <b>...<\/b> When <b>foo<\/b>' is used in connection with bar' <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=1154qlpkp\/**http%3A\/\/www.answers.com\/topic\/foo",
            "date": "2009\/06\/10",
            "dispurl": "www.<b>answers.com<\/b>\/topic\/<b>foo<\/b>",
            "size": "52475",
            "title": "<b>foo<\/b>: Information from Answers.com",
            "url": "http:\/\/www.answers.com\/topic\/foo"
        },
        {
            "abstract": "MySpace Music profile for <b>FOO<\/b>. Download <b>FOO<\/b> 2-step \/ 2-step \/ 2-step music singles, watch music videos, listen to free streaming mp3s, &amp; read <b>FOO's<\/b> blog.",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=12sff5hb8\/**http%3A\/\/profile.myspace.com\/index.cfm%3Ffuseaction=user.viewProfile%26friendID=149304303",
            "date": "2009\/05\/04",
            "dispurl": "<b>profile.myspace.com<\/b>\/index.cfm?<wbr>fuseaction=user.viewProfile&amp;<b>...<\/b>",
            "size": "119056",
            "title": "<b>FOO<\/b> on MySpace Music - Free Streaming MP3s, Pictures &amp; Music Downloads",
            "url": "http:\/\/profile.myspace.com\/index.cfm?fuseaction=user.viewProfile&friendID=149304303"
        },
        {
            "abstract": "<b>foo<\/b>-<b>foo<\/b> fou-fou, fu-fu Caribbean, West African ; small dumplings made by soaking cassava , boiled green plantain , or sometimes yam and allowing it to",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=119csf3ar\/**http%3A\/\/www.answers.com\/topic\/foo-foo",
            "date": "2009\/05\/28",
            "dispurl": "www.<b>answers.com<\/b>\/topic\/<b>foo<\/b>-<b>foo<\/b>",
            "size": "46859",
            "title": "<b>Foo<\/b>-<b>Foo<\/b>: Information from Answers.com",
            "url": "http:\/\/www.answers.com\/topic\/foo-foo"
        },
        {
            "abstract": "Get exclusive content and interact with <b>Foo<\/b> Fighters right from Facebook. <b>...<\/b> <b>Foo<\/b> Fighters Bid on a complete Rock Band Wii system, on which Dave Grohl signed <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=11ifovir7\/**http%3A\/\/www.facebook.com\/foofighters%3Fref=pdb",
            "date": "2009\/06\/08",
            "dispurl": "www.<b>facebook.com<\/b>\/<b>foo<\/b>fighters?<wbr>ref=pdb",
            "size": "208471",
            "title": "<b>Foo<\/b> Fighters | Facebook",
            "url": "http:\/\/www.facebook.com\/foofighters?ref=pdb"
        },
        {
            "abstract": "Bid on a complete Rock Band Wii system, on which Dave Grohl signed the guitar! A wide array of artists also signed, check it out! <b>...<\/b>",
            "clickurl": "http:\/\/lrd.yahooapis.com\/_ylc=X3oDMTU4bTJubWc2BF9TAzIwMjMxNTI3MDIEYXBwaWQDam9rNUVsVFYzNEY3bDNuMmZNamk2aDk3UVd4YlNfc055ejlnMzBQcUtvQzB2LlFtT01ETlNVbHdSWGV2VW5rLQRjbGllbnQDYm9zcwRzZXJ2aWNlA0JPU1MEc2xrA3RpdGxlBHNyY3B2aWQDdDBjd05VZ2VBdTNoQnR6VFp4VTFHWTNKUzUycm9FbzFTRkFBQ1I5Wg--\/SIG=11471skrn\/**http%3A\/\/www.foofighters.com\/news",
            "date": "2009\/06\/09",
            "dispurl": "www.<b>foofighters.com<\/b>\/news",
            "size": "29096",
            "title": "<b>Foo<\/b> Fighters",
            "url": "http:\/\/www.foofighters.com\/news"
        }]
    }
}
"""