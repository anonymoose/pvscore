/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

XMLSerializer_01=function(){};XMLSerializer_01.prototype.type="XMLSerializer_01";XMLSerializer_01.prototype.toXML=function(_1518){var xml="<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n";xml=xml+"<form>\n";var _151a=_1518.getFigures();for(var i=0;i<_151a.getSize();i++){var _151c=_151a.get(i);xml=xml+"<"+_151c.type+" x=\""+_151c.getX()+"\" y=\""+_151c.getY()+"\" id=\""+_151c.getId()+"\">\n";xml=xml+this.getPropertyXML(_151c,"   ");if(_151c instanceof CompartmentFigure){xml=xml+this.getChildXML(_151c,"   ");}xml=xml+"</"+_151c.type+">\n";}xml=xml+"</form>\n";return xml;};XMLSerializer_01.prototype.getChildXML=function(_151d,_151e){var xml="";var _1520=_151d.getChildren();for(var i=0;i<_1520.getSize();i++){var _1522=_1520.get(i);xml=xml+_151e+"<"+_1522.type+" x=\""+_1522.getX()+"\" y=\""+_1522.getY()+"\" id=\""+_1522.getId()+"\">\n";xml=xml+this.getPropertyXML(_1522,"   "+_151e);if(_1522 instanceof CompartmentFigure){xml=xml+this.getChildXML(_1522,"   "+_151e);}xml=xml+_151e+"</"+_1522.type+">\n";}return xml;};XMLSerializer_01.prototype.getPropertyXML=function(_1523,_1524){var xml="";var _1526=_1523.getProperties();for(key in _1526){var value=_1526[key];if(value!==null){xml=xml+_1524+"<property name=\""+key+"\" value=\""+value+"\">\n";}}return xml;};