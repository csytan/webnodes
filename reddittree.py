from django.utils import simplejson
import urllib

link = "http://www.reddit.com/r/programming/comments/7yruv/so_i_told_my_wife_i_do_have_a_social_life_i_share/.json"
link = "http://www.reddit.com/r/reddit.com/comments/82uj2/for_all_of_reddits_antiestablishment_posturing/.json"
link = 'http://www.reddit.com/r/politics/comments/830hm/everytime_you_ride_on_a_national_highway_remember/.json'
link = 'http://www.reddit.com/r/programming/comments/830u9/wolfram_alpha_is_coming_and_it_could_be_as/.json'
link = 'http://www.reddit.com/r/worldnews/comments/837fl/victim_will_get_to_blind_the_man_who_blinded_her/.json'
#link = 'http://www.reddit.com/r/programming/comments/83i5n/the_rubber_duck_method_of_debugging/.json'
#link = 'http://www.reddit.com/r/programming/comments/83ee0/speaking_as_a_programmer_itunes_is_really/.json'

comments = []
graph = {}

ROOT = ''

def process(node):
    if not node: return
    data = node['data']
    kind = node['kind']
    
    if kind == 't3':
        # root comment
        comments.append({
            'id': data['name'],
            'content': data['title'] + '<a href="'+ data['url'] + '">link</a>',
            'author': data['author']
        })
        global ROOT
        ROOT = data['name']
    elif kind == 't1':
        # normal comment
        comments.append({
            'id': data['name'],
            'content': data['body'],
            'author': data['author']
        })
        p_children = graph.setdefault(data['parent_id'], [])
        p_children.append(data['name'])
        process(data['replies'])
    elif kind == 'Listing':
        for node in data['children']:
            process(node)


response = urllib.urlopen(link).read()
nodes = simplejson.loads(response)

for node in nodes:
    process(node)

graph = simplejson.dumps(graph)





def hot_topics():
    response = urllib.urlopen('http://www.reddit.com/.json').read()
    data = simplejson.loads(response)
    
    topics = []
    for topic in data['data']['children']:
        topics.append({
            'title': data['title']
        })

"""
{
  "data" : {
    "children" : [
      {
        "data" : {
          "author" : "prondose",
          "clicked" : false,
          "created" : 1236690899,
          "domain" : "i399.photobucket.com",
          "downs" : 619,
          "hidden" : false,
          "id" : "83id1",
          "likes" : null,
          "name" : "t3_83id1",
          "num_comments" : 295,
          "saved" : false,
          "score" : 1514,
          "subreddit" : "pics",
          "subreddit_id" : "t5_2qh0u",
          "title" : "Pedobear asks a question on Yahoo! Answers",
          "ups" : 2133,
          "url" : "http://i399.photobucket.com/albums/pp79/dnlslm9/LittleGirl.jpg"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "Siderman1",
          "clicked" : false,
          "created" : 1236718773,
          "domain" : "self.reddit.com",
          "downs" : 402,
          "hidden" : false,
          "id" : "83irg",
          "likes" : null,
          "name" : "t3_83irg",
          "num_comments" : 455,
          "saved" : false,
          "score" : 1101,
          "subreddit" : "reddit.com",
          "subreddit_id" : "t5_6",
          "title" : "My Friend from RE/MAX: \"The new RE/DDIT logo pissed everyone off who was older than 30 at my office. They all think we're being mocked--which we are.\"",
          "ups" : 1503,
          "url" : "http://www.reddit.com/comments/83irg/my_friend_from_remax_the_new_reddit_logo_pissed/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "lamby",
          "clicked" : false,
          "created" : 1236714567,
          "domain" : "lists.ethernal.org",
          "downs" : 191,
          "hidden" : false,
          "id" : "83i5n",
          "likes" : null,
          "name" : "t3_83i5n",
          "num_comments" : 201,
          "saved" : false,
          "score" : 785,
          "subreddit" : "programming",
          "subreddit_id" : "t5_2fwo",
          "title" : "The Rubber Duck method of debugging",
          "ups" : 976,
          "url" : "http://lists.ethernal.org/oldarchives/cantlug-0211/msg00174.html"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "entor",
          "clicked" : false,
          "created" : 1236717959,
          "domain" : "whitehouse.gov",
          "downs" : 207,
          "hidden" : false,
          "id" : "83in6",
          "likes" : null,
          "name" : "t3_83in6",
          "num_comments" : 124,
          "saved" : false,
          "score" : 480,
          "subreddit" : "politics",
          "subreddit_id" : "t5_2cneq",
          "title" : "Obama releases memo restricting use of presidential signing statements, and urging agency reviews of all such Bush actions. Now is the time to shed light on the past abuse of Executive power!",
          "ups" : 687,
          "url" : "http://www.whitehouse.gov/the_press_office/Memorandum-on-Presidential-Signing-Statements/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "rootbeerfloat",
          "clicked" : false,
          "created" : 1236723130,
          "domain" : "theirtoys.com",
          "downs" : 175,
          "hidden" : false,
          "id" : "83jg1",
          "likes" : null,
          "name" : "t3_83jg1",
          "num_comments" : 89,
          "saved" : false,
          "score" : 295,
          "subreddit" : "WTF",
          "subreddit_id" : "t5_2qh61",
          "title" : "The most comprehensive guide to finding adult content, EVER. (Nothing Graphic, Topic is Maybe NSFW)",
          "ups" : 470,
          "url" : "http://theirtoys.com/sexblog/adult-surfers-guide-to-the-internet.html"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "Altras",
          "clicked" : false,
          "created" : 1236712097,
          "domain" : "youtube.com",
          "downs" : 176,
          "hidden" : false,
          "id" : "83huc",
          "likes" : null,
          "name" : "t3_83huc",
          "num_comments" : 182,
          "saved" : false,
          "score" : 509,
          "subreddit" : "science",
          "subreddit_id" : "t5_mouw",
          "title" : "Refreshingly, the new Fox TV show Lie To Me got it right when it comes to lie detectors (Video restored after Fox had it taken down!)",
          "ups" : 685,
          "url" : "http://www.youtube.com/watch?v=oEZTt_Ciiws&amp;feature=channel_page"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "mitchwright",
          "clicked" : false,
          "created" : 1236704433,
          "domain" : "marcofolio.net",
          "downs" : 346,
          "hidden" : false,
          "id" : "83kk6",
          "likes" : null,
          "name" : "t3_83kk6",
          "num_comments" : 173,
          "saved" : false,
          "score" : 151,
          "subreddit" : "funny",
          "subreddit_id" : "t5_2qh33",
          "title" : "Tuck and Roll! [GIF]",
          "ups" : 497,
          "url" : "http://www.marcofolio.net/images/stories/fun/imagedump/imgdmp_0807_2/july_08_2_04.gif"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "p3on",
          "clicked" : false,
          "created" : 1236687370,
          "domain" : "self.worldnews",
          "downs" : 522,
          "hidden" : false,
          "id" : "83fdv",
          "likes" : null,
          "name" : "t3_83fdv",
          "num_comments" : 283,
          "saved" : false,
          "score" : 1228,
          "subreddit" : "worldnews",
          "subreddit_id" : "t5_2qh13",
          "title" : "Reddit: Stop linking to the Daily Mail (dailymail.co.uk), it's a useless tabloid. If something is newsworth you can find it somewhere more credible.",
          "ups" : 1750,
          "url" : "http://www.reddit.com/comments/83fdv/reddit_stop_linking_to_the_daily_mail/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "Facepuncher",
          "clicked" : false,
          "created" : 1236733638,
          "domain" : "blog.bull3t.me.uk",
          "downs" : 133,
          "hidden" : false,
          "id" : "83l99",
          "likes" : null,
          "name" : "t3_83l99",
          "num_comments" : 124,
          "saved" : false,
          "score" : 105,
          "subreddit" : "technology",
          "subreddit_id" : "t5_2qh16",
          "title" : "The Norton Antivirus cover-up: A mysterious program known as pifts.exe associated with the AV program is attempting to contact a server in Africa. Symantec is hush-hush. ",
          "ups" : 238,
          "url" : "http://blog.bull3t.me.uk/archives/internet/the-mysterious-norton-cover-up-and-piftsexe/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "jack4640",
          "clicked" : false,
          "created" : 1236718808,
          "domain" : "self.atheism",
          "downs" : 145,
          "hidden" : false,
          "id" : "83irs",
          "likes" : null,
          "name" : "t3_83irs",
          "num_comments" : 134,
          "saved" : false,
          "score" : 166,
          "subreddit" : "atheism",
          "subreddit_id" : "t5_2qh2p",
          "title" : "Wouldn't it be more productive if pastors preached about fiscal responsibility, credit debt and healthy lifestyle choices rather than THE GAYS ARE COMING TO ABORT YOU?",
          "ups" : 311,
          "url" : "http://www.reddit.com/comments/83irs/wouldnt_it_be_more_productive_if_pastors_preached/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "saurabhdas",
          "clicked" : false,
          "created" : 1236720985,
          "domain" : "ted.com",
          "downs" : 55,
          "hidden" : false,
          "id" : "83j3f",
          "likes" : null,
          "name" : "t3_83j3f",
          "num_comments" : 88,
          "saved" : false,
          "score" : 183,
          "subreddit" : "technology",
          "subreddit_id" : "t5_2qh16",
          "title" : "Awesomeness at TED: The best technology I've seen in quite a while!",
          "ups" : 238,
          "url" : "http://www.ted.com/index.php/talks/pattie_maes_demos_the_sixth_sense.html"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "bearwave",
          "clicked" : false,
          "created" : 1236720825,
          "domain" : "nynerd.com",
          "downs" : 308,
          "hidden" : false,
          "id" : "83j2i",
          "likes" : null,
          "name" : "t3_83j2i",
          "num_comments" : 121,
          "saved" : false,
          "score" : 213,
          "subreddit" : "funny",
          "subreddit_id" : "t5_2qh33",
          "title" : "Change has come to the Whitehouse [Pic]",
          "ups" : 521,
          "url" : "http://nynerd.com/change-has-come-to-the-whitehouse/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "drongo",
          "clicked" : false,
          "created" : 1236692432,
          "domain" : "guardian.co.uk",
          "downs" : 77,
          "hidden" : false,
          "id" : "83ilj",
          "likes" : null,
          "name" : "t3_83ilj",
          "num_comments" : 151,
          "saved" : false,
          "score" : 205,
          "subreddit" : "worldnews",
          "subreddit_id" : "t5_2qh13",
          "title" : "UK police sweeping powers of arrest: \"People can now be (and have been) arrested and detained for not wearing a seatbelt, dropping litter, shouting in the presence of a police officer, climbing a tree, and building a snowman.\"",
          "ups" : 282,
          "url" : "http://www.guardian.co.uk/commentisfree/henryporter/2009/mar/06/civil-liberties-police"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "stilesjp",
          "clicked" : false,
          "created" : 1236727268,
          "domain" : "msnbc.msn.com",
          "downs" : 114,
          "hidden" : false,
          "id" : "83k4y",
          "likes" : null,
          "name" : "t3_83k4y",
          "num_comments" : 300,
          "saved" : false,
          "score" : 167,
          "subreddit" : "WTF",
          "subreddit_id" : "t5_2qh61",
          "title" : "Teenage girl kills herself after 'sexting' images were posted online by her ex-boyfriend.",
          "ups" : 281,
          "url" : "http://www.msnbc.msn.com/id/29546030/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "mrbroom",
          "clicked" : false,
          "created" : 1236718532,
          "domain" : "open.salon.com",
          "downs" : 80,
          "hidden" : false,
          "id" : "83iq9",
          "likes" : null,
          "name" : "t3_83iq9",
          "num_comments" : 67,
          "saved" : false,
          "score" : 133,
          "subreddit" : "funny",
          "subreddit_id" : "t5_2qh33",
          "title" : "Why Is Rush Getting Such Bad Press?",
          "ups" : 213,
          "url" : "http://open.salon.com/blog/mjwycha/2009/03/08/a_defence_of_rush_against_intolorant_liberals"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "blargfrit",
          "clicked" : false,
          "created" : 1236703073,
          "domain" : "milkandcookies.com",
          "downs" : 749,
          "hidden" : false,
          "id" : "83gx3",
          "likes" : null,
          "name" : "t3_83gx3",
          "num_comments" : 346,
          "saved" : false,
          "score" : 244,
          "subreddit" : "funny",
          "subreddit_id" : "t5_2qh33",
          "title" : "RELIGION! (Front page of Digg, then censored by youtube. See the PSA that's got the internet talking)",
          "ups" : 993,
          "url" : "http://www.milkandcookies.com/link/151455/detail/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "billybaldwin",
          "clicked" : false,
          "created" : 1236733755,
          "domain" : "youtube.com",
          "downs" : 32,
          "hidden" : false,
          "id" : "83l9z",
          "likes" : null,
          "name" : "t3_83l9z",
          "num_comments" : 30,
          "saved" : false,
          "score" : 46,
          "subreddit" : "funny",
          "subreddit_id" : "t5_2qh33",
          "title" : "Guido Beach: A short time ago, off a NJ exit ramp far, far away... [VID]",
          "ups" : 78,
          "url" : "http://www.youtube.com/watch?v=kyAzwREVBZs"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "worldnewsnow",
          "clicked" : false,
          "created" : 1236743041,
          "domain" : "inewsit.com",
          "downs" : 31,
          "hidden" : false,
          "id" : "83moq",
          "likes" : null,
          "name" : "t3_83moq",
          "num_comments" : 34,
          "saved" : false,
          "score" : 29,
          "subreddit" : "worldnews",
          "subreddit_id" : "t5_2qh13",
          "title" : "Footage of Witch craft people being burned in Kenya NOT FOR THE FAINT HEARTED",
          "ups" : 60,
          "url" : "http://www.inewsit.com/video/gallery/Five-people-suspected-to-be-witchcrafts-were-bruterly-murded-in-kisii-Nyamataro-Village"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "badiozamzam",
          "clicked" : false,
          "created" : 1236722589,
          "domain" : "youtube.com",
          "downs" : 13,
          "hidden" : false,
          "id" : "83jcn",
          "likes" : null,
          "name" : "t3_83jcn",
          "num_comments" : 20,
          "saved" : false,
          "score" : 49,
          "subreddit" : "atheism",
          "subreddit_id" : "t5_2qh2p",
          "title" : "Critics of Sharia are silenced at the UN - 13 March 2008",
          "ups" : 62,
          "url" : "http://www.youtube.com/watch?v=XrVIv1s5qzo"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "InsomniakPM",
          "clicked" : false,
          "created" : 1236726654,
          "domain" : "chrysler5thavenue.blogspot.com",
          "downs" : 73,
          "hidden" : false,
          "id" : "83k0x",
          "likes" : null,
          "name" : "t3_83k0x",
          "num_comments" : 29,
          "saved" : false,
          "score" : 47,
          "subreddit" : "technology",
          "subreddit_id" : "t5_2qh16",
          "title" : "What is PIFTS and why is Symantec covering it up?",
          "ups" : 120,
          "url" : "http://chrysler5thavenue.blogspot.com/2009/03/piftsexe.html"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "Facepuncher",
          "clicked" : false,
          "created" : 1236733648,
          "domain" : "blog.bull3t.me.uk",
          "downs" : 44,
          "hidden" : false,
          "id" : "83l9b",
          "likes" : null,
          "name" : "t3_83l9b",
          "num_comments" : 12,
          "saved" : false,
          "score" : 35,
          "subreddit" : "worldnews",
          "subreddit_id" : "t5_2qh13",
          "title" : "The Norton Antivirus cover-up: A mysterious program known as pifts.exe associated with the AV program is attempting to contact a server in Africa. Symantec is hush-hush. ",
          "ups" : 79,
          "url" : "http://blog.bull3t.me.uk/archives/internet/the-mysterious-norton-cover-up-and-piftsexe/"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "Mithridates",
          "clicked" : false,
          "created" : 1236727925,
          "domain" : "en.wikipedia.org",
          "downs" : 34,
          "hidden" : false,
          "id" : "83k94",
          "likes" : null,
          "name" : "t3_83k94",
          "num_comments" : 18,
          "saved" : false,
          "score" : 29,
          "subreddit" : "atheism",
          "subreddit_id" : "t5_2qh2p",
          "title" : "What Christianity could have been: Marcionism, a branch of Christianity rivaling even the Church of Rome in the 2nd century that saw the God of the Old Testament as a lesser demiurge and the source of evil.",
          "ups" : 63,
          "url" : "http://en.wikipedia.org/wiki/Marcionism"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "GreekStyle",
          "clicked" : false,
          "created" : 1236722072,
          "domain" : "iht.com",
          "downs" : 62,
          "hidden" : false,
          "id" : "83j9g",
          "likes" : null,
          "name" : "t3_83j9g",
          "num_comments" : 70,
          "saved" : false,
          "score" : 117,
          "subreddit" : "politics",
          "subreddit_id" : "t5_2cneq",
          "title" : "Turkish document showing 972,000 Ottoman Armenians disappeared from official population records from 1915 through 1916 is met with silence.",
          "ups" : 179,
          "url" : "http://www.iht.com/articles/2009/03/09/europe/turkey.php"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "democracy101",
          "clicked" : false,
          "created" : 1236709540,
          "domain" : "populistamerica.com",
          "downs" : 143,
          "hidden" : false,
          "id" : "83hk6",
          "likes" : null,
          "name" : "t3_83hk6",
          "num_comments" : 196,
          "saved" : false,
          "score" : 202,
          "subreddit" : "politics",
          "subreddit_id" : "t5_2cneq",
          "title" : "Peter Schiff: \"By simply clinging to tax cuts as their single economic miracle cure, Republicans risk further marginalization.\"",
          "ups" : 345,
          "url" : "http://www.populistamerica.com/rush_to_judgment"
        },
        "kind" : "t3"
      },
      {
        "data" : {
          "author" : "ChevChelios",
          "clicked" : false,
          "created" : 1236735558,
          "domain" : "quicken.intuit.com",
          "downs" : 26,
          "hidden" : false,
          "id" : "83lku",
          "likes" : null,
          "name" : "t3_83lku",
          "num_comments" : 15,
          "saved" : false,
          "score" : 127,
          "subreddit" : "reddit.com",
          "subreddit_id" : "t5_6",
          "title" : "Hidden millionaires: Lessons from unconventional money management",
          "ups" : 153,
          "url" : "http://quicken.intuit.com/personal-finance-articles/fun-with-finances/Hidden-Millionaires-Lessons-From-Unconventional-Money-Management.html"
        },
        "kind" : "t3"
      }
    ]
  },
  "kind" : "Listing"
}

"""


