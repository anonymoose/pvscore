String.prototype.parseColor=function(){
var color="#";
if(this.slice(0,4)=="rgb("){
var cols=this.slice(4,this.length-1).split(",");
var i=0;
do{
color+=parseInt(cols[i]).toColorPart();
}while(++i<3);
}else{
if(this.slice(0,1)=="#"){
if(this.length==4){
for(var i=1;i<4;i++){
color+=(this.charAt(i)+this.charAt(i)).toLowerCase();
}
}
if(this.length==7){
color=this.toLowerCase();
}
}
}
return (color.length==7?color:(arguments[0]||this));
};
Element.collectTextNodes=function(_387b){
return $A($(_387b).childNodes).collect(function(node){
return (node.nodeType==3?node.nodeValue:(node.hasChildNodes()?Element.collectTextNodes(node):""));
}).flatten().join("");
};
Element.collectTextNodesIgnoreClass=function(_387d,_387e){
return $A($(_387d).childNodes).collect(function(node){
return (node.nodeType==3?node.nodeValue:((node.hasChildNodes()&&!Element.hasClassName(node,_387e))?Element.collectTextNodesIgnoreClass(node,_387e):""));
}).flatten().join("");
};
Element.setContentZoom=function(_3880,_3881){
_3880=$(_3880);
_3880.setStyle({fontSize:(_3881/100)+"em"});
if(navigator.appVersion.indexOf("AppleWebKit")>0){
window.scrollBy(0,0);
}
return _3880;
};
Element.getOpacity=function(_3882){
return $(_3882).getStyle("opacity");
};
Element.setOpacity=function(_3883,value){
return $(_3883).setStyle({opacity:value});
};
Element.getInlineOpacity=function(_3885){
return $(_3885).style.opacity||"";
};
Element.forceRerendering=function(_3886){
try{
_3886=$(_3886);
var n=document.createTextNode(" ");
_3886.appendChild(n);
_3886.removeChild(n);
}
catch(e){
}
};
Array.prototype.call=function(){
var args=arguments;
this.each(function(f){
f.apply(this,args);
});
};
var Effect={_elementDoesNotExistError:{name:"ElementDoesNotExistError",message:"The specified DOM element does not exist, but is required for this effect to operate"},tagifyText:function(_388a){
if(typeof Builder=="undefined"){
throw ("Effect.tagifyText requires including script.aculo.us' builder.js library");
}
var _388b="position:relative";
if(/MSIE/.test(navigator.userAgent)&&!window.opera){
_388b+=";zoom:1";
}
_388a=$(_388a);
$A(_388a.childNodes).each(function(child){
if(child.nodeType==3){
child.nodeValue.toArray().each(function(_388d){
_388a.insertBefore(Builder.node("span",{style:_388b},_388d==" "?String.fromCharCode(160):_388d),child);
});
Element.remove(child);
}
});
},multiple:function(_388e,_388f){
var _3890;
if(((typeof _388e=="object")||(typeof _388e=="function"))&&(_388e.length)){
_3890=_388e;
}else{
_3890=$(_388e).childNodes;
}
var _3891=Object.extend({speed:0.1,delay:0},arguments[2]||{});
var _3892=_3891.delay;
$A(_3890).each(function(_3893,index){
new _388f(_3893,Object.extend(_3891,{delay:index*_3891.speed+_3892}));
});
},PAIRS:{"slide":["SlideDown","SlideUp"],"blind":["BlindDown","BlindUp"],"appear":["Appear","Fade"]},toggle:function(_3895,_3896){
_3895=$(_3895);
_3896=(_3896||"appear").toLowerCase();
var _3897=Object.extend({queue:{position:"end",scope:(_3895.id||"global"),limit:1}},arguments[2]||{});
Effect[_3895.visible()?Effect.PAIRS[_3896][1]:Effect.PAIRS[_3896][0]](_3895,_3897);
}};
var Effect2=Effect;
Effect.Transitions={linear:Prototype.K,sinoidal:function(pos){
return (-Math.cos(pos*Math.PI)/2)+0.5;
},reverse:function(pos){
return 1-pos;
},flicker:function(pos){
return ((-Math.cos(pos*Math.PI)/4)+0.75)+Math.random()/4;
},wobble:function(pos){
return (-Math.cos(pos*Math.PI*(9*pos))/2)+0.5;
},pulse:function(pos,_389d){
_389d=_389d||5;
return (Math.round((pos%(1/_389d))*_389d)===0?((pos*_389d*2)-Math.floor(pos*_389d*2)):1-((pos*_389d*2)-Math.floor(pos*_389d*2)));
},none:function(pos){
return 0;
},full:function(pos){
return 1;
}};
Effect.ScopedQueue=Class.create();
Object.extend(Object.extend(Effect.ScopedQueue.prototype,Enumerable),{initialize:function(){
this.effects=[];
this.interval=null;
},_each:function(_38a0){
this.effects._each(_38a0);
},add:function(_38a1){
var _38a2=new Date().getTime();
var _38a3=(typeof _38a1.options.queue=="string")?_38a1.options.queue:_38a1.options.queue.position;
switch(_38a3){
case "front":
this.effects.findAll(function(e){
return e.state=="idle";
}).each(function(e){
e.startOn+=_38a1.finishOn;
e.finishOn+=_38a1.finishOn;
});
break;
case "with-last":
_38a2=this.effects.pluck("startOn").max()||_38a2;
break;
case "end":
_38a2=this.effects.pluck("finishOn").max()||_38a2;
break;
}
_38a1.startOn+=_38a2;
_38a1.finishOn+=_38a2;
if(!_38a1.options.queue.limit||(this.effects.length<_38a1.options.queue.limit)){
this.effects.push(_38a1);
}
if(!this.interval){
this.interval=setInterval(this.loop.bind(this),15);
}
},remove:function(_38a6){
this.effects=this.effects.reject(function(e){
return e==_38a6;
});
if(this.effects.length===0){
clearInterval(this.interval);
this.interval=null;
}
},loop:function(){
var _38a8=new Date().getTime();
for(var i=0,len=this.effects.length;i<len;i++){
if(this.effects[i]){
this.effects[i].loop(_38a8);
}
}
}});
Effect.Queues={instances:$H(),get:function(_38aa){
if(typeof _38aa!="string"){
return _38aa;
}
if(!this.instances[_38aa]){
this.instances[_38aa]=new Effect.ScopedQueue();
}
return this.instances[_38aa];
}};
Effect.Queue=Effect.Queues.get("global");
Effect.DefaultOptions={transition:Effect.Transitions.sinoidal,duration:1,fps:60,sync:false,from:0,to:1,delay:0,queue:"parallel"};
Effect.Base=function(){
};
Effect.Base.prototype={position:null,start:function(_38ab){
this.options=Object.extend(Object.extend({},Effect.DefaultOptions),_38ab||{});
this.currentFrame=0;
this.state="idle";
this.startOn=this.options.delay*1000;
this.finishOn=this.startOn+(this.options.duration*1000);
this.event("beforeStart");
if(!this.options.sync){
Effect.Queues.get(typeof this.options.queue=="string"?"global":this.options.queue.scope).add(this);
}
},loop:function(_38ac){
if(_38ac>=this.startOn){
if(_38ac>=this.finishOn){
this.render(1);
this.cancel();
this.event("beforeFinish");
if(this.finish){
this.finish();
}
this.event("afterFinish");
return;
}
var pos=(_38ac-this.startOn)/(this.finishOn-this.startOn);
var frame=Math.round(pos*this.options.fps*this.options.duration);
if(frame>this.currentFrame){
this.render(pos);
this.currentFrame=frame;
}
}
},render:function(pos){
if(this.state=="idle"){
this.state="running";
this.event("beforeSetup");
if(this.setup){
this.setup();
}
this.event("afterSetup");
}
if(this.state=="running"){
if(this.options.transition){
pos=this.options.transition(pos);
}
pos*=(this.options.to-this.options.from);
pos+=this.options.from;
this.position=pos;
this.event("beforeUpdate");
if(this.update){
this.update(pos);
}
this.event("afterUpdate");
}
},cancel:function(){
if(!this.options.sync){
Effect.Queues.get(typeof this.options.queue=="string"?"global":this.options.queue.scope).remove(this);
}
this.state="finished";
},event:function(_38b0){
if(this.options[_38b0+"Internal"]){
this.options[_38b0+"Internal"](this);
}
if(this.options[_38b0]){
this.options[_38b0](this);
}
},inspect:function(){
var data=$H();
for(property in this){
if(typeof this[property]!="function"){
data[property]=this[property];
}
}
return "#<Effect:"+data.inspect()+",options:"+$H(this.options).inspect()+">";
}};
Effect.Parallel=Class.create();
Object.extend(Object.extend(Effect.Parallel.prototype,Effect.Base.prototype),{initialize:function(_38b2){
this.effects=_38b2||[];
this.start(arguments[1]);
},update:function(_38b3){
this.effects.invoke("render",_38b3);
},finish:function(_38b4){
this.effects.each(function(_38b5){
_38b5.render(1);
_38b5.cancel();
_38b5.event("beforeFinish");
if(_38b5.finish){
_38b5.finish(_38b4);
}
_38b5.event("afterFinish");
});
}});
Effect.Event=Class.create();
Object.extend(Object.extend(Effect.Event.prototype,Effect.Base.prototype),{initialize:function(){
var _38b6=Object.extend({duration:0},arguments[0]||{});
this.start(_38b6);
},update:Prototype.emptyFunction});
Effect.Opacity=Class.create();
Object.extend(Object.extend(Effect.Opacity.prototype,Effect.Base.prototype),{initialize:function(_38b7){
this.element=$(_38b7);
if(!this.element){
throw (Effect._elementDoesNotExistError);
}
if(/MSIE/.test(navigator.userAgent)&&!window.opera&&(!this.element.currentStyle.hasLayout)){
this.element.setStyle({zoom:1});
}
var _38b8=Object.extend({from:this.element.getOpacity()||0,to:1},arguments[1]||{});
this.start(_38b8);
},update:function(_38b9){
this.element.setOpacity(_38b9);
}});
Effect.Move=Class.create();
Object.extend(Object.extend(Effect.Move.prototype,Effect.Base.prototype),{initialize:function(_38ba){
this.element=$(_38ba);
if(!this.element){
throw (Effect._elementDoesNotExistError);
}
var _38bb=Object.extend({x:0,y:0,mode:"relative"},arguments[1]||{});
this.start(_38bb);
},setup:function(){
this.element.makePositioned();
this.originalLeft=parseFloat(this.element.getStyle("left")||"0");
this.originalTop=parseFloat(this.element.getStyle("top")||"0");
if(this.options.mode=="absolute"){
this.options.x=this.options.x-this.originalLeft;
this.options.y=this.options.y-this.originalTop;
}
},update:function(_38bc){
this.element.setStyle({left:Math.round(this.options.x*_38bc+this.originalLeft)+"px",top:Math.round(this.options.y*_38bc+this.originalTop)+"px"});
}});
Effect.MoveBy=function(_38bd,toTop,_38bf){
return new Effect.Move(_38bd,Object.extend({x:_38bf,y:toTop},arguments[3]||{}));
};
Effect.Scale=Class.create();
Object.extend(Object.extend(Effect.Scale.prototype,Effect.Base.prototype),{initialize:function(_38c0,_38c1){
this.element=$(_38c0);
if(!this.element){
throw (Effect._elementDoesNotExistError);
}
var _38c2=Object.extend({scaleX:true,scaleY:true,scaleContent:true,scaleFromCenter:false,scaleMode:"box",scaleFrom:100,scaleTo:_38c1},arguments[2]||{});
this.start(_38c2);
},setup:function(){
this.restoreAfterFinish=this.options.restoreAfterFinish||false;
this.elementPositioning=this.element.getStyle("position");
this.originalStyle={};
["top","left","width","height","fontSize"].each(function(k){
this.originalStyle[k]=this.element.style[k];
}.bind(this));
this.originalTop=this.element.offsetTop;
this.originalLeft=this.element.offsetLeft;
var _38c4=this.element.getStyle("font-size")||"100%";
["em","px","%","pt"].each(function(_38c5){
if(_38c4.indexOf(_38c5)>0){
this.fontSize=parseFloat(_38c4);
this.fontSizeType=_38c5;
}
}.bind(this));
this.factor=(this.options.scaleTo-this.options.scaleFrom)/100;
this.dims=null;
if(this.options.scaleMode=="box"){
this.dims=[this.element.offsetHeight,this.element.offsetWidth];
}
if(/^content/.test(this.options.scaleMode)){
this.dims=[this.element.scrollHeight,this.element.scrollWidth];
}
if(!this.dims){
this.dims=[this.options.scaleMode.originalHeight,this.options.scaleMode.originalWidth];
}
},update:function(_38c6){
var _38c7=(this.options.scaleFrom/100)+(this.factor*_38c6);
if(this.options.scaleContent&&this.fontSize){
this.element.setStyle({fontSize:this.fontSize*_38c7+this.fontSizeType});
}
this.setDimensions(this.dims[0]*_38c7,this.dims[1]*_38c7);
},finish:function(_38c8){
if(this.restoreAfterFinish){
this.element.setStyle(this.originalStyle);
}
},setDimensions:function(_38c9,width){
var d={};
if(this.options.scaleX){
d.width=Math.round(width)+"px";
}
if(this.options.scaleY){
d.height=Math.round(_38c9)+"px";
}
if(this.options.scaleFromCenter){
var topd=(_38c9-this.dims[0])/2;
var leftd=(width-this.dims[1])/2;
if(this.elementPositioning=="absolute"){
if(this.options.scaleY){
d.top=this.originalTop-topd+"px";
}
if(this.options.scaleX){
d.left=this.originalLeft-leftd+"px";
}
}else{
if(this.options.scaleY){
d.top=-topd+"px";
}
if(this.options.scaleX){
d.left=-leftd+"px";
}
}
}
this.element.setStyle(d);
}});
Effect.Highlight=Class.create();
Object.extend(Object.extend(Effect.Highlight.prototype,Effect.Base.prototype),{initialize:function(_38ce){
this.element=$(_38ce);
if(!this.element){
throw (Effect._elementDoesNotExistError);
}
var _38cf=Object.extend({startcolor:"#ffff99"},arguments[1]||{});
this.start(_38cf);
},setup:function(){
if(this.element.getStyle("display")=="none"){
this.cancel();
return;
}
this.oldStyle={};
if(!this.options.keepBackgroundImage){
this.oldStyle.backgroundImage=this.element.getStyle("background-image");
this.element.setStyle({backgroundImage:"none"});
}
if(!this.options.endcolor){
this.options.endcolor=this.element.getStyle("background-color").parseColor("#ffffff");
}
if(!this.options.restorecolor){
this.options.restorecolor=this.element.getStyle("background-color");
}
this._base=$R(0,2).map(function(i){
return parseInt(this.options.startcolor.slice(i*2+1,i*2+3),16);
}.bind(this));
this._delta=$R(0,2).map(function(i){
return parseInt(this.options.endcolor.slice(i*2+1,i*2+3),16)-this._base[i];
}.bind(this));
},update:function(_38d2){
this.element.setStyle({backgroundColor:$R(0,2).inject("#",function(m,v,i){
return m+(Math.round(this._base[i]+(this._delta[i]*_38d2)).toColorPart());
}.bind(this))});
},finish:function(){
this.element.setStyle(Object.extend(this.oldStyle,{backgroundColor:this.options.restorecolor}));
}});
Effect.ScrollTo=Class.create();
Object.extend(Object.extend(Effect.ScrollTo.prototype,Effect.Base.prototype),{initialize:function(_38d6){
this.element=$(_38d6);
this.start(arguments[1]||{});
},setup:function(){
Position.prepare();
var _38d7=Position.cumulativeOffset(this.element);
if(this.options.offset){
_38d7[1]+=this.options.offset;
}
var max=window.innerHeight?window.height-window.innerHeight:document.body.scrollHeight-(document.documentElement.clientHeight?document.documentElement.clientHeight:document.body.clientHeight);
this.scrollStart=Position.deltaY;
this.delta=(_38d7[1]>max?max:_38d7[1])-this.scrollStart;
},update:function(_38d9){
Position.prepare();
window.scrollTo(Position.deltaX,this.scrollStart+(_38d9*this.delta));
}});
Effect.Fade=function(_38da){
_38da=$(_38da);
var _38db=_38da.getInlineOpacity();
var _38dc=Object.extend({from:_38da.getOpacity()||1,to:0,afterFinishInternal:function(_38dd){
if(_38dd.options.to!=0){
return;
}
_38dd.element.hide().setStyle({opacity:_38db});
}},arguments[1]||{});
return new Effect.Opacity(_38da,_38dc);
};
Effect.Appear=function(_38de){
_38de=$(_38de);
var _38df=Object.extend({from:(_38de.getStyle("display")=="none"?0:_38de.getOpacity()||0),to:1,afterFinishInternal:function(_38e0){
_38e0.element.forceRerendering();
},beforeSetup:function(_38e1){
_38e1.element.setOpacity(_38e1.options.from).show();
}},arguments[1]||{});
return new Effect.Opacity(_38de,_38df);
};
Effect.Puff=function(_38e2){
_38e2=$(_38e2);
var _38e3={opacity:_38e2.getInlineOpacity(),position:_38e2.getStyle("position"),top:_38e2.style.top,left:_38e2.style.left,width:_38e2.style.width,height:_38e2.style.height};
return new Effect.Parallel([new Effect.Scale(_38e2,200,{sync:true,scaleFromCenter:true,scaleContent:true,restoreAfterFinish:true}),new Effect.Opacity(_38e2,{sync:true,to:0})],Object.extend({duration:1,beforeSetupInternal:function(_38e4){
Position.absolutize(_38e4.effects[0].element);
},afterFinishInternal:function(_38e5){
_38e5.effects[0].element.hide().setStyle(_38e3);
}},arguments[1]||{}));
};
Effect.BlindUp=function(_38e6){
_38e6=$(_38e6);
_38e6.makeClipping();
return new Effect.Scale(_38e6,0,Object.extend({scaleContent:false,scaleX:false,restoreAfterFinish:true,afterFinishInternal:function(_38e7){
_38e7.element.hide().undoClipping();
}},arguments[1]||{}));
};
Effect.BlindDown=function(_38e8){
_38e8=$(_38e8);
var _38e9=_38e8.getDimensions();
return new Effect.Scale(_38e8,100,Object.extend({scaleContent:false,scaleX:false,scaleFrom:0,scaleMode:{originalHeight:_38e9.height,originalWidth:_38e9.width},restoreAfterFinish:true,afterSetup:function(_38ea){
_38ea.element.makeClipping().setStyle({height:"0px"}).show();
},afterFinishInternal:function(_38eb){
_38eb.element.undoClipping();
}},arguments[1]||{}));
};
Effect.SwitchOff=function(_38ec){
_38ec=$(_38ec);
var _38ed=_38ec.getInlineOpacity();
return new Effect.Appear(_38ec,Object.extend({duration:0.4,from:0,transition:Effect.Transitions.flicker,afterFinishInternal:function(_38ee){
new Effect.Scale(_38ee.element,1,{duration:0.3,scaleFromCenter:true,scaleX:false,scaleContent:false,restoreAfterFinish:true,beforeSetup:function(_38ef){
_38ef.element.makePositioned().makeClipping();
},afterFinishInternal:function(_38f0){
_38f0.element.hide().undoClipping().undoPositioned().setStyle({opacity:_38ed});
}});
}},arguments[1]||{}));
};
Effect.DropOut=function(_38f1){
_38f1=$(_38f1);
var _38f2={top:_38f1.getStyle("top"),left:_38f1.getStyle("left"),opacity:_38f1.getInlineOpacity()};
return new Effect.Parallel([new Effect.Move(_38f1,{x:0,y:100,sync:true}),new Effect.Opacity(_38f1,{sync:true,to:0})],Object.extend({duration:0.5,beforeSetup:function(_38f3){
_38f3.effects[0].element.makePositioned();
},afterFinishInternal:function(_38f4){
_38f4.effects[0].element.hide().undoPositioned().setStyle(_38f2);
}},arguments[1]||{}));
};
Effect.Shake=function(_38f5){
_38f5=$(_38f5);
var _38f6={top:_38f5.getStyle("top"),left:_38f5.getStyle("left")};
return new Effect.Move(_38f5,{x:20,y:0,duration:0.05,afterFinishInternal:function(_38f7){
new Effect.Move(_38f7.element,{x:-40,y:0,duration:0.1,afterFinishInternal:function(_38f8){
new Effect.Move(_38f8.element,{x:40,y:0,duration:0.1,afterFinishInternal:function(_38f9){
new Effect.Move(_38f9.element,{x:-40,y:0,duration:0.1,afterFinishInternal:function(_38fa){
new Effect.Move(_38fa.element,{x:40,y:0,duration:0.1,afterFinishInternal:function(_38fb){
new Effect.Move(_38fb.element,{x:-20,y:0,duration:0.05,afterFinishInternal:function(_38fc){
_38fc.element.undoPositioned().setStyle(_38f6);
}});
}});
}});
}});
}});
}});
};
Effect.SlideDown=function(_38fd){
_38fd=$(_38fd).cleanWhitespace();
var _38fe=_38fd.down().getStyle("bottom");
var _38ff=_38fd.getDimensions();
return new Effect.Scale(_38fd,100,Object.extend({scaleContent:false,scaleX:false,scaleFrom:window.opera?0:1,scaleMode:{originalHeight:_38ff.height,originalWidth:_38ff.width},restoreAfterFinish:true,afterSetup:function(_3900){
_3900.element.makePositioned();
_3900.element.down().makePositioned();
if(window.opera){
_3900.element.setStyle({top:""});
}
_3900.element.makeClipping().setStyle({height:"0px"}).show();
},afterUpdateInternal:function(_3901){
_3901.element.down().setStyle({bottom:(_3901.dims[0]-_3901.element.clientHeight)+"px"});
},afterFinishInternal:function(_3902){
_3902.element.undoClipping().undoPositioned();
_3902.element.down().undoPositioned().setStyle({bottom:_38fe});
}},arguments[1]||{}));
};
Effect.SlideUp=function(_3903){
_3903=$(_3903).cleanWhitespace();
var _3904=_3903.down().getStyle("bottom");
return new Effect.Scale(_3903,window.opera?0:1,Object.extend({scaleContent:false,scaleX:false,scaleMode:"box",scaleFrom:100,restoreAfterFinish:true,beforeStartInternal:function(_3905){
_3905.element.makePositioned();
_3905.element.down().makePositioned();
if(window.opera){
_3905.element.setStyle({top:""});
}
_3905.element.makeClipping().show();
},afterUpdateInternal:function(_3906){
_3906.element.down().setStyle({bottom:(_3906.dims[0]-_3906.element.clientHeight)+"px"});
},afterFinishInternal:function(_3907){
_3907.element.hide().undoClipping().undoPositioned().setStyle({bottom:_3904});
_3907.element.down().undoPositioned();
}},arguments[1]||{}));
};
Effect.Squish=function(_3908){
return new Effect.Scale(_3908,window.opera?1:0,{restoreAfterFinish:true,beforeSetup:function(_3909){
_3909.element.makeClipping();
},afterFinishInternal:function(_390a){
_390a.element.hide().undoClipping();
}});
};
Effect.Grow=function(_390b){
_390b=$(_390b);
var _390c=Object.extend({direction:"center",moveTransition:Effect.Transitions.sinoidal,scaleTransition:Effect.Transitions.sinoidal,opacityTransition:Effect.Transitions.full},arguments[1]||{});
var _390d={top:_390b.style.top,left:_390b.style.left,height:_390b.style.height,width:_390b.style.width,opacity:_390b.getInlineOpacity()};
var dims=_390b.getDimensions();
var _390f,initialMoveY;
var moveX,moveY;
switch(_390c.direction){
case "top-left":
_390f=initialMoveY=moveX=moveY=0;
break;
case "top-right":
_390f=dims.width;
initialMoveY=moveY=0;
moveX=-dims.width;
break;
case "bottom-left":
_390f=moveX=0;
initialMoveY=dims.height;
moveY=-dims.height;
break;
case "bottom-right":
_390f=dims.width;
initialMoveY=dims.height;
moveX=-dims.width;
moveY=-dims.height;
break;
case "center":
_390f=dims.width/2;
initialMoveY=dims.height/2;
moveX=-dims.width/2;
moveY=-dims.height/2;
break;
}
return new Effect.Move(_390b,{x:_390f,y:initialMoveY,duration:0.01,beforeSetup:function(_3911){
_3911.element.hide().makeClipping().makePositioned();
},afterFinishInternal:function(_3912){
new Effect.Parallel([new Effect.Opacity(_3912.element,{sync:true,to:1,from:0,transition:_390c.opacityTransition}),new Effect.Move(_3912.element,{x:moveX,y:moveY,sync:true,transition:_390c.moveTransition}),new Effect.Scale(_3912.element,100,{scaleMode:{originalHeight:dims.height,originalWidth:dims.width},sync:true,scaleFrom:window.opera?1:0,transition:_390c.scaleTransition,restoreAfterFinish:true})],Object.extend({beforeSetup:function(_3913){
_3913.effects[0].element.setStyle({height:"0px"}).show();
},afterFinishInternal:function(_3914){
_3914.effects[0].element.undoClipping().undoPositioned().setStyle(_390d);
}},_390c));
}});
};
Effect.Shrink=function(_3915){
_3915=$(_3915);
var _3916=Object.extend({direction:"center",moveTransition:Effect.Transitions.sinoidal,scaleTransition:Effect.Transitions.sinoidal,opacityTransition:Effect.Transitions.none},arguments[1]||{});
var _3917={top:_3915.style.top,left:_3915.style.left,height:_3915.style.height,width:_3915.style.width,opacity:_3915.getInlineOpacity()};
var dims=_3915.getDimensions();
var moveX,moveY;
switch(_3916.direction){
case "top-left":
moveX=moveY=0;
break;
case "top-right":
moveX=dims.width;
moveY=0;
break;
case "bottom-left":
moveX=0;
moveY=dims.height;
break;
case "bottom-right":
moveX=dims.width;
moveY=dims.height;
break;
case "center":
moveX=dims.width/2;
moveY=dims.height/2;
break;
}
return new Effect.Parallel([new Effect.Opacity(_3915,{sync:true,to:0,from:1,transition:_3916.opacityTransition}),new Effect.Scale(_3915,window.opera?1:0,{sync:true,transition:_3916.scaleTransition,restoreAfterFinish:true}),new Effect.Move(_3915,{x:moveX,y:moveY,sync:true,transition:_3916.moveTransition})],Object.extend({beforeStartInternal:function(_391a){
_391a.effects[0].element.makePositioned().makeClipping();
},afterFinishInternal:function(_391b){
_391b.effects[0].element.hide().undoClipping().undoPositioned().setStyle(_3917);
}},_3916));
};
Effect.Pulsate=function(_391c){
_391c=$(_391c);
var _391d=arguments[1]||{};
var _391e=_391c.getInlineOpacity();
var _391f=_391d.transition||Effect.Transitions.sinoidal;
var _3920=function(pos){
return _391f(1-Effect.Transitions.pulse(pos,_391d.pulses));
};
_3920.bind(_391f);
return new Effect.Opacity(_391c,Object.extend(Object.extend({duration:2,from:0,afterFinishInternal:function(_3922){
_3922.element.setStyle({opacity:_391e});
}},_391d),{transition:_3920}));
};
Effect.Fold=function(_3923){
_3923=$(_3923);
var _3924={top:_3923.style.top,left:_3923.style.left,width:_3923.style.width,height:_3923.style.height};
_3923.makeClipping();
return new Effect.Scale(_3923,5,Object.extend({scaleContent:false,scaleX:false,afterFinishInternal:function(_3925){
new Effect.Scale(_3923,1,{scaleContent:false,scaleY:false,afterFinishInternal:function(_3926){
_3926.element.hide().undoClipping().setStyle(_3924);
}});
}},arguments[1]||{}));
};
Effect.Morph=Class.create();
Object.extend(Object.extend(Effect.Morph.prototype,Effect.Base.prototype),{initialize:function(_3927){
this.element=$(_3927);
if(!this.element){
throw (Effect._elementDoesNotExistError);
}
var _3928=Object.extend({style:{}},arguments[1]||{});
if(typeof _3928.style=="string"){
if(_3928.style.indexOf(":")==-1){
var _3929="",selector="."+_3928.style;
$A(document.styleSheets).reverse().each(function(_392a){
if(_392a.cssRules){
cssRules=_392a.cssRules;
}else{
if(_392a.rules){
cssRules=_392a.rules;
}
}
$A(cssRules).reverse().each(function(rule){
if(selector==rule.selectorText){
_3929=rule.style.cssText;
throw $break;
}
});
if(_3929){
throw $break;
}
});
this.style=_3929.parseStyle();
_3928.afterFinishInternal=function(_392c){
_392c.element.addClassName(_392c.options.style);
_392c.transforms.each(function(_392d){
if(_392d.style!="opacity"){
_392c.element.style[_392d.style.camelize()]="";
}
});
};
}else{
this.style=_3928.style.parseStyle();
}
}else{
this.style=$H(_3928.style);
}
this.start(_3928);
},setup:function(){
function parseColor(color){
if(!color||["rgba(0, 0, 0, 0)","transparent"].include(color)){
color="#ffffff";
}
color=color.parseColor();
return $R(0,2).map(function(i){
return parseInt(color.slice(i*2+1,i*2+3),16);
});
}
this.transforms=this.style.map(function(pair){
var _3931=pair[0].underscore().dasherize(),value=pair[1],unit=null;
if(value.parseColor("#zzzzzz")!="#zzzzzz"){
value=value.parseColor();
unit="color";
}else{
if(_3931=="opacity"){
value=parseFloat(value);
if(/MSIE/.test(navigator.userAgent)&&!window.opera&&(!this.element.currentStyle.hasLayout)){
this.element.setStyle({zoom:1});
}
}else{
if(Element.CSS_LENGTH.test(value)){
var _3932=value.match(/^([\+\-]?[0-9\.]+)(.*)$/),value=parseFloat(_3932[1]),unit=(_3932.length==3)?_3932[2]:null;
}
}
}
var _3933=this.element.getStyle(_3931);
return $H({style:_3931,originalValue:unit=="color"?parseColor(_3933):parseFloat(_3933||0),targetValue:unit=="color"?parseColor(value):value,unit:unit});
}.bind(this)).reject(function(_3934){
return ((_3934.originalValue==_3934.targetValue)||(_3934.unit!="color"&&(isNaN(_3934.originalValue)||isNaN(_3934.targetValue))));
});
},update:function(_3935){
var style=$H(),value=null;
this.transforms.each(function(_3937){
value=_3937.unit=="color"?$R(0,2).inject("#",function(m,v,i){
return m+(Math.round(_3937.originalValue[i]+(_3937.targetValue[i]-_3937.originalValue[i])*_3935)).toColorPart();
}):_3937.originalValue+Math.round(((_3937.targetValue-_3937.originalValue)*_3935)*1000)/1000+_3937.unit;
style[_3937.style]=value;
});
this.element.setStyle(style);
}});
Effect.Transform=Class.create();
Object.extend(Effect.Transform.prototype,{initialize:function(_393b){
this.tracks=[];
this.options=arguments[1]||{};
this.addTracks(_393b);
},addTracks:function(_393c){
_393c.each(function(track){
var data=$H(track).values().first();
this.tracks.push($H({ids:$H(track).keys().first(),effect:Effect.Morph,options:{style:data}}));
}.bind(this));
return this;
},play:function(){
return new Effect.Parallel(this.tracks.map(function(track){
var _3940=[$(track.ids)||$$(track.ids)].flatten();
return _3940.map(function(e){
return new track.effect(e,Object.extend({sync:true},track.options));
});
}).flatten(),this.options);
}});
Element.CSS_PROPERTIES=$w("backgroundColor backgroundPosition borderBottomColor borderBottomStyle "+"borderBottomWidth borderLeftColor borderLeftStyle borderLeftWidth "+"borderRightColor borderRightStyle borderRightWidth borderSpacing "+"borderTopColor borderTopStyle borderTopWidth bottom clip color "+"fontSize fontWeight height left letterSpacing lineHeight "+"marginBottom marginLeft marginRight marginTop markerOffset maxHeight "+"maxWidth minHeight minWidth opacity outlineColor outlineOffset "+"outlineWidth paddingBottom paddingLeft paddingRight paddingTop "+"right textIndent top width wordSpacing zIndex");
Element.CSS_LENGTH=/^(([\+\-]?[0-9\.]+)(em|ex|px|in|cm|mm|pt|pc|\%))|0$/;
String.prototype.parseStyle=function(){
var _3942=Element.extend(document.createElement("div"));
_3942.innerHTML="<div style=\""+this+"\"></div>";
var style=_3942.down().style,styleRules=$H();
Element.CSS_PROPERTIES.each(function(_3944){
if(style[_3944]){
styleRules[_3944]=style[_3944];
}
});
if(/MSIE/.test(navigator.userAgent)&&!window.opera&&this.indexOf("opacity")>-1){
styleRules.opacity=this.match(/opacity:\s*((?:0|1)?(?:\.\d*)?)/)[1];
}
return styleRules;
};
Element.morph=function(_3945,style){
new Effect.Morph(_3945,Object.extend({style:style},arguments[2]||{}));
return _3945;
};
["setOpacity","getOpacity","getInlineOpacity","forceRerendering","setContentZoom","collectTextNodes","collectTextNodesIgnoreClass","morph"].each(function(f){
Element.Methods[f]=Element[f];
});
Element.Methods.visualEffect=function(_3948,_3949,_394a){
s=_3949.gsub(/_/,"-").camelize();
effect_class=s.charAt(0).toUpperCase()+s.substring(1);
new Effect[effect_class](_3948,_394a);
return $(_3948);
};
Element.addMethods();
