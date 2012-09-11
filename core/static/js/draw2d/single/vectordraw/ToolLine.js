ToolLine=function(_3de1){
ToolGeneric.call(this,_3de1);
this.setDimension(24,24);
};
ToolLine.prototype=new ToolGeneric();
ToolLine.prototype.type="ToolLine";
ToolLine.prototype.execute=function(x,y){
var _3de4=new Line();
_3de4.setStartPoint(x,y);
_3de4.setEndPoint(x+100,y+100);
this.palette.workflow.getCommandStack().execute(new CommandAdd(this.palette.workflow,_3de4));
ToolGeneric.prototype.execute.call(this,x,y);
};
