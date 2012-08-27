ToolGroup=function(_3b07){
ToolGeneric.call(this,_3b07);
this.setTooltip("Form Group");
};
ToolGroup.prototype=new ToolGeneric;
ToolGroup.prototype.type="ToolGroup";
ToolGroup.prototype.execute=function(x,y){
var _3b0a=new GroupFigure();
_3b0a.setDimension(100,60);
this.palette.workflow.addFigure(_3b0a,x,y);
ToolGeneric.prototype.execute.call(this,x,y);
};
