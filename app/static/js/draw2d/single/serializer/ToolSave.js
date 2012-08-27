ToolSave=function(_3d9a){
ToolGeneric.call(this,_3d9a);
};
ToolSave.prototype=new Button();
ToolSave.prototype.type="ToolSave";
ToolSave.prototype.execute=function(x,y){
alert(new XMLSerializer_01().toXML(this.palette.workflow.getDocument()));
};
