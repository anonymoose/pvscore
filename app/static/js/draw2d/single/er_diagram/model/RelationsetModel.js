RelationsetModel=function(){
this.relations=new ArrayList();
this.nonPersistentTableAliases=new ArrayList();
};
RelationsetModel.prototype.type="RelationsetModel";
RelationsetModel.prototype.getRelationModels=function(){
return this.relations;
};
RelationsetModel.prototype.getTableAliasModels=function(){
return this.nonPersistentTableAliases;
};
RelationsetModel.prototype.addRelationModel=function(_4a0e){
this.relations.add(_4a0e);
if(this.nonPersistentTableAliases.indexOf(_4a0e.getToTableModel())<=0){
this.nonPersistentTableAliases.add(_4a0e.getToTableModel());
}
if(this.nonPersistentTableAliases.indexOf(_4a0e.getFromTableModel())<=0){
this.nonPersistentTableAliases.add(_4a0e.getFromTableModel());
}
};
RelationsetModel.prototype.getPosition=function(_4a0f){
return new Point(100,100);
};
