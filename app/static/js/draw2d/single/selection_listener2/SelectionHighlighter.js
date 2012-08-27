SelectionHighlighter=function(_43b1){
this.workflow=_43b1;
this.counter=0;
this.black=new Color(0,0,0);
this.gray=new Color(200,200,200);
};
SelectionHighlighter.prototype.type="SelectionHighlighter";
SelectionHighlighter.prototype.onSelectionChanged=function(_43b2){
this.counter++;
debugLabel.setText("Count:"+this.counter);
var alpha=(_43b2===null)?1:0.2;
var color=(_43b2===null)?this.black:this.gray;
var doc=this.workflow.getDocument();
var _43b6=doc.getFigures();
for(var i=0;i<_43b6.getSize();i++){
_43b6.get(i).setAlpha(alpha);
}
var lines=doc.getLines();
for(var i=0;i<lines.getSize();i++){
lines.get(i).setColor(color);
}
if(_43b2!==null){
_43b2.setAlpha(1);
if(_43b2 instanceof Node){
var ports=_43b2.getPorts();
for(var i=0;i<ports.getSize();i++){
var port=ports.get(i);
var _43bb=port.getConnections();
for(var j=0;j<_43bb.getSize();j++){
_43bb.get(j).setColor(this.black);
}
}
}
}
};
