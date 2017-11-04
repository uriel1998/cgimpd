cgimpd
========

A CGI (and BASH) implementation of a web-based remote control for MPD

# Rationale

There's a lot - a *lot* - of different web UIs for MPD. However, they often 
rely on PHP, databases, don't have a feature I need (such as cover art), or 
have features I didn't need (a separate webserver). So I decided to make 
this for a fast, basic, but featureful remote control/status implementation.

This can also be installed on a *remote* webserver.

# Installation

* Ensure AllowOverrides is on for the webserver so that the .htaccess file is acknowledged
* I utilize my [WebServer Covers script](https://github.com/uriel1998/yolo-mpd/blob/master/webserver_covers.sh) so that my whole music collection doesn't have to be inside of webroot. You can, of course, symlink your music collection inside of webroot, but that just makes me uneasy.
* Copy this repository inside your webroot.
* Configure cgimpd.rc
* Configure .htaccess

Format of .rc file

```
hostname.of.mpd
1485
password
5 < - refresh in seconds
/directory/of/music
/directory/for/covers
/www/base/directory
http://url.to/refresh/to/
```

Format of .htaccess

```
#Alternate default index page
DirectoryIndex mpd.cgi

AddHandler cgi-script .cgi
Options +ExecCGI 

<Files "cgimpd.rc">
        Order Deny,Allow
        Deny from all
</Files>

```
