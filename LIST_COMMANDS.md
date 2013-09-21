
# Default commands
 * Available to anyone
 * **Exclude regexp :** `'(help|test|chans|source)'`
 * **List :**

  + `help [<command>]`

     > Prints general help or help for specific &lt;command&gt;.

  + `test`

     > Simple test to check whether I'm present.

  + `chans`

     > Prints the list of all the channels I'm in.

  + `source`

     > Gives the link to my sourcecode.

# Logs Query commands
 * Available to anyone
 * **Exclude regexp :** `'(last(from|with|seen)?|.*more)'`
 * **List :**

  + `last [<N>] [--from <nick>] [--with <text>] [--chan <chan>] [--skip <nb>] [--filtered|--nofilter]`

     > Prints the last or <N> (max 5) last message(s) from current or main channel if <chan> is not given, optionnally starting back <nb> results earlier and filtered by user <nick> and by &lt;word&gt;. --nofilter includes tweets that were not displayed because of filters, --filtered searches only through these.

  + `lastfrom <nick> [<N>]`

     > Alias for "last --from", prints the last or <N> (max 5) last message(s) from user &lt;nick&gt; (options from "last" except --from can apply).

  + `lastwith <word> [<N>]`

     > Alias for "last --with", prints the last or <N> (max 5) last message(s) matching &lt;word&gt; (options from "last" can apply).

  + `lastmore [<N>]`

     > Prints 1 or &lt;N&gt; more result(s) (max 5) from previous "last" "lastwith" "lastfrom" or "lastcount" command (options from "last" except --skip can apply; --from and --with will reset --skip to 0).

  + `more [<N>]`

     > Alias for "lastmore". Prints 1 or &lt;N&gt; more result(s) (max 5) from previous "last" "lastwith" "lastfrom" or "lastcount" command (options from "last" except --skip can apply; --from and --with will reset --skip to 0).

  + `lastseen <nickname>`

     > Prints the last time &lt;nickname&gt; was seen logging in and out.

# Twitter counting commands
 * Available to anyone
 * **Exclude regexp :** `'.*count'`
 * **List :**

  + `count <text>`

     > Prints the character length of &lt;text&gt; (spaces will be trimmed, urls will be shortened to 20 chars).

  + `lastcount`

     > Prints the latest "count" command and its result (options from "last" except &lt;N&gt; can apply).

# Twitter &amp; Identi.ca sending commands
 * Twitter available when TWITTER's USER, KEY, SECRET, OAUTH_TOKEN and OAUTH_SECRET are provided in gazouilleur/config.py for the chan and FORBID_POST is not given or set to True.
 * Identi.ca available when IDENTICA's USER is provided in gazouilleur/config.py for the chan.
 * available to anyone if TWITTER's ALLOW_ALL is set to True, otherwise only to GLOBAL_USERS and chan's USERS
 * **Exclude regexp :** `'(identica|twitter.*|answer.*|rt|rm.*tweet|dm|stats)'`
 * **List :**

  + `identica <text> [--nolimit]`

     > Posts &lt;text&gt; as a status on Identi.ca (--nolimit overrides the minimum 30 characters rule).
     > > restricted to /IDENTICA

  + `twitteronly <text> [--nolimit] [--force]`

     > Posts &lt;text&gt; as a status on Twitter (--nolimit overrides the minimum 30 characters rule / --force overrides the restriction to mentions users I couldn't find on Twitter).
     > > restricted to /IDENTICA

  + `twitter <text> [--nolimit] [--force]`

     > Posts &lt;text&gt; as a status on Identi.ca and on Twitter (--nolimit overrides the minimum 30 characters rule / --force overrides the restriction to mentions users I couldn't find on Twitter).
     > > restricted to /TWITTER

  + `answer <tweet_id> <@author text> [--nolimit] [--force]`

     > Posts <text> as a status on Identi.ca and as a response to <tweet_id> on Twitter. &lt;text&gt; must include the @author of the tweet answered to except when answering myself. (--nolimit overrides the minimum 30 characters rule / --force overrides the restriction to mentions users I couldn't find on Twitter).
     > > restricted to /TWITTER

  + `answerlast <text> [--nolimit] [--force]`

     > Send &lt;text&gt; as a tweet in answer to the last tweet sent to Twitter from the channel.
     > > restricted to /TWITTER

  + `rt <tweet_id>`

     > Retweets &lt;tweet_id&gt; on Twitter and posts a ♻ status on Identi.ca.
     > > restricted to /TWITTER

  + `rmtweet <tweet_id>`

     > Deletes &lt;tweet_id&gt; from Twitter.
     > > restricted to /TWITTER

  + `rmlasttweet`

     > Deletes last tweet sent to Twitter from the channel.
     > > restricted to /TWITTER

  + `dm <user> <text> [--nolimit]`

     > Posts <text> as a direct message to &lt;user&gt; on Twitter (--nolimit overrides the minimum 30 characters rule).
     > > restricted to /TWITTER

  + `stats`

     > Prints stats on the Twitter account set for the channel.
     > > restricted to /TWITTER

# Twitter &amp; RSS Feeds monitoring commands
 * (Un)Follow and (Un)Filter available only to GLOBAL_USERS and chan's USERS
 * Others available to anyone
 * **Exclude regexp :** `'(u?n?f(ollow|ilter)|list|newsurl|last(tweets|news))'`
 * **List :**

  + `follow <name url|text|@user>`

     > Asks me to follow and display elements from a RSS named <name> at <url>, or tweets matching <text> or from &lt;@user&gt;.
     > > restricted to /AUTH

  + `unfollow <name|text|@user>`

     > Asks me to stop following and displaying elements from a RSS named <name>, or tweets matching <text> or from &lt;@user&gt;.
     > > restricted to /AUTH

  + `filter <word>`

     > Filters the display of tweets or news containing &lt;word&gt;.
     > > restricted to /AUTH

  + `unfilter <word>`

     > Removes a tweets display filter for &lt;word&gt;.
     > > restricted to /AUTH

  + `list [tweets|news|filters]`

     > Displays the list of filters or news or tweets queries followed for current channel.

  + `newsurl <name>`

     > Displays the url of a RSS feed saved as &lt;name&gt; for current channel.

  + `lasttweets <word> [<N>]`

     > Prints the last or <N> last tweets matching &lt;word&gt; (options from "last" can apply).

  + `lastnews <word> [<N>]`

     > Prints the last or <N> last news matching &lt;word&gt; (options from "last" can apply).

# Ping commands
 * Available only to GLOBAL_USERS and chan's USERS except for NoPing to anyone
 * **Exclude regexp :** `'.*ping.*'`
 * **List :**

  + `ping [<text>]`

     > Pings all ops, admins, last 18h speakers and at most 5 more random users on the chan saying &lt;text&gt; except for users set with noping.
     > > restricted to /AUTH

  + `pingall [<text>]`

     > Pings all ops, admins and at most 50 more random users on the chan by saying &lt;text&gt; except for users set with noping.
     > > restricted to /AUTH

  + `pingteam [<text>]`

     > Pings all ops and admins on the chan by saying &lt;text&gt; except for users set with noping.
     > > restricted to /AUTH

  + `noping <user1> [<user2> [<userN>...]] [--stop] [--list]`

     > Deactivates pings from ping command for &lt;users 1 to N> listed. With --stop, reactivates pings for those users. With --list just gives the list of deactivated users.

# Tasks commands
 * RunLater available to anyone
 * Cancel &amp; Tasks available only to GLOBAL_USERS and chan's USERS
 * **Exclude regexp :** `'(runlater|tasks|cancel)'`
 * **List :**

  + `runlater <minutes> [--chan <channel>] <command [arguments]>`

     > Schedules <command> in <minutes> for current channel or optional &lt;channel&gt;.

  + `tasks`

     > Prints the list of coming tasks scheduled.
     > > restricted to /AUTH

  + `cancel <task_id>`

     > Cancels the scheduled task &lt;task_id&gt;.
     > > restricted to /AUTH

# Other commands...
 * Pad &amp; Title available to anyone
 * FuckOff/ComeBack &amp; SetPad available only to GLOBAL_USERS and chan's USERS
 * **Exclude regexp :** `'(fuckoff|comeback|.*pad|title)'`
 * **List :**

  + `fuckoff [<N>]`

     > Tells me to shut up for the next &lt;N&gt; minutes (defaults to 5).
     > > restricted to /AUTH

  + `comeback`

     > Tells me to start talking again after use of "fuckoff".
     > > restricted to /AUTH

  + `setpad <url>`

     > Defines &lt;url&gt; of the current etherpad.
     > > restricted to /AUTH

  + `pad`

     > Prints the url of the current etherpad.

  + `title <url>`

     > Prints the title of the webpage at &lt;url&gt;.