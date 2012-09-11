/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

LabelConnection=function(){Connection.call(this);var _6e4=new Label("Message");_6e4.setBackgroundColor(new Color(230,230,250));_6e4.setBorder(new LineBorder(1));this.addFigure(_6e4,new ManhattanMidpointLocator(this));};LabelConnection.prototype=new Connection();LabelConnection.prototype.type="LabelConnection";