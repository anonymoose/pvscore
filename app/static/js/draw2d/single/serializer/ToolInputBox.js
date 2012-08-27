ToolInputBox=function(_386d){
ToolGeneric.call(this,_386d);
};
ToolInputBox.prototype=new ToolGeneric;
ToolInputBox.prototype.type="ToolInputBox";
ToolInputBox.prototype.execute=function(x,y){
var _3870=new InputBoxFigure();
_3870.setDimension(100,20);
this.palette.workflow.addFigure(_3870,x,y);
var _3871=this.palette.workflow.getBestCompartmentFigure(x,y);
if(_3871){
_3871.addChild(_3870);
}
ToolGeneric.prototype.execute.call(this,x,y);
};
