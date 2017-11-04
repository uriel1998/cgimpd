#!/bin/bash

TEMPFILE=$(mktemp)

CMD=`echo "$QUERY_STRING" | sed -n 's/^.*cmd=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

if [ -f ./cgimpd.rc ];then
        readarray -t line < ./cgimpd.rc
        MPD_HOST=${line[0]}
        MPD_PORT=${line[1]}
        MPD_PASS=${line[2]}
        WEBPAGE_REFRESH=${line[3]}
        MPDBASE=${line[4]}
        COVERBASE=${line[5]}
        WWWBASE=${line[6]}
else
        MPD_HOST="SHIT"
fi


echo "Content-type: text/html"
echo ""
echo '<html><head><link href="./images/favicon.ico" rel="SHORTCUT ICON">'
echo '  <meta http-equiv="content-type" content="text/html; charset=utf-8" />'
echo '  <meta name="viewport" content="width=device-width, initial-scale=1">'
echo '  <link rel="stylesheet" href="./css/default.css" type="text/css" />'
echo '  <title>Simple MPD web output</title>'
echo '  <meta http-equiv="refresh" content="'$WEBPAGE_REFRESH'; url='$REFRESHTO'">'
echo '</head>'
echo '<body id="home">'


    # test if any parameters were passed
    if [ $CMD ]
    then
      case "$CMD" in
        OutputOn*)
            outputnumber=$(echo "$CMD" | awk -F 'OutputOn' '{print $2}')
            bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT enable $outputnumber)
        ;;
        OutputOff*)
            outputnumber=$(echo "$CMD" | awk -F 'OutputOff' '{print $2}')
            bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT disable $outputnumber)            
        ;;
        Pause)
#          echo "Output of ifconfig :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT toggle)
 #         echo "</pre>"
          ;;
        Play)
#          echo "Output of ifconfig :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT toggle)
 #         echo "</pre>"
          ;;     
        Next)
#          echo "Output of uname -a :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT next)
#          echo "</pre>"
          ;;
     
        Previous)
#          echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT prev)
#          echo "</pre>"
          ;;
        Previous)
#          echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT prev)
#          echo "</pre>"
          ;;
        Sequential)
 #         echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT random off)
 #         echo "</pre>"
          ;;
        Random)
  #        echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT random on)
 #         echo "</pre>"
          ;;
        Once)
  #        echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT repeat off)
   #       echo "</pre>"
          ;;
        Repeat)
 #         echo "Output of dmesg :<pre>"
          bobnewby=$(mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT repeat on)
 #         echo "</pre>"
          ;;
        esac
    fi



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

if [ -f "$COVERFILE" ];then
    COVERDIR=$(dirname "$SCRATCH")
    COVERFILE="$COVERDIR/cover.jpg"
else
    COVERFILE="$SONGDIR/folder.jpg"
    if [ -f "$COVERFILE" ];then
        scratchdirname=$(dirname"$RELSONGFILE")
        COVERFILE="$COVERBASE/$scratchdirname/folder.jpg"    
    else
        COVERFILE="./images/nocoverart.jpg"
    fi
fi

REPEAT=$(echo "$mpd_state1" | grep -e "repeat" | awk -F " " '{print $4}')
RANDOMPLAY=$(echo "$mpd_state1" | grep -e "random" | awk -F " " '{print $6}')
CONSUME=$(echo "$mpd_state1" | grep -e "random" | awk -F " " '{print $10}')

mpc --host $MPD_PASS@$MPD_HOST --port $MPD_PORT outputs > "$TEMPFILE"
readarray -t output_temp < "$TEMPFILE"
rm "$TEMPFILE"
for i in "${output_temp[@]}";do
    toadd=$(echo "$i" | awk -F '(' '{print $2}' | awk -F ')' '{print $1}') 
    outputname=("${outputname[@]}" "$toadd")
    toadd=$(echo "$i" | awk -F ')' '{print $2}' | awk -F 'is ' '{print $2}') 
    outputstatus=("${outputstatus[@]}" "$toadd")
done


echo '<div id="outer">'
echo '  <div id="primarycontainer">'
echo '      <div id="content">'
echo '          <div class="post">'
printf '<img class=\"avatar\" src="%s" />\n' "$COVERFILE"
echo "<p><h2>$ARTIST</h2></p><p><h2>$TITLE</h2></p><p><h2>$ALBUM</h2></p>"

echo '<form style="width: 60%" method=get>'
echo '<button type="submit" name="cmd" value="Previous" style="border: 0; background: transparent">'
echo '    <img class="button" src="./images/183193_-_backward.png" alt="Prev" />'
echo '</button>'    
case "$PLAYSTATE" in
    playing)
        echo '<button type="submit" name="cmd" value="Pause" style="border: 0; background: transparent">'
        echo '    <img class="button" src="./images/183196_-_pause.png" alt="Pause" />'
        echo '</button>'    
        ;;
    paused)
        echo '<button type="submit" name="cmd" value="Play" style="border: 0; background: transparent">'
        echo '    <img class="button" src="./images/183195_-_play.png" alt="Play" />'
        echo '</button>'    
        ;;
esac

echo '<button type="submit" name="cmd" value="Next" style="border: 0; background: transparent">'
echo '    <img class="button" src="./images/183194_-_forward.png" alt="Next" />'
echo '</button>'    


if [ "$RANDOMPLAY" == "on" ];then
    echo '<button type="submit" name="cmd" value="Sequential" style="border: 0; background: transparent">'
    echo '    <img class="button" src="./images/183219_-_centered.png" alt="Random" />'
    echo '</button>'    
else
    echo '<button type="submit" name="cmd" value="Random" style="border: 0; background: transparent">'
    echo '    <img class="button" src="./images/183221_-_justification.png" alt="submit" />'
    echo '</button>'    
fi

if [ "$REPEAT" == "on" ];then
    echo '<button type="submit" name="cmd" value="Once" style="border: 0; background: transparent">'
    echo '    <img class="button" src="./images/183190_-_sync.png" alt="submit" />'
    echo '</button>'    
else
    echo '<button type="submit" name="cmd" value="Repeat" style="border: 0; background: transparent">'
    echo '    <img class="button" src="./images/183254_-_arrow_forward_right.png" alt="submit" />'
    echo '</button>'    
fi
echo "</form>"
echo '<form style="width: 70%" method=get>'
arraylength=${#outputname[@]}

# use for loop to read all values and indexes
for (( i=1; i<${arraylength}+1; i++ )); do
    echo "<p>${outputname[$i-1]} "
    if [ "${outputstatus[$i-1]}" = "disabled" ];then
        echo '<button type="submit" name="cmd" value="OutputOn'$i'" style="border: 0; background: transparent"><img class="toggle" src="./images/if_on-botton-left-off_2205230.png" alt="off" /></button></p>'    
    else
        echo '<button type="submit" name="cmd" value="OutputOff'$i'" style="border: 0; background: transparent"><img class="toggle" src="./images/if_on-botton-right-off_2205232.png" alt="on" /></button></p>'     
    fi
    echo "<br />"
done
echo "</form>"
echo '              </div>'





echo '      </div> <!-- Primary content area end -->'
echo '  </div> <!-- Primary container end -->'
echo '  <div class="clear"><hr /></div>'
echo '<div id="wrapper">'
echo '</div>'
echo '  <div id="footer">'
now="$(date)"  
printf "Updated at %s  \n" "$now" 
echo '      <p>Code &copy; 2017 Steven Saus under an MIT license. <br />Design modified from <a href="http://www.freecsstemplates.org/preview/zenlike" target="_blank" >Zenlike</A> by <a target="_blank" href="http://www.nodethirtythree.com/">NodeThirtyThree Design</a>.<br />  Images from <a href="https://unsplash.com/photos/MEcxLZ8ENV8" target="_blank">Valentino Funghi</A> and <a target="_blank" href="https://www.iconfinder.com/icons/379343/equalizer_music_icon#size=128">Paul Iconfinder</p>'
echo '  </div>'
echo '</div>'
echo '</body>'
echo '</html>' 


