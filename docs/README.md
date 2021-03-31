# web-based mpd utilities
### (officially *cgimpd* )

Using BASH to create a quick web based lyrics/art view of a playing MPD 
instance, and using BASH and CGI to implement a web-based remote control for 
MPD.

![cgimpd logo](https://github.com/uriel1998/cgimpd/raw/master/cgimpd-open-graph.png "logo")  

## Contents
 1. [About](#1-about)
 2. [License](#2-license)
 3. [Prerequisites](#3-prerequisites)
 4. [Installation](#4-installation)
 5. [Attribution](#5-attribution)
 
***

## 1. About

Originally, this repository just had the CGI implementation (`cgimpd`) of a 
remote control. Currently, it holds both that and a small script (`mpdview.sh`) 
that creates a lightweight web page that has information about what's playing.

### CGI-MPD

There's a lot - a *lot* - of different web UIs for MPD. However, they often 
rely on PHP, databases, don't have a feature I need (such as cover art), or 
have features I didn't need (a separate webserver). So I decided to make 
this for a fast, basic, but featureful remote control/status implementation.

`cgimpd` can be installed on a *remote* webserver from the MPD instance.


![screenshot](https://raw.githubusercontent.com/uriel1998/cgimpd/master/cgi-mpd-screenshot.jpg)

### MPDVIEW

While I love [ompd](https://ompd.pl/) and [rompr](https://fatg3erman.github.io/RompR/), 
I wanted something I could easily pull up and show folks when they asked 
what song was playing - or even leave up in the background without worrying 
that someone would accidentally click a button or press a key. `mpdview` 
 does *not* require cgi; it runs separately on the server machine.

`mpdview` can also be installed on a *remote* webserver from the MPD instance.

![screenshot](https://raw.githubusercontent.com/uriel1998/cgimpd/master/screenshot.png)

## 2. License

This project is licensed under the MIT License. For the full license, see `LICENSE`.

## 3. Prerequisites

* Working webserver

## 4. Installation

1. Download or clone the repository, and put the uncompressed files in a location 
of your choice. Change into that directory.

2. Configure cgimpd.rc 

```
hostname.of.mpd
1485 < - mpd port
password
5 < - refresh in seconds
/directory/of/music
/directory/for/covers
/www/base/directory
http://url.to/refresh/to/
/directory/for/fanart
/directory/for/artistart
```

3. I utilize my [WebServer Covers script](https://github.com/uriel1998/yolo-mpd/blob/master/webserver_covers.sh) so that my whole music collection doesn't have to be inside of webroot. You can, of course, symlink your music collection inside of webroot, but that just makes me uneasy.


4. `mpdview` only:
- create the directory `out` below the script directory
- symlink the files in `out` to somewhere in your webroot
- launch `mpdview.sh &`
- optionally run as a systemd unit
- defaults already exist in `images` if fanart, artist art, or album art is 
not found
- Lyrics are fetched from the music directory as `[song filename].txt`.
- Fanart is simply `Band Name.jpg`.  


4. `cgimpd` only: 

- Ensure AllowOverrides is on for the webserver so that the .htaccess file is acknowledged
- Configure .htaccess

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

## 5. Attribution

* Webpage template based off of [zenlike](http://www.freecsstemplates.org/preview/zenlike) by [NodeThirtyThree Design](http://www.nodethirtythree.com/)
* No cover image by [Valentino Funghi](https://unsplash.com/photos/MEcxLZ8ENV8)
* Icons from [Iconfinder](https://www.iconfinder.com/iconsets/freecns-cumulus)
