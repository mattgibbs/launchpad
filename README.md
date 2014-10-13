launchpad
=========

A PyQt-based application launcher.

Launchpad lets you make a list of your frequently used programs (or any shell command, for that matter), then launch items from that list quickly, via an auto-complete text box.  If you have seen something like Quicksilver, you pretty much know what Launchpad is.  It is based on PyQt, and works on OS X and Linux.  Launchpad was written to make it easier to run a two mile long particle accelerator, and it might be able to make whatever you are doing easier too.

Why use Launchpad instead of some other launcher tool?
----------

Launchpad is really bare bones, for better or worse.  It is simple enough that it probably runs well on any unix-based OS that can run Python and Qt (I've tried Linux and OS X).  Unlike Quicksilver, you have full control over what items it might try to launch, but that also means you have to manually enter those items.  To add an item, you specify a name and a shell command to run, and it will add it to a SQLite database.  If this sounds useful, great!  If this doesn't sound fancy enough, or if it sounds complicated, you might want to try something else.
