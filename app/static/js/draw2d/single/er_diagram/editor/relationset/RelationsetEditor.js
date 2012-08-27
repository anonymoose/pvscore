RelationsetEditor=function(id,_3b81){
Workflow.call(this,id);
this.relationset=_3b81;
var _3b82=this.relationset.getTableAliasModels();
for(var i=0;i<_3b82.getSize();i++){
var _3b84=new TableAliasFigure(_3b82.get(i));
this.addFigure(_3b84);
}
};
RelationsetEditor.prototype=new Workflow();
RelationsetEditor.prototype.type="RelationsetEditor";
