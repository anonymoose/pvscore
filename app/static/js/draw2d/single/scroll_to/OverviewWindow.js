OverviewWindow=function(name){
WindowFigure.call(this,"Overview Window");
this.setDimension(180,150);
this.servers={};
this.name=name;
};
OverviewWindow.prototype=new WindowFigure();
OverviewWindow.prototype.type="OverviewWindow";
OverviewWindow.prototype.createHTMLElement=function(){
var item=WindowFigure.prototype.createHTMLElement.call(this);
this.inputDiv=document.createElement("div");
this.inputDiv.style.position="absolute";
this.inputDiv.style.left="10px";
this.inputDiv.style.top="20px";
this.inputDiv.style.overflow="auto";
this.inputDiv.style.border="1px solid black";
this.inputDiv.style.font="normal 10px verdana";
item.appendChild(this.inputDiv);
return item;
};
OverviewWindow.prototype.setDimension=function(w,h){
WindowFigure.prototype.setDimension.call(this,w,h);
if(this.inputDiv!==null){
this.inputDiv.style.height=(h-30)+"px";
this.inputDiv.style.width=(w-20)+"px";
}
};
OverviewWindow.prototype.addServer=function(_43d3){
this.servers[_43d3.id]=_43d3;
this.createList();
};
OverviewWindow.prototype.removeServer=function(_43d4){
this.servers[_43d4.id]=null;
this.createList();
};
OverviewWindow.prototype.createList=function(){
this.inputDiv.innerHTML="";
var list=document.createElement("ul");
for(key in this.servers){
var _43d6=this.servers[key];
if(_43d6!==null){
var li=document.createElement("li");
var a=document.createElement("a");
a.href="javascript:OverviewWindow.scrollTo('"+_43d6.id+"')";
a.innerHTML=_43d6.ip;
li.appendChild(a);
if(_43d6.isReachable()){
a.style.color="green";
}else{
a.style.color="red";
a.style.fontWeight="bold";
}
list.appendChild(li);
}
}
this.inputDiv.appendChild(list);
};
OverviewWindow.scrollTo=function(id){
var _43da=workflow.getFigure(id);
workflow.scrollTo(_43da.getX()-OverviewWindow.screenWidth()/2,_43da.getY()-OverviewWindow.screenHeight()/2);
};
OverviewWindow.prototype.onDragend=function(){
WindowFigure.prototype.onDragend.call(this);
};
OverviewWindow.screenWidth=function(){
var _43db=0;
if(typeof (window.innerWidth)=="number"){
_43db=window.innerWidth;
}else{
if(document.documentElement&&(document.documentElement.clientWidth||document.documentElement.clientHeight)){
_43db=document.documentElement.clientWidth;
}else{
if(document.body&&(document.body.clientWidth||document.body.clientHeight)){
_43db=document.body.clientWidth;
}
}
}
return _43db;
};
OverviewWindow.screenHeight=function(){
var _43dc=0;
if(typeof (window.innerWidth)=="number"){
_43dc=window.innerHeight;
}else{
if(document.documentElement&&(document.documentElement.clientWidth||document.documentElement.clientHeight)){
_43dc=document.documentElement.clientHeight;
}else{
if(document.body&&(document.body.clientWidth||document.body.clientHeight)){
_43dc=document.body.clientHeight;
}
}
}
return _43dc;
};
