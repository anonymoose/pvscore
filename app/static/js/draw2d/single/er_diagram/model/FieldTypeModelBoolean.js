FieldTypeModelBoolean=function(_42c1){
FieldTypeModel.call(this,FieldModel.DBTYPE_BOOLEAN);
this.defaultValue=_42c1;
};
FieldTypeModelBoolean.prototype.type="FieldTypeModelBoolean";
FieldTypeModelBoolean.prototype=new FieldTypeModel;
FieldTypeModelBoolean.prototype.getDefault=function(){
return this.defaultValue;
};
FieldTypeModelBoolean.prototype.setDefault=function(value){
var save=this.getDefault();
if(save==value){
return;
}
this.defaultValue=value;
this.parent.firePropertyChange(PROPERTY_DEFAULT,save,value);
};
