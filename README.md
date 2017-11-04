Ensure allow overrides is on
configure cgimpd.rc

use the webserver covers script (or symlink your music directory INSIDE your webroot, if you like)
https://github.com/uriel1998/yolo-mpd/blob/master/webserver_covers.sh


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
