#!/usr/bin/env python
# encoding: utf-8
"""
aechat.py

Created by Chris Tan on 2009-04-03.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""


text = """
[7:03pm] Jason_Google: Hi Everyone. Time for another App Engine Chat
Time! I'll be in the channel for the next hour to attempt to answer
questions if anyone has any.
[7:03pm] _thom_: Cool.
[7:07pm] _thom_: Jason, how often do these chats usually take place?
[7:07pm] Jason_Google: We hold these twice a month on the first and
third Wednesdays.
[7:07pm] =95 _thom_ adds to calendar, thanks
[7:08pm] Jason_Google: They're at different times to accommodate
different parts of the world. Here's a link to the schedule:
https://groups.google.com/group/google-appengine/browse_thread/thread/3dce0=
eba81be2626#
[7:08pm] Jason_Google: Anyone have any cool new App Engine apps to
share?
[7:09pm] warreninaustintx: after the 2nd AE language is released, will
there be separate SDKs?
[7:09pm] _thom_: Heh. Does moderator.appspot.com count
[7:09pm] johnleblanc: what can you share with us about this?
http://moderator.appspot.com
[7:09pm] _thom_: jinx
[7:10pm] Jason_Google: warreninaustintx: Yes
[7:11pm] oizo: Hi. My first question (sorry for bad english, i'm from
russia). How do i know size a entity in bigtable for calculate needed
spaces. For example - i have model with one string property, and put
into it 1000 chars. What size will have in bigtable? Tnx
[7:12pm] pranny: hi folks: people from Google: welcome
[7:12pm] Jason_Google: oizo: One second, let me look this up for you.
[7:12pm] Jason_Google: pranny: Hi
[7:13pm] pranny: I am interested in the search API. I came to know
about it yesterday noght only, and today will give it a shot. Can we
expect better searches in coming versions ?
[7:13pm] _mattd: Jason_Google: will scheduled tasks be coming sooner
or later?
[7:14pm] dan_google_: oizo: There's a description of the space usage
for an entity on the Quotas page in the docs: http://code.google.com/appeng=
ine/docs/quotas.html
[7:14pm] dan_google_: Each entity stored in the datastore requires the
the following metadata:
[7:14pm] dan_google_: The entity key, including the kind, the ID or
key name, and the key of the entity's parent entity.
[7:14pm] dan_google_: The name and value of each property. Since the
datastore is schemaless, the name of each property must be stored with
the property value for any given entity.
[7:14pm] dan_google_: Any built-in and custom index rows that refer to
this entity. Each row contains the entity kind, any number of property
values depending on the index definition, and the entity key. See How
Index Building Works for more details.
[7:15pm] dan_google_: _mattd: uh, sooner?
[7:15pm] Jason_Google: oizo: I will have to follow up re: calculating
the storage space for a single entity. In general, you can calculate
how much storage your application is using in the Admin Console, and
the size is obviously proportionate to the number of bytes.
[7:15pm] Jason_Google: Ah, welcome Dan.
[7:15pm] =95 dan_google_ waves to Jason.
[7:15pm] _mattd: dan_google_: cool!
[7:15pm] _mattd: dan_google_: any details on what "background
processing" holds for us?
[7:16pm] dan_google_: _mattd: It holds the ability to do processing in
the background!
[7:16pm] _mattd: ha
[7:16pm] dan_google_: _mattd: Not really.
[7:16pm] _mattd: ok
[7:16pm] dan_google_: _mattd: However, this is a good point to plug
our presentations coming up at Google I/O, including one all about
plans for background processing.
[7:17pm] Jason_Google: You can find a full list of sessions at
http://code.google.com/events/io/sessions.html.
[7:17pm] pranny: hey Googlers: this is not something related to
Appengine, but I was really expecting some false hoax this Apr 1 by
Google. Could not find any. Just one on the Australia site. I loved
Virgle last year
[7:17pm] _mattd: dan_google_: our band's on tour at the time, so i
have to wait until the news and videos come out
[7:17pm] dan_google_: Description of the talk to be presented by Brett
Slatkin: "App Engine was designed to run request-driven web
applications, although this will change in the coming year with the
release of a number of offline computing components. In this session,
we'll explore the task queue/executor model of computation and some of
the more interesting applications."
[7:18pm] _mattd: sounds great
[7:18pm] johnleblanc: Can we expect Django 1.0 support soon?
[7:18pm] dan_google_: pranny:
http://googleappengine.blogspot.com/2009/04/brand-new-language-on-google-ap=
p-engine.html
[7:18pm] _thom_: or 1.1 for that matter
[7:18pm] Jason_Google: pranny: There were quite a few pranks. I
followed them all at
http://www.techcrunch.com/2009/04/01/april-fools-youtube-flails-amazon-clou=
d-computing-in-a-blimp-3d-chrome-browsing-google-master-ai/.
[7:18pm] johnleblanc: good one
[7:19pm] pranny: Jason_Google: oh, I did not read these blogs. They
look great. Fortran 7
[7:19pm] Jason_Google: johnleblanc: There are a series of articles re:
Django at http://code.google.com/appengine/articles/. Or are you
looking for deeper integration?
[7:20pm] johnleblanc: just craving the goodies from 1.0 such as django
admin, formsets, etc
[7:20pm] Jason_Google: I'm actually fairly new to Python, so I haven't
had the opportunity to try it myself.
[7:20pm] _thom_: 0.9.6 !=3D 1.0.2 of Django, feature-wise
[7:20pm] johnleblanc: this has been my savior: http://groups.google.com/gro=
up/app-engine-patch
[7:20pm] johnleblanc: oops, meant http://code.google.com/p/app-engine-patch=
/
[7:21pm] _thom_: ...but that adds a whole lot of complexity when
trying to grok how things work.
[7:22pm] pranny: any update on search module?
[7:22pm] dan_google_: Search past chats for my rantings on how to best
support newer versions of Django.  In short, Django 1.x + zipimport +
either the Helper or app-engine-patch is the recommended way to do it.
[7:22pm] _mattd: any sort of full-text search on the way?
[7:22pm] johnleblanc: indeed, Waldemar has been amazing in the AEP
group
[7:22pm] Jason_Google: pranny: We eventually want to offer support for
full-text search but it's a ways off.
[7:24pm] johnleblanc: dan_google_: past chats archived where?
[7:24pm] Jason_Google: We post transcripts in the Google Group. You
should be able to find them there.
[7:25pm] Jason_Google: https://groups.google.com/group/google-appengine/sea=
rch?group=3Dgoogle-appengine&q=3Dtranscript
[7:25pm] oizo: Second question: When i use simple transaction (for
example only class Balance with ref User) i may make parent key for
Balance objects from this class (Key.from_path('Balance', 'group')) or
create second class Group and use parent key from it (from_path
('Group', 'group')). What better use?
[7:26pm] dan_google_: oizo: It doesn't make much of a difference, as
long as all of the entities you want to modify in a transaction end up
in the same group.
[7:26pm] dan_google_: oizo: It sounds like you can just make the User
entity the parent of the user's Balance entity.
[7:28pm] oizo: Why not fake Balance entity?
[7:29pm] dan_google_: oizo: It doesn't make a different with regards
to the transaction.  You can do whatever is easiest for your app.
[7:30pm] dan_google_: oizo: I forget whether the parent entity has to
exist to create the child with a path.  (I know you can delete the
parent later and continue to refer to the child with a complete path.)
[7:30pm] oizo: ok, thank you very much
[7:31pm] Jason_Google: According to the docs, "You can create an
entity with an ancestor path without first creating the parent
entity."
[7:35pm] oizo: it's really add another pay system for billing (as
poplular russian WebMoney)?
[7:35pm] dan_google_: oizo: Is that a question?
[7:35pm] Jason_Google: Currently, Google Checkout is the only system
that's supported, and there aren't any current plans to add others.
But you can always file a feature request.
[7:36pm] dan_google_: oizo: Note that if you're implementing balance
transfers within the app, you'll need to do something more complicated
than put all user accounts in a single entity group.  Doing so would
drastically slow down your throughput, since only one transaction can
update the group at a time.
[7:38pm] johnleblanc: any examples of GAE + checkout you can point us
to?
[7:39pm] Jason_Google: Oh, I was referring to our billing setup. When
you enable billing for your application, you have to create a
recurring charge authorization with Google Checkout.
[7:40pm] dan_google_: We need a good article on GAE + checkout.  It's
been on my to-do list for a long time.
[7:40pm] johnleblanc: thank you
[7:40pm] warreninaustintx: i don't suppose the billing app is open
source, huh?
[7:41pm] Jason_Google: warreninaustintx: No
[7:41pm] dan_google_: warreninaustintx: Nope, sorry, the admin console
isn't open source.
[7:41pm] dan_google_: warreninaustintx: It uses features not available
to other apps.  Like the ability to create apps.
[7:42pm] johnleblanc: I'd also be curious to see a google calendar +
GAE integration.  Perhaps a booking engine type of thing?
[7:44pm] Jason_Google: We're actually working on an example app with
Calendar. I don't know when it will be finished, but it's pretty far
along. We hope to publish that with an article.
[7:44pm] johnleblanc: nice!
[7:44pm] Jason_Google: There's already an article on using Google Data
services with GAE, but not Calendar-specific.
[7:45pm] pranny: Jason_Google: I was looking over the reviews on
search module, and I found http://zhuocorporation.spaces.live.com/blog/cns!=
D76A58A7350B0D0B!1824.entry
interesting. It shows some 'bugs' in the module.
[7:46pm] oizo: Is any way to get name of all my models and indices in
bigtable (in SDK is datastore_admin.GetSchema() etc), on prod don't
work (exception) but in your admin you such as getting
[7:47pm] Jason_Google: pranny: I agree, it's not terribly robust.
Better support will hopefully be coming, but it's not on the current
roadmap.
[7:48pm] Jason_Google: oizo: Programatically, I'm not sure. The Admin
Console shows the indices and models for your application, though.
[7:51pm] moraes: oizo: try the code you find in
datastore_admin.GetSchema(), rather than trying to import it
[7:56pm] oizo: moraes: exeption was in low-level (in PB as i remember)
[7:56pm] oizo: *exception
[7:58pm] Leemp: oo, is there a google talk going on now? Or did i miss
it
[7:59pm] Leemp: I've been struggling with the sdk trying to solve an
issue haha, i totally forgot about the Q&A
[7:59pm] Leemp: oh n/m, 9-10am pst
[7:59pm] Jason_Google: Hi Leemp. It's just about over. What's your
issue?
[7:59pm] Leemp: Oh awesome, one sec, typing
[8:00pm] Leemp: Jason_Google: Ok, i use WingIDE and would like to have
WingIDE catch any exceptions raised in my app. However, it seems the
SDK has a try-except floating around somewhere that is catching it and
printing it to the client (web browser)
[8:01pm] Leemp: Jason_Google: Wingware (makers of WingIDE) suggest
finding this, and placing a little bit of code in there to raise the
exception again for WingIDEs sake. Any thoughts on where this magic
try-except is, and if that is indeed my best course of action?
[8:02pm] mjwiacek: Leemp, is the exception you see in your browser
purple-ish?
[8:02pm] Leemp: mjwiacek: Plain white, though i would also like to
catch the purple one aswell
[8:02pm] Jason_Google: Ah, I see. I'll have to follow up on this since
I'm not completely sure.
[8:02pm] Leemp: WingIDE has a nice debugger, and my browser _does
not_. I hate having a great debugger, that i can't use. :?
[8:02pm] Leemp: :/*
[8:03pm] moraes: hmm, you use webapp?
[8:03pm] Leemp: moraes: yes, for the handlers
[8:03pm] moraes: i think you should investigate WSGIApplication, and
probably make your own
[8:05pm] dan_google_: I'm out.  Thanks, all!
[8:06pm] oizo: Thanks you too!
[8:06pm] Jason_Google: Good night (or perhaps morning/afternoon) to
everyone. This ends today's Chat Time. The next will be two Wednesdays
from today, April 15, 9-10 a.m. PDT.
"""

import re

re_time = re.compile('^(\[\d.*\])', re.MULTILINE)

split = re.split(re_time, text)
comment_strs = [s for s in split if not s.startswith('[')]

id = 0
comments = []
for s in comment_strs:
    if ':' in s:
        comments.append({
            'id': id,
            'author': s.split(':')[0].lstrip(),
            'body': s.split(':')[1].lstrip(),
            'parent': s.split(':')
        })
        id += 1

print comments
