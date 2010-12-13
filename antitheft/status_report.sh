#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/opt/local/bin
export PATH

BOUNDARY="BOUNDARY-$(date|md5)--"

#IPADDR=$(wget -q -O - http://home.sumin.us:8000/geoip/ip.php)
HOSTNAME=$(hostname)
ACTIVE_USER=$(who|grep console|awk '{print $1}')

DATETIME=$(date +%Y%m%d-%H%M%S)
FROM="$(whoami)@${HOSTNAME}"
TO="suminb@gmail.com"
SUBJECT="System Status Report of ${HOSTNAME}"

HR="--------------------------------------------------------------------------------"

#
# Taking a picture through the built-in webcam
#
isightcapture -t jpg /tmp/cam-${DATETIME}.jpg

#
# Screencapture
#
#PID_LOGINWINDOW=$(ps -ef|grep loginwindow|head -n 1|awk '{print $1}')
#sudo launchctl bsexec $PID_LOGINWINDOW screencapture -t png -x /tmp/sc-${DATETIME}.png

#
# Sending an email
#
(
echo "Content-Type: multipart/mixed; boundary=${BOUNDARY}" && \
echo "Mime-Version: 1.0" && \
echo "From: ${FROM}" && \
echo "To: ${TO}" && \
echo "Subject: ${SUBJECT}" && \

echo "--${BOUNDARY}" && \
echo "Content-Type: text/html; charset=\"utf-8\"" && \
echo -e "\n" && \
echo "<html><head><title>${SUBJECT}</title></head><body>" && \
echo "<pre style=\"font-family:monospace;\">" && \

echo -e "$HR\n Uptime & Active Users\n$HR" && \
w && \

#echo -e "\n$HR\n Memory Usage\n$HR" && \
#top -l 1 | head -n 7 && \

#echo -e "\n$HR\n Disk Usage\n$HR" && \
#df -h && \

# Temporarily disabled
#echo -e "\n$HR\n GeoIP\n$HR" && \
#wget -q -O - http://home.sumin.us:8000/geoip/geoip.php && \
#echo -e "<a href=\"http://home.sumin.us:8000/geoip/details.php?ip=${IPADDR}\">View Details</a>\n" && \

echo -e "\n$HR\n Network Interfaces\n$HR" && \
ifconfig -a && \

#echo -e "\n$HR\n Active Sockets\n$HR" && \
#netstat -a | /usr/bin/egrep "(tcp|udp)" && \

echo -e "\n$HR\n Process List\n$HR"  && \
ps aux && \

#echo -e "\n$HR\n chkrootkit\n$HR" && \
#chkrootkit && \

echo "</div></body></html>" && \
echo && \

echo "--${BOUNDARY}" && \
echo "Content-Disposition: attachment; filename=cam-${DATETIME}.jpg" && \
echo "Content-Type: application/zip; x-unix-mode=0644" && \
echo "Content-Transfer-Encoding: base64" && \
echo && \
openssl base64 < /tmp/cam-${DATETIME}.jpg

#echo "--${BOUNDARY}" && \
#echo "Content-Disposition: attachment; filename=sc-${DATETIME}.png" && \
#echo "Content-Type: application/zip; x-unix-mode=0644" && \
#echo "Content-Transfer-Encoding: base64" && \
#echo && \
#openssl base64 < /tmp/sc-${DATETIME}.png

) | sendmail -t -i

exit 0;
