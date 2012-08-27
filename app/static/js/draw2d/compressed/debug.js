/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

function trace(_6fa){var _6fb=openwindow("about:blank",700,400);_6fb.document.writeln("<pre>"+_6fa+"</pre>");}function openwindow(url,_6fd,_6fe){var left=(screen.width-_6fd)/2;var top=(screen.height-_6fe)/2;property="left="+left+", top="+top+", toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=1,alwaysRaised,width="+_6fd+",height="+_6fe;return window.open(url,"_blank",property);}function dumpObject(obj){trace("----------------------------------------------------------------------------");trace("- Object dump");trace("----------------------------------------------------------------------------");for(var i in obj){try{if(typeof obj[i]!="function"){trace(i+" --&gt; "+obj[i]);}}catch(e){}}for(var i in obj){try{if(typeof obj[i]=="function"){trace(i+" --&gt; "+obj[i]);}}catch(e){}}trace("----------------------------------------------------------------------------");}