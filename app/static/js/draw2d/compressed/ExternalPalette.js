/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

ExternalPalette=function(_c0d,_c0e){this.html=document.getElementById(_c0e);this.workflow=_c0d;this.parts=new ArrayList();};ExternalPalette.prototype.type="ExternalPalette";ExternalPalette.prototype.getHTMLElement=function(){return this.html;};ExternalPalette.prototype.addPalettePart=function(part){if(!(part instanceof AbstractPalettePart)){throw "parameter is not instanceof [AbstractPalettePart]";}this.parts.add(part);this.html.appendChild(part.getHTMLElement());part.setEnviroment(this.workflow,this);};