XMLSerializer_01=function(){
};
XMLSerializer_01.prototype.type="XMLSerializer_01";
XMLSerializer_01.prototype.toXML=function(_4678){
var xml="<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n";
xml=xml+"<form>\n";
var _467a=_4678.getFigures();
for(var i=0;i<_467a.getSize();i++){
var _467c=_467a.get(i);
xml=xml+"<"+_467c.type+" x=\""+_467c.getX()+"\" y=\""+_467c.getY()+"\" id=\""+_467c.getId()+"\">\n";
xml=xml+this.getPropertyXML(_467c,"   ");
if(_467c instanceof CompartmentFigure){
xml=xml+this.getChildXML(_467c,"   ");
}
xml=xml+"</"+_467c.type+">\n";
}
xml=xml+"</form>\n";
return xml;
};
XMLSerializer_01.prototype.getChildXML=function(_467d,_467e){
var xml="";
var _4680=_467d.getChildren();
for(var i=0;i<_4680.getSize();i++){
var _4682=_4680.get(i);
xml=xml+_467e+"<"+_4682.type+" x=\""+_4682.getX()+"\" y=\""+_4682.getY()+"\" id=\""+_4682.getId()+"\">\n";
xml=xml+this.getPropertyXML(_4682,"   "+_467e);
if(_4682 instanceof CompartmentFigure){
xml=xml+this.getChildXML(_4682,"   "+_467e);
}
xml=xml+_467e+"</"+_4682.type+">\n";
}
return xml;
};
XMLSerializer_01.prototype.getPropertyXML=function(_4683,_4684){
var xml="";
var _4686=_4683.getProperties();
for(key in _4686){
var value=_4686[key];
if(value!==null){
xml=xml+_4684+"<property name=\""+key+"\" value=\""+value+"\">\n";
}
}
return xml;
};
