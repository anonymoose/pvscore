/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

SelectionHighlighter=function(_1251){this.workflow=_1251;this.counter=0;this.black=new Color(0,0,0);this.gray=new Color(200,200,200);};SelectionHighlighter.prototype.type="SelectionHighlighter";SelectionHighlighter.prototype.onSelectionChanged=function(_1252){this.counter++;debugLabel.setText("Count:"+this.counter);var alpha=(_1252===null)?1:0.2;var color=(_1252===null)?this.black:this.gray;var doc=this.workflow.getDocument();var _1256=doc.getFigures();for(var i=0;i<_1256.getSize();i++){_1256.get(i).setAlpha(alpha);}var lines=doc.getLines();for(var i=0;i<lines.getSize();i++){lines.get(i).setColor(color);}if(_1252!==null){_1252.setAlpha(1);if(_1252 instanceof Node){var ports=_1252.getPorts();for(var i=0;i<ports.getSize();i++){var port=ports.get(i);var _125b=port.getConnections();for(var j=0;j<_125b.getSize();j++){_125b.get(j).setColor(this.black);}}}}};