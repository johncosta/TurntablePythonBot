TurntablePythonBot
==================

A [Turntable.fm](http://turntable.fm) bot written in Python using [ttapi from
alaingilbert](https://github.com/alaingilbert/Turntable-API)

I've seen a few different TT bots, and I wanted to take the opportunity to
write my own and use some of what I've been learning as I've been learning
Python.

Feel free to borrow anything that you find helpful, even though I don't think
there is anything too terribly original in here.

Eventually I intended to clean up some of the patterns and make this less
procedural, but that will depend upon my progress with the Python learning. For
now, it seems to be doing what I want it do.

================
General Commands
================

Here is what I can do to help you. In the main room channel, the following
commands are available:

* !hello : Have me say hello to you
* !suck it : See what happens if you offend me
* !user count : Get me to announce how many people are in here
* !help : Presumably you already figured this one out
* !queue list : Show the current DJ queue. Alias: !ql
* !queue add : Get yourself added to the queue. Aliases: !q+ or !add
* !queue remove : Remove yourself from the queue. Aliases: !q- or !remove
* !status : Get your current status.

=================
Operator Commands
=================

Since you appear to be one of my operators, you can also do the following in a
private message with me:

* bop : make me give this song an awesome, regardless of the state of the room.
* snag : I'll add the current song to my playlist
* step up : Make me a DJ
* step down : Get me off the stage
* dq <Position#> : remove the person at <Position#> from the DJ Queue
* pop : remove the person in first place in the DJ Queue. The same as 'dq 1'
* theme = <room theme> : set & announce the theme for the room
* die : cause the python process to exit. Can only be executed by the owner.
