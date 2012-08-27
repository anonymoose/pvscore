RelationModel=function(_3c2f,_3c30,toKey){
this.fromTable=_3c2f;
this.toTable=_3c30;
this.toKey=toKey;
};
RelationModel.prototype.type="RelationModel";
RelationModel.prototype.getFromTableModel=function(){
return this.fromTable;
};
RelationModel.prototype.getToTableModel=function(){
return this.toTable;
};
