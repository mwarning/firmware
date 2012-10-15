#!/usr/bin/haserl -n
Content-type: text/html

<html>
<head>
<title>Info</title>
</head>
<body>
<a href="#" id="link">Login</a><br />
<script type="text/javascript">
document.getElementById("link").href="https://"+location.host;
</script>
<br />
<b>Eigene Mesh IP: </b>
<% ifconfig br-mesh | grep "inet addr" | awk 'BEGIN { FS=":" } { print $2 }'| awk '{ print $1 }' %>
<br />
<b>Andere Knoten im Netz: </b>
<% batctl tg | grep '^ \*' | cut -b 33-49 | sort | uniq | wc -l %>
<br />
<b>Anzahl benachbarter Knoten: </b>
<% batctl o | grep '^[[:digit:]|[:lower:]]' | cut -b 37-53 | sort | uniq | wc -l %>
<br /><br />
<b>Liste bekannter Gateways: </b>
<%
gw_macs=`batctl gwl | grep "^=>" | awk '{ print $2 }'`
if [ `batctl gw | grep -c -o -m 1 "^server"` -eq 1 ]; then
  own_ip=`ifconfig br-mesh | grep "inet addr" | awk 'BEGIN { FS=":" } { print $2 }'| awk '{ print $1 }'`
fi

if [ ! -z "$gw_macs" ]; then
  echo "<ul>"
  if [ -n "$own_ip" ]; then
    echo "<li>$own_ip (dieser Knoten)</li>"
  fi
  for mac in "$gw_macs"; do
    [ -n "$mac" ] && echo "<li>" `mac2ip "$mac"` "</li>"
  done
  echo "</ul>"
else
  if [ -n "$own_ip" ]; then
    echo "<ul>"
    echo "<li>$own_ip (dieser Knoten)</li>"
    echo "</ul>"
  else
    echo "Keine"
  fi
fi
%>
</body>
</html>
