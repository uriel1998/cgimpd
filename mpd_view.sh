#!/bin/bash

#get installation directory
export SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

CMD=`echo "$QUERY_STRING" | sed -n 's/^.*cmd=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

if [ -f $SCRIPT_DIR/cgimpd.rc ];then
        readarray -t line < ./cgimpd.rc
        MPD_HOST=${line[0]}
        MPD_PORT=${line[1]}
        MPD_PASS=${line[2]}
        WEBPAGE_REFRESH=${line[3]}
        MPDBASE=${line[4]}
        COVERBASE=${line[5]}
        WWWBASE=${line[6]}
        FANARTBASE=${line[7]}
        ARTISTARTBASE=${line[8]}
else
        MPD_HOST="SHIT"
fi


main() {

	FIRST_RUN=true

	while true; do

        cp -f "${SCRIPT_DIR}"/images/favicon.ico "${SCRIPT_DIR}"/out/favicon.ico
        echo '<html><head><link href="favicon.ico" rel="SHORTCUT ICON">' > ${SCRIPT_DIR}/out/index.html
        echo '  <meta http-equiv="content-type" content="text/html; charset=utf-8" />' >> ${SCRIPT_DIR}/out/index.html
        echo '  <meta name="viewport" content="width=device-width, initial-scale=1">' >> ${SCRIPT_DIR}/out/index.html
        cp -f ${SCRIPT_DIR}/css/default.css ${SCRIPT_DIR}/out/default.css
        echo '  <link rel="stylesheet" href="mpdview.css" type="text/css" />' >> ${SCRIPT_DIR}/out/index.html
        echo '  <title>Simple MPD web output</title>' >> ${SCRIPT_DIR}/out/index.html
        echo '  <meta http-equiv="refresh" content="'$WEBPAGE_REFRESH'; url='$WWWBASE'">' >> ${SCRIPT_DIR}/out/index.html
        echo '</head>' >> ${SCRIPT_DIR}/out/index.html
        echo '<body>' >> ${SCRIPT_DIR}/out/index.html

        mpd_state1=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT --format "a@%artist%\nb@%album%\nc@%title%\nd@%file%")
        ARTIST=$(echo "$mpd_state1" | grep "a@" | awk -F "a@" '{print $2}')
        ALBUM=$(echo "$mpd_state1" | grep "b@" | awk -F "b@" '{print $2}')
        TITLE=$(echo "$mpd_state1" | grep "c@" | awk -F "c@" '{print $2}')
        SONGFILE=$(echo "$mpd_state1" | grep "d@" | awk -F "d@" '{print $2}')
        PLAYSTATE=$(echo "$mpd_state1" | grep -e "\[" | awk -F "]" '{print $1}' | cut -c 2- )
        RELSONGFILE=$(echo "$mpd_state1" | grep "d@" | awk -F "d@" '{print $2}')
        SONGFILE="$MPDBASE/$RELSONGFILE"
        SCRATCH="$COVERBASE/$RELSONGFILE"
        SONGDIR=$(dirname "$SONGFILE")
        COVERFILE="$SONGDIR/cover.jpg"


        #WRONG IMAGE FOR WRONG PLACE
        if [ -f "${FANARTBASE}${ARTIST}.jpg" ];then
            FANART="${FANARTBASE}${ARTIST}.jpg"
        else
            FANART="$SCRIPT_DIR/images/nofanart.jpg"
        fi

        echo "${ARTISTARTBASE}${ARTIST}.jpg"

        if [ -f "${ARTISTARTBASE}${ARTIST}.jpg" ];then
            ARTISTART="${ARTISTARTBASE}${ARTIST}.jpg"
        else
            ARTISTART="$SCRIPT_DIR/images/noartist.jpg"
        fi

        if [ -f "$COVERFILE" ];then
            COVERDIR=$(dirname "$SCRATCH")
            COVERFILE="$COVERDIR/cover.jpg"
        else
            COVERFILE="$SONGDIR/folder.jpg"
            if [ -f "$COVERFILE" ];then
                scratchdirname=$(dirname"$RELSONGFILE")
                COVERFILE="$COVERBASE/$scratchdirname/folder.jpg"    
            else
                COVERFILE="$SCRIPT_DIR/images/nocoverart.jpg"
            fi
        fi

        cp -f "${FANART}" ${SCRIPT_DIR}/out/fanart.jpg
        cp -f "${COVERFILE}" ${SCRIPT_DIR}/out/album.jpg
        cp -f "${ARTISTART}" ${SCRIPT_DIR}/out/artist.jpg

        echo '<div class="bg">' >> ${SCRIPT_DIR}/out/index.html
        echo '<div class="container">' >> ${SCRIPT_DIR}/out/index.html
        printf '<img class=\"album\" src="%s" />\n<img class=\"artist\" src="%s" />\n' "album.jpg" "artist.jpg" >> ${SCRIPT_DIR}/out/index.html
        echo "<p><h2 id="outlined_text">$ARTIST</h2></p><p><h2 id="outlined_text">$TITLE</h2></p><p><h2 id="outlined_text">$ALBUM</h2></p>" >> ${SCRIPT_DIR}/out/index.html
        echo '      </div> <!-- Primary content area end -->' >> ${SCRIPT_DIR}/out/index.html
        echo '  </div> <!-- Primary container end -->' >> ${SCRIPT_DIR}/out/index.html
        echo '</body>' >> ${SCRIPT_DIR}/out/index.html
        echo '</html>'  >> ${SCRIPT_DIR}/out/index.html

		mpc --host "$MPD_HOST" idle &> /dev/null
        echo "looping"
   done
}

main


#TODO - lyrics, percent completed meter
