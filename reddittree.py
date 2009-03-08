from django.utils import simplejson
import urllib

link = "http://www.reddit.com/r/programming/comments/7yruv/so_i_told_my_wife_i_do_have_a_social_life_i_share/.json"
link = "http://www.reddit.com/r/reddit.com/comments/82uj2/for_all_of_reddits_antiestablishment_posturing/.json"
link = 'http://www.reddit.com/r/politics/comments/830hm/everytime_you_ride_on_a_national_highway_remember/.json'

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




"""
[
  {
    "data" : {
      "children" : [
        {
          "data" : {
            "author" : "heyt",
            "clicked" : false,
            "created" : 1236491414,
            "domain" : "samoth3.deviantart.com",
            "downs" : 193,
            "hidden" : false,
            "id" : "82ye9",
            "likes" : null,
            "name" : "t3_82ye9",
            "num_comments" : 79,
            "saved" : false,
            "score" : 481,
            "subreddit" : "reddit.com",
            "subreddit_id" : "t5_6",
            "title" : "Hey guys! Show some love and support for my good friend Thomas. Was diagnosed with ALS in 2001 (is totally paralyzed except for his eyes.) Check the art he draws only with his eyes. Funny guy too. Light hearted about his diagnosis.",
            "ups" : 674,
            "url" : "http://samoth3.deviantart.com/"
          },
          "kind" : "t3"
        }
      ]
    },
    "kind" : "Listing"
  },
  {
    "data" : {
      "children" : [
        {
          "data" : {
            "author" : "nmaunder",
            "body" : "\"when I was first diagnosed with ALS the doctor gave me five years to live, but when I told him I couldn't pay the bill he gave me five more. Seems to be working.\"\n\nNice!\n\n\n",
            "created" : 1236542244,
            "downs" : 11,
            "id" : "c083q6g",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083q6g",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "IntolerantFaith",
                      "body" : "I think we should all give this a try.",
                      "created" : 1236554855,
                      "downs" : 0,
                      "id" : "c083sl8",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083sl8",
                      "parent_id" : "t1_c083q6g",
                      "replies" : null,
                      "ups" : 10
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 92
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "JustinTC",
            "body" : "I can't even draw that well with my hands\n",
            "created" : 1236549796,
            "downs" : 4,
            "id" : "c083rgt",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rgt",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "yayweb20",
                      "body" : "Neither can he.",
                      "created" : 1236553469,
                      "downs" : 9,
                      "id" : "c083sa7",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083sa7",
                      "parent_id" : "t1_c083rgt",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "adamrgolf",
                                "body" : ":o",
                                "created" : 1236557047,
                                "downs" : 0,
                                "id" : "c083t5o",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083t5o",
                                "parent_id" : "t1_c083sa7",
                                "replies" : null,
                                "ups" : 9
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 62
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 47
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "seanalltogether",
            "body" : "I'm always amazed when someone can express so much with so few strokes\n\nhttp://fc75.deviantart.com/fs40/f/2009/015/a/6/Alter_Number_1_by_samoth3.jpg",
            "created" : 1236526349,
            "downs" : 10,
            "id" : "c083nwt",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083nwt",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "TyPower",
                      "body" : "I am an artist myself and I find the story inspiring. The next time I 'don't feel like painting' out of difficulty I'll think of Thomas. Sometimes I avoid painting because pulling good work out of myself is often a precarious affair. On the one hand I have the dream result envisioned mentally and on the other I have what I have on the canvas. 1 out of 5 I hit the jackpot and get the rush of success. The other 4 depress me because they \"just fell short of getting there\".\r\n\r\nThomas' story just made me relax.\r\n\r\nGonna undertake a fresh 36\" x 36\" canvas tomorrow with renewed vigour.\r\n\r\nThanks for the inspiration!",
                      "created" : 1236537959,
                      "downs" : 1,
                      "id" : "c083pn9",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083pn9",
                      "parent_id" : "t1_c083nwt",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "HunterTV",
                                "body" : "The thing about art is that you have to play to your own particular strength. If you get bogged down because you can't solo like Jimmy Page or photograph like Ansel Adams you're just missing whatever makes your art yours.\n\nI just started learning freehand drawing with a Wacom I bought, and I have to remind myself of this constantly.",
                                "created" : 1236541812,
                                "downs" : 1,
                                "id" : "c083q4e",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083q4e",
                                "parent_id" : "t1_c083pn9",
                                "replies" : {
                                  "data" : {
                                    "children" : [
                                      {
                                        "data" : {
                                          "author" : "crazedgremlin",
                                          "body" : "I bought a Wacom Graphire tablet a few years ago and I still have a ridiculously hard time drawing with it.  I just expect it to either feel like a paintbrush or a pencil, but it refuses.  ...Maybe if I could get some extra friction between the pen and the plastic...",
                                          "created" : 1236552948,
                                          "downs" : 0,
                                          "id" : "c083s66",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083s66",
                                          "parent_id" : "t1_c083q4e",
                                          "replies" : {
                                            "data" : {
                                              "children" : [
                                                {
                                                  "data" : {
                                                    "author" : "iofthestorm",
                                                    "body" : "There are actually some felt-tip nibs or whatever you call them that you can get for Wacom styluses, I've heard they add some friction. I think they're under $5 so definitely worth checking out if you're using it for art. I have a tablet PC that I use for taking notes and I was going to look into one of those, but never cared enough to actually get one.",
                                                    "created" : 1236566241,
                                                    "downs" : 0,
                                                    "id" : "c083vwx",
                                                    "likes" : null,
                                                    "link_id" : "t3_82ye9",
                                                    "name" : "t1_c083vwx",
                                                    "parent_id" : "t1_c083s66",
                                                    "replies" : null,
                                                    "ups" : 2
                                                  },
                                                  "kind" : "t1"
                                                },
                                                {
                                                  "data" : {
                                                    "author" : "HunterTV",
                                                    "body" : "It takes a lot of practice. For one thing, you're not looking where your pen tip is, you're looking at the screen.\n\nFor another, unless you have a really big ass tablet, the 1:1 relationship between a smaller tablet and a larger screen can be difficult to get used to. Even though  I start seeing the pixels in the strokes, which is a little unusual to get used to in itself, zooming in for precise strokes helps.\n\nI'll have to try the paper trick notouch suggested below though.\n\nTweaking your tablet settings helps too. I must've played with the settings for weeks before I settled on comfortable settings, which I promptly backed up.\n\nIf it's any encouragement, I got the tablet last Christmas, and [this](http://imgur.com/H91L.jpg) was the first proper piece I made after getting used to it, and I did [this one](http://imgur.com/H94D.jpg) two months later.",
                                                    "created" : 1236558175,
                                                    "downs" : 0,
                                                    "id" : "c083th3",
                                                    "likes" : null,
                                                    "link_id" : "t3_82ye9",
                                                    "name" : "t1_c083th3",
                                                    "parent_id" : "t1_c083s66",
                                                    "replies" : null,
                                                    "ups" : 2
                                                  },
                                                  "kind" : "t1"
                                                },
                                                {
                                                  "data" : {
                                                    "author" : "notouch",
                                                    "body" : "Try tape a piece of paper on your wacom. Though I find plastic bag's surface works better (not the grocery plastic bags, the slightly thicker ones from clothes stores).",
                                                    "created" : 1236555898,
                                                    "downs" : 0,
                                                    "id" : "c083suz",
                                                    "likes" : null,
                                                    "link_id" : "t3_82ye9",
                                                    "name" : "t1_c083suz",
                                                    "parent_id" : "t1_c083s66",
                                                    "replies" : null,
                                                    "ups" : 1
                                                  },
                                                  "kind" : "t1"
                                                }
                                              ]
                                            },
                                            "kind" : "Listing"
                                          },
                                          "ups" : 3
                                        },
                                        "kind" : "t1"
                                      }
                                    ]
                                  },
                                  "kind" : "Listing"
                                },
                                "ups" : 16
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 24
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "jerrygofixit",
                      "body" : "You should check out Isketch.net and go to the '5 strokes' room, it's unbelievable.  ",
                      "created" : 1236553479,
                      "downs" : 0,
                      "id" : "c083sa9",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083sa9",
                      "parent_id" : "t1_c083nwt",
                      "replies" : null,
                      "ups" : 2
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "howardhus",
                      "body" : "I am way more impressed by the strengt he has and that he never gave up. This one is my favorite [work of art](http://tinyurl.com/simpleartwork).\n",
                      "created" : 1236533601,
                      "downs" : 48,
                      "id" : "c083p1r",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083p1r",
                      "parent_id" : "t1_c083nwt",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "orbat",
                                "body" : "You do realize Rick rolls were never funny?",
                                "created" : 1236546627,
                                "downs" : 4,
                                "id" : "c083qvu",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083qvu",
                                "parent_id" : "t1_c083p1r",
                                "replies" : {
                                  "data" : {
                                    "children" : [
                                      {
                                        "data" : {
                                          "author" : "Retsoka",
                                          "body" : "yes they were and are",
                                          "created" : 1236551991,
                                          "downs" : 8,
                                          "id" : "c083rya",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083rya",
                                          "parent_id" : "t1_c083qvu",
                                          "replies" : null,
                                          "ups" : 4
                                        },
                                        "kind" : "t1"
                                      }
                                    ]
                                  },
                                  "kind" : "Listing"
                                },
                                "ups" : 7
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 6
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "heffocheffefer",
                      "body" : "How about when it's just [one stroke](http://graphics1.snopes.com/photos/arts/graphics/onestroke.jpg \"[Jesus alert]\").",
                      "created" : 1236530268,
                      "downs" : 29,
                      "id" : "c083oj8",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083oj8",
                      "parent_id" : "t1_c083nwt",
                      "replies" : null,
                      "ups" : 4
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 66
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Anzi",
            "body" : "Great art, and a great friend for posting this.",
            "created" : 1236534001,
            "downs" : 0,
            "id" : "c083p3s",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083p3s",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "heyt",
                      "body" : "Thanks man.  My father and sister visited him today and I felt very bad because I had to work.  I had no clue about his work and seriously, for a person that has lost so much, its amazing that he has so much strength left.  He is really an inspiration.  Thanks reddit for the awesome comments!",
                      "created" : 1236534731,
                      "downs" : 0,
                      "id" : "c083p7x",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083p7x",
                      "parent_id" : "t1_c083p3s",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "unamerican",
                                "body" : "Give him my best, and tell him to keep kickin' ass.  By no means should he let up on the ass kickin' front.  The ass kickin' must continue.\n\nSounds like a great guy with a terrible diagnosis.  I'm glad he has a friend like you.",
                                "created" : 1236543776,
                                "downs" : 0,
                                "id" : "c083qfb",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083qfb",
                                "parent_id" : "t1_c083p7x",
                                "replies" : null,
                                "ups" : 9
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 24
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 21
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "fingertron",
            "body" : "Wow that's amazing! How does he do it?",
            "created" : 1236524275,
            "downs" : 2,
            "id" : "c083nl1",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083nl1",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "heyt",
                      "body" : "He uses an infared computer system made for quads and blinks to set the pencil/pen to draw and then moves his eye to the place he wants to go, then blinks again, to stop movement. After that, it is a vector system and he can adjust size, erase, etc...  pretty neat for a person that can ONLY move his eyes.",
                      "created" : 1236534038,
                      "downs" : 8,
                      "id" : "c083p43",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083p43",
                      "parent_id" : "t1_c083nl1",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "docgravel",
                                "body" : "Can you get some more details for me?  I've worked on an on screen keyboard with english language word prediction and auto completion for people with disabilities.  We partnered with Eyetech DS, which is essentially two IR lights aimed at your eyes with a high quality digital camera in the center that tracks the movement of the shine in your eyes.  It worked pretty well, but there is no way I could have ever used it to create art like this, hence my curiosity.",
                                "created" : 1236548366,
                                "downs" : 0,
                                "id" : "c083r65",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083r65",
                                "parent_id" : "t1_c083p43",
                                "replies" : {
                                  "data" : {
                                    "children" : [
                                      {
                                        "data" : {
                                          "author" : "banjobill",
                                          "body" : "I would be very interested to hear about this too. Currently doing research with eye tracking in VR field.",
                                          "created" : 1236550516,
                                          "downs" : 1,
                                          "id" : "c083rlm",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083rlm",
                                          "parent_id" : "t1_c083r65",
                                          "replies" : null,
                                          "ups" : 9
                                        },
                                        "kind" : "t1"
                                      },
                                      {
                                        "data" : {
                                          "author" : "jerrygofixit",
                                          "body" : "For loss of some better words, that's in-fucking-credible. ",
                                          "created" : 1236553552,
                                          "downs" : 0,
                                          "id" : "c083say",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083say",
                                          "parent_id" : "t1_c083r65",
                                          "replies" : null,
                                          "ups" : 3
                                        },
                                        "kind" : "t1"
                                      },
                                      {
                                        "data" : {
                                          "author" : "diizeh",
                                          "body" : "http://c4q.org/",
                                          "created" : 1236566779,
                                          "downs" : 0,
                                          "id" : "c083w3h",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083w3h",
                                          "parent_id" : "t1_c083r65",
                                          "replies" : null,
                                          "ups" : 1
                                        },
                                        "kind" : "t1"
                                      }
                                    ]
                                  },
                                  "kind" : "Listing"
                                },
                                "ups" : 13
                              },
                              "kind" : "t1"
                            },
                            {
                              "data" : {
                                "author" : "italkshit",
                                "body" : "That and they hooked up a super laser to his penis.  When he goes to reddit's NSFW section, he creates works of art.\n\nSeriously, hell of a job.  To do that with your eyes has to take a lot of focus (no pun intended).",
                                "created" : 1236535507,
                                "downs" : 21,
                                "id" : "c083pbx",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083pbx",
                                "parent_id" : "t1_c083p43",
                                "replies" : null,
                                "ups" : 8
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 65
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "Mr_A",
                      "body" : "Drawing with your eyes is easy. It's learning to hold the pencil that takes practice.",
                      "created" : 1236531728,
                      "downs" : 6,
                      "id" : "c083or9",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083or9",
                      "parent_id" : "t1_c083nl1",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "rossifumi",
                                "body" : "said the guy who never tried it before.  put your money where your mouth is and start drawing and show everyone",
                                "created" : 1236548765,
                                "downs" : 24,
                                "id" : "c083r8p",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083r8p",
                                "parent_id" : "t1_c083or9",
                                "replies" : {
                                  "data" : {
                                    "children" : [
                                      {
                                        "data" : {
                                          "author" : "maxd",
                                          "body" : "You're stupid.",
                                          "created" : 1236551230,
                                          "downs" : 0,
                                          "id" : "c083rqp",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083rqp",
                                          "parent_id" : "t1_c083r8p",
                                          "replies" : null,
                                          "ups" : 11
                                        },
                                        "kind" : "t1"
                                      },
                                      {
                                        "data" : {
                                          "author" : "hett",
                                          "body" : "Wow, you're fucking oblivious.",
                                          "created" : 1236559009,
                                          "downs" : 0,
                                          "id" : "c083tq0",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083tq0",
                                          "parent_id" : "t1_c083r8p",
                                          "replies" : null,
                                          "ups" : 2
                                        },
                                        "kind" : "t1"
                                      }
                                    ]
                                  },
                                  "kind" : "Listing"
                                },
                                "ups" : 2
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 41
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "MarkByers",
                      "body" : "With his eyes.",
                      "created" : 1236549015,
                      "downs" : 1,
                      "id" : "c083rau",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083rau",
                      "parent_id" : "t1_c083nl1",
                      "replies" : null,
                      "ups" : 2
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "redleader",
                      "body" : "I also want to know",
                      "created" : 1236529611,
                      "downs" : 5,
                      "id" : "c083of7",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083of7",
                      "parent_id" : "t1_c083nl1",
                      "replies" : null,
                      "ups" : 3
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 29
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "narwhals",
            "body" : "Great stuff man, very inspiring. Its so easy for us to just keep on retreating into our own shells because of the daily routine which grinds us like a old worn out machine till we really become just that. Then suddenly you come across people like him who defy everything and you feel like a human again.\n\nI used to draw very well in school. Won a few competition and such but then the whole \"life\" got hold of me and now I spent most of the time coding and forgetting about every single resolution I ever made to do something which could have resulted in a bit more fun in life. I think I just found some inspiration to try to break out of this fucked up lifestyle.\n\nThanks and give him my regards.",
            "created" : 1236544702,
            "downs" : 1,
            "id" : "c083qks",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083qks",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "gatsby137",
                      "body" : "Narwhals, you are hereby ordered by Reddit to create some art and post a link to it. You have until 01 May. We're waiting.",
                      "created" : 1236551593,
                      "downs" : 1,
                      "id" : "c083rub",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083rub",
                      "parent_id" : "t1_c083qks",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "m741",
                                "body" : "Listen, now, you're going to die, Raymond K. Hessel, tonight. You might die in one second or in one hour, you decide. So lie to me... Fill in the blank. What does Raymond Hessel want to be when he grows up?\n\nA vet, you said, you want to be a vet, a veterinarian.\n\nThat means school. You have to go to school for that.\n\nIt means too much school, you said.\n\nYou could be in school working your ass off, or you could be dead. You choose...\n\nSo, I said, go back to school. If you wake up tomorrow morning, you find a way to get back to school.\n\nRaymong K. K. Hessel, your dinner is going to taste better than any meal you've eaten, and tomorrow will be the most beautiful day of your entire life.",
                                "created" : 1236559410,
                                "downs" : 0,
                                "id" : "c083tur",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083tur",
                                "parent_id" : "t1_c083rub",
                                "replies" : null,
                                "ups" : 3
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 13
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 11
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Arcesius",
            "body" : "Get him to do more; he's got an audience here.",
            "created" : 1236550151,
            "downs" : 0,
            "id" : "c083rj6",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rj6",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 5
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "mattormeg",
            "body" : "I had a buddy who died from ALS. It's a tough thing to watch, and I imagine even tougher to go through. Your pal Thomas kicks ass. Thanks for cluing me in to this guy.",
            "created" : 1236555973,
            "downs" : 0,
            "id" : "c083svp",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083svp",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 3
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "manthrax",
            "body" : "Fuckin way better artist than me. Grrrr.\n\n",
            "created" : 1236528041,
            "downs" : 0,
            "id" : "c083o6q",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083o6q",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "whiffybatter",
                      "body" : "Seriously -- his \"Desert Pearl\" face is really beautiful.",
                      "created" : 1236536974,
                      "downs" : 1,
                      "id" : "c083pin",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083pin",
                      "parent_id" : "t1_c083o6q",
                      "replies" : null,
                      "ups" : 4
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 13
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Tanuki0",
            "body" : "That's really impressive. It's great that your friend can still express himself through art.",
            "created" : 1236549095,
            "downs" : 0,
            "id" : "c083rbe",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rbe",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 4
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "SceneScenery",
            "body" : "Have you heard of Jason Becker?  He's in a similar situation but instead of drawing, he writes music.  http://www.youtube.com/watch?v=tYIZP1hrfZI  ",
            "created" : 1236569829,
            "downs" : 0,
            "id" : "c083x4t",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083x4t",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "thelilacgirl",
            "body" : "This is awesome!  Thank you so much for sharing.  I would purchase a print if this artist was selling his work.  On a related note, it's good news that the Obama administration has over-turned the prior archaic laws that banned stem cell research, which could show a lot of promise with ALS.  ",
            "created" : 1236553588,
            "downs" : 0,
            "id" : "c083sb8",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083sb8",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 2
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "nixonrichard",
            "body" : "\"Man in hat\" = sued by Nintendo",
            "created" : 1236517868,
            "downs" : 1,
            "id" : "c083maz",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083maz",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "gatsby137",
                      "body" : "It's-a me, Mario's lawyer!",
                      "created" : 1236551754,
                      "downs" : 0,
                      "id" : "c083rvq",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083rvq",
                      "parent_id" : "t1_c083maz",
                      "replies" : null,
                      "ups" : 9
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "AverageCanadian",
                      "body" : "It would be difficult to find a worse PR move than trying to sue somebody with ALS, especially if they are in the late stages of it. ",
                      "created" : 1236554642,
                      "downs" : 0,
                      "id" : "c083sj6",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083sj6",
                      "parent_id" : "t1_c083maz",
                      "replies" : null,
                      "ups" : 3
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 13
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "joharilanng",
            "body" : "Can we get more details on this like how long it takes him, the system he uses etc?\n\nWould like to know more.",
            "created" : 1236538346,
            "downs" : 0,
            "id" : "c083pp0",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083pp0",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 4
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "acangiano",
            "body" : "Inspiring work. Can you please ask Thomas if he can think of any software that would make his life easier when using his computer?",
            "created" : 1236565279,
            "downs" : 0,
            "id" : "c083vkm",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083vkm",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "happyhappy",
            "body" : "Show him some mercy and kill him.",
            "created" : 1236564850,
            "downs" : 0,
            "id" : "c083vgh",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083vgh",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Earthstepper",
            "body" : "Thomas...keep on kicking ass for the working class buddy!",
            "created" : 1236563433,
            "downs" : 0,
            "id" : "c083v1i",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083v1i",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "jgarfink",
            "body" : "ALS is awful. I'm glad he found a way to keep up his spirits.",
            "created" : 1236549706,
            "downs" : 0,
            "id" : "c083rg6",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rg6",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 2
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Matthew1",
            "body" : "Thank you for posting this ~ very uplifting!",
            "created" : 1236549681,
            "downs" : 1,
            "id" : "c083rfz",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rfz",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 3
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "ikovachi",
            "body" : "wow!!!!  this work is awesome",
            "created" : 1236560434,
            "downs" : 0,
            "id" : "c083u68",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083u68",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "kaiise",
            "body" : "\"shopped\"",
            "created" : 1236559561,
            "downs" : 0,
            "id" : "c083twk",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083twk",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Bedrovelsen",
            "body" : "Sweet.\nYou might as well be as happy as possible no matter your situation. It really helps your healing or if not healing then the life you have left. No point in being depressed for the rest of your time.",
            "created" : 1236557989,
            "downs" : 0,
            "id" : "c083tew",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083tew",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Uncial",
            "body" : "To Thomas: there's just no keeping your talent down-- you have drawn wonderful things with your eyes, and I'd love to see more of your work. Three cheers for you!",
            "created" : 1236553375,
            "downs" : 2,
            "id" : "c083s9i",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083s9i",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 2
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "r_schleufer",
            "body" : "I know his drawings are good compared to 90% of all people, but it is really impressive for someone that can draw with only his eyes.\n\nI'm not sure what I'd do if I was paralyzed. I would find some method to continue doing art, but I'm not sure if I'd continue drawing.",
            "created" : 1236531149,
            "downs" : 0,
            "id" : "c083oo9",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083oo9",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 3
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "CuilHandLuke",
            "body" : "Upvoted also for use of Xara Xtreme.  I've been using it for 15+ years for almost all my graphic work.  Easy to use easy to learn and even has a free Linux version.",
            "created" : 1236550191,
            "downs" : 0,
            "id" : "c083rjj",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083rjj",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "infoaddicted",
                      "body" : "So you use the Windows or Linux version?  The Linux version is disappointingly  unstable.",
                      "created" : 1236554784,
                      "downs" : 0,
                      "id" : "c083skd",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083skd",
                      "parent_id" : "t1_c083rjj",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "CuilHandLuke",
                                "body" : "I use the Windows version.  The Linux version won't do animations or multipage PDFs.  Also I haven't use the Linux version enough to push it to its limits.",
                                "created" : 1236560505,
                                "downs" : 0,
                                "id" : "c083u6u",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083u6u",
                                "parent_id" : "t1_c083skd",
                                "replies" : null,
                                "ups" : 1
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 1
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "tehbored",
            "body" : "Does he have one of those things that Stephen Hawking has that lets him speak? Does it sound the same as Hawking's?",
            "created" : 1236527649,
            "downs" : 1,
            "id" : "c083o4s",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083o4s",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "heyt",
                      "body" : "yeah, and he has 12 voices to choose from.  Used to be a psych teacher.  Very cool dude.  ",
                      "created" : 1236534142,
                      "downs" : 0,
                      "id" : "c083p4m",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083p4m",
                      "parent_id" : "t1_c083o4s",
                      "replies" : null,
                      "ups" : 15
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 4
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "howardhus",
            "body" : "he also can move the cheek.",
            "created" : 1236533409,
            "downs" : 2,
            "id" : "c083p0h",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083p0h",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 3
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "chickinkickir",
            "body" : "Love..no doubt..",
            "created" : 1236518879,
            "downs" : 1,
            "id" : "c083mib",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083mib",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 5
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "sardak",
            "body" : "Nicely done, fluid lines and, yes, he's funny.",
            "created" : 1236537196,
            "downs" : 0,
            "id" : "c083pjq",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083pjq",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Devaney1984",
            "body" : "That's very cool, and how the hell do 110 people down vote this story? ",
            "created" : 1236552960,
            "downs" : 1,
            "id" : "c083s6d",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083s6d",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "Stick",
                      "body" : "With the limbs they have that still work.",
                      "created" : 1236553147,
                      "downs" : 2,
                      "id" : "c083s7u",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083s7u",
                      "parent_id" : "t1_c083s6d",
                      "replies" : {
                        "data" : {
                          "children" : [
                            {
                              "data" : {
                                "author" : "infoaddicted",
                                "body" : "Knee-jerk reaction by reddit cynics, of which there are plenty.",
                                "created" : 1236554695,
                                "downs" : 3,
                                "id" : "c083sjl",
                                "likes" : null,
                                "link_id" : "t3_82ye9",
                                "name" : "t1_c083sjl",
                                "parent_id" : "t1_c083s7u",
                                "replies" : {
                                  "data" : {
                                    "children" : [
                                      {
                                        "data" : {
                                          "author" : "mercurialohearn",
                                          "body" : "doesn't \"reddit\" mean \"cynic\" in klingon?",
                                          "created" : 1236567139,
                                          "downs" : 0,
                                          "id" : "c083w7w",
                                          "likes" : null,
                                          "link_id" : "t3_82ye9",
                                          "name" : "t1_c083w7w",
                                          "parent_id" : "t1_c083sjl",
                                          "replies" : null,
                                          "ups" : 1
                                        },
                                        "kind" : "t1"
                                      }
                                    ]
                                  },
                                  "kind" : "Listing"
                                },
                                "ups" : 2
                              },
                              "kind" : "t1"
                            }
                          ]
                        },
                        "kind" : "Listing"
                      },
                      "ups" : 10
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 1
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "Thangalin",
            "body" : "Line art = png; photographs = jpg.",
            "created" : 1236528434,
            "downs" : 20,
            "id" : "c083o8v",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083o8v",
            "parent_id" : "t3_82ye9",
            "replies" : {
              "data" : {
                "children" : [
                  {
                    "data" : {
                      "author" : "RECURSIVE_META_JOKE",
                      "body" : "*Right clicks image, selects properties and checks file extension*\n\nTHIS IS AN OUTRAGE.  I DON'T CARE IF YOU'RE A PARALYZED ALS PATIENT WITH NO MOTOR FUNCTION WHATSOEVER, YOU SHOULD SAVE YOUR PRODIGIOUS AND INSPIRING ARTWORK IN A LOSSLESS FORMAT.",
                      "created" : 1236534806,
                      "downs" : 3,
                      "id" : "c083p8e",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083p8e",
                      "parent_id" : "t1_c083o8v",
                      "replies" : null,
                      "ups" : 28
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "dickbutt",
                      "body" : "SVG might be better.",
                      "created" : 1236537126,
                      "downs" : 0,
                      "id" : "c083pjd",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083pjd",
                      "parent_id" : "t1_c083o8v",
                      "replies" : null,
                      "ups" : 5
                    },
                    "kind" : "t1"
                  },
                  {
                    "data" : {
                      "author" : "rsda",
                      "body" : "Fail at life.",
                      "created" : 1236540821,
                      "downs" : 1,
                      "id" : "c083q00",
                      "likes" : null,
                      "link_id" : "t3_82ye9",
                      "name" : "t1_c083q00",
                      "parent_id" : "t1_c083o8v",
                      "replies" : null,
                      "ups" : 5
                    },
                    "kind" : "t1"
                  }
                ]
              },
              "kind" : "Listing"
            },
            "ups" : 9
          },
          "kind" : "t1"
        },
        {
          "data" : {
            "author" : "sysstemlord",
            "body" : "!(your personal army)",
            "created" : 1236552855,
            "downs" : 6,
            "id" : "c083s58",
            "likes" : null,
            "link_id" : "t3_82ye9",
            "name" : "t1_c083s58",
            "parent_id" : "t3_82ye9",
            "replies" : null,
            "ups" : 2
          },
          "kind" : "t1"
        }
      ]
    },
    "kind" : "Listing"
  }
]

"""
