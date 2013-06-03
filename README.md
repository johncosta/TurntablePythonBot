TurntablePythonBot
==================

A [Turntable.fm](http://turntable.fm) bot written in Python using [ttapi from
alaingilbert](https://github.com/alaingilbert/Turntable-API)

This project is forked from the code provided by [kgleason]
(https://github.com/kgleason/) and [TurntablePythonBot]
(https://github.com/kgleason/TurntablePythonBot).  It's a refactor and
repackaging of that code.

==========================================
General Commands (Not yet fully supported)
==========================================

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

===========================================
Operator Commands (Not yet fully supported)
===========================================

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

=====================
Provisioning hardware
=====================
https://help.github.com/articles/generating-ssh-keys


===================
Running with Docker
===================
docker run -d johncosta/turntablebot /usr/local/bin/ttpbot <authkey> <userid> <roomid> <ownerid> <path_to_command.yml>

