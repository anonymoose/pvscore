ToolCheckBox=function(_3d68){
ToolGeneric.call(this,_3d68);
};
ToolCheckBox.prototype=new ToolGeneric;
ToolCheckBox.prototype.type="ToolCheckBox";
ToolCheckBox.prototype.execute=function(x,y){
var _3d6b=new CheckBoxFigure();
_3d6b.setDimension(100,20);
this.palette.workflow.addFigure(_3d6b,x,y);
var _3d6c=this.palette.workflow.getBestCompartmentFigure(x,y);
if(_3d6c){
_3d6c.addChild(_3d6b);
}
ToolGeneric.prototype.execute.call(this,x,y);
};
