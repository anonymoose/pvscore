/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

String.prototype.parseColor=function(){var _718="#";if(this.slice(0,4)=="rgb("){var cols=this.slice(4,this.length-1).split(",");var i=0;do{_718+=parseInt(cols[i]).toColorPart();}while(++i<3);}else{if(this.slice(0,1)=="#"){if(this.length==4){for(var i=1;i<4;i++){_718+=(this.charAt(i)+this.charAt(i)).toLowerCase();}}if(this.length==7){_718=this.toLowerCase();}}}return (_718.length==7?_718:(arguments[0]||this));};Element.collectTextNodes=function(_71b){return $A($(_71b).childNodes).collect(function(node){return (node.nodeType==3?node.nodeValue:(node.hasChildNodes()?Element.collectTextNodes(node):""));}).flatten().join("");};Element.collectTextNodesIgnoreClass=function(_71d,_71e){return $A($(_71d).childNodes).collect(function(node){return (node.nodeType==3?node.nodeValue:((node.hasChildNodes()&&!Element.hasClassName(node,_71e))?Element.collectTextNodesIgnoreClass(node,_71e):""));}).flatten().join("");};Element.setContentZoom=function(_720,_721){_720=$(_720);_720.setStyle({fontSize:(_721/100)+"em"});if(navigator.appVersion.indexOf("AppleWebKit")>0){window.scrollBy(0,0);}return _720;};Element.getOpacity=function(_722){return $(_722).getStyle("opacity");};Element.setOpacity=function(_723,_724){return $(_723).setStyle({opacity:_724});};Element.getInlineOpacity=function(_725){return $(_725).style.opacity||"";};Element.forceRerendering=function(_726){try{_726=$(_726);var n=document.createTextNode(" ");_726.appendChild(n);_726.removeChild(n);}catch(e){}};Array.prototype.call=function(){var args=arguments;this.each(function(f){f.apply(this,args);});};var Effect={_elementDoesNotExistError:{name:"ElementDoesNotExistError",message:"The specified DOM element does not exist, but is required for this effect to operate"},tagifyText:function(_72a){if(typeof Builder=="undefined"){throw ("Effect.tagifyText requires including script.aculo.us' builder.js library");}var _72b="position:relative";if(/MSIE/.test(navigator.userAgent)&&!window.opera){_72b+=";zoom:1";}_72a=$(_72a);$A(_72a.childNodes).each(function(_72c){if(_72c.nodeType==3){_72c.nodeValue.toArray().each(function(_72d){_72a.insertBefore(Builder.node("span",{style:_72b},_72d==" "?String.fromCharCode(160):_72d),_72c);});Element.remove(_72c);}});},multiple:function(_72e,_72f){var _730;if(((typeof _72e=="object")||(typeof _72e=="function"))&&(_72e.length)){_730=_72e;}else{_730=$(_72e).childNodes;}var _731=Object.extend({speed:0.1,delay:0},arguments[2]||{});var _732=_731.delay;$A(_730).each(function(_733,_734){new _72f(_733,Object.extend(_731,{delay:_734*_731.speed+_732}));});},PAIRS:{"slide":["SlideDown","SlideUp"],"blind":["BlindDown","BlindUp"],"appear":["Appear","Fade"]},toggle:function(_735,_736){_735=$(_735);_736=(_736||"appear").toLowerCase();var _737=Object.extend({queue:{position:"end",scope:(_735.id||"global"),limit:1}},arguments[2]||{});Effect[_735.visible()?Effect.PAIRS[_736][1]:Effect.PAIRS[_736][0]](_735,_737);}};var Effect2=Effect;Effect.Transitions={linear:Prototype.K,sinoidal:function(pos){return (-Math.cos(pos*Math.PI)/2)+0.5;},reverse:function(pos){return 1-pos;},flicker:function(pos){return ((-Math.cos(pos*Math.PI)/4)+0.75)+Math.random()/4;},wobble:function(pos){return (-Math.cos(pos*Math.PI*(9*pos))/2)+0.5;},pulse:function(pos,_73d){_73d=_73d||5;return (Math.round((pos%(1/_73d))*_73d)===0?((pos*_73d*2)-Math.floor(pos*_73d*2)):1-((pos*_73d*2)-Math.floor(pos*_73d*2)));},none:function(pos){return 0;},full:function(pos){return 1;}};Effect.ScopedQueue=Class.create();Object.extend(Object.extend(Effect.ScopedQueue.prototype,Enumerable),{initialize:function(){this.effects=[];this.interval=null;},_each:function(_740){this.effects._each(_740);},add:function(_741){var _742=new Date().getTime();var _743=(typeof _741.options.queue=="string")?_741.options.queue:_741.options.queue.position;switch(_743){case "front":this.effects.findAll(function(e){return e.state=="idle";}).each(function(e){e.startOn+=_741.finishOn;e.finishOn+=_741.finishOn;});break;case "with-last":_742=this.effects.pluck("startOn").max()||_742;break;case "end":_742=this.effects.pluck("finishOn").max()||_742;break;}_741.startOn+=_742;_741.finishOn+=_742;if(!_741.options.queue.limit||(this.effects.length<_741.options.queue.limit)){this.effects.push(_741);}if(!this.interval){this.interval=setInterval(this.loop.bind(this),15);}},remove:function(_746){this.effects=this.effects.reject(function(e){return e==_746;});if(this.effects.length===0){clearInterval(this.interval);this.interval=null;}},loop:function(){var _748=new Date().getTime();for(var i=0,len=this.effects.length;i<len;i++){if(this.effects[i]){this.effects[i].loop(_748);}}}});Effect.Queues={instances:$H(),get:function(_74a){if(typeof _74a!="string"){return _74a;}if(!this.instances[_74a]){this.instances[_74a]=new Effect.ScopedQueue();}return this.instances[_74a];}};Effect.Queue=Effect.Queues.get("global");Effect.DefaultOptions={transition:Effect.Transitions.sinoidal,duration:1,fps:60,sync:false,from:0,to:1,delay:0,queue:"parallel"};Effect.Base=function(){};Effect.Base.prototype={position:null,start:function(_74b){this.options=Object.extend(Object.extend({},Effect.DefaultOptions),_74b||{});this.currentFrame=0;this.state="idle";this.startOn=this.options.delay*1000;this.finishOn=this.startOn+(this.options.duration*1000);this.event("beforeStart");if(!this.options.sync){Effect.Queues.get(typeof this.options.queue=="string"?"global":this.options.queue.scope).add(this);}},loop:function(_74c){if(_74c>=this.startOn){if(_74c>=this.finishOn){this.render(1);this.cancel();this.event("beforeFinish");if(this.finish){this.finish();}this.event("afterFinish");return;}var pos=(_74c-this.startOn)/(this.finishOn-this.startOn);var _74e=Math.round(pos*this.options.fps*this.options.duration);if(_74e>this.currentFrame){this.render(pos);this.currentFrame=_74e;}}},render:function(pos){if(this.state=="idle"){this.state="running";this.event("beforeSetup");if(this.setup){this.setup();}this.event("afterSetup");}if(this.state=="running"){if(this.options.transition){pos=this.options.transition(pos);}pos*=(this.options.to-this.options.from);pos+=this.options.from;this.position=pos;this.event("beforeUpdate");if(this.update){this.update(pos);}this.event("afterUpdate");}},cancel:function(){if(!this.options.sync){Effect.Queues.get(typeof this.options.queue=="string"?"global":this.options.queue.scope).remove(this);}this.state="finished";},event:function(_750){if(this.options[_750+"Internal"]){this.options[_750+"Internal"](this);}if(this.options[_750]){this.options[_750](this);}},inspect:function(){var data=$H();for(property in this){if(typeof this[property]!="function"){data[property]=this[property];}}return "#<Effect:"+data.inspect()+",options:"+$H(this.options).inspect()+">";}};Effect.Parallel=Class.create();Object.extend(Object.extend(Effect.Parallel.prototype,Effect.Base.prototype),{initialize:function(_752){this.effects=_752||[];this.start(arguments[1]);},update:function(_753){this.effects.invoke("render",_753);},finish:function(_754){this.effects.each(function(_755){_755.render(1);_755.cancel();_755.event("beforeFinish");if(_755.finish){_755.finish(_754);}_755.event("afterFinish");});}});Effect.Event=Class.create();Object.extend(Object.extend(Effect.Event.prototype,Effect.Base.prototype),{initialize:function(){var _756=Object.extend({duration:0},arguments[0]||{});this.start(_756);},update:Prototype.emptyFunction});Effect.Opacity=Class.create();Object.extend(Object.extend(Effect.Opacity.prototype,Effect.Base.prototype),{initialize:function(_757){this.element=$(_757);if(!this.element){throw (Effect._elementDoesNotExistError);}if(/MSIE/.test(navigator.userAgent)&&!window.opera&&(!this.element.currentStyle.hasLayout)){this.element.setStyle({zoom:1});}var _758=Object.extend({from:this.element.getOpacity()||0,to:1},arguments[1]||{});this.start(_758);},update:function(_759){this.element.setOpacity(_759);}});Effect.Move=Class.create();Object.extend(Object.extend(Effect.Move.prototype,Effect.Base.prototype),{initialize:function(_75a){this.element=$(_75a);if(!this.element){throw (Effect._elementDoesNotExistError);}var _75b=Object.extend({x:0,y:0,mode:"relative"},arguments[1]||{});this.start(_75b);},setup:function(){this.element.makePositioned();this.originalLeft=parseFloat(this.element.getStyle("left")||"0");this.originalTop=parseFloat(this.element.getStyle("top")||"0");if(this.options.mode=="absolute"){this.options.x=this.options.x-this.originalLeft;this.options.y=this.options.y-this.originalTop;}},update:function(_75c){this.element.setStyle({left:Math.round(this.options.x*_75c+this.originalLeft)+"px",top:Math.round(this.options.y*_75c+this.originalTop)+"px"});}});Effect.MoveBy=function(_75d,_75e,_75f){return new Effect.Move(_75d,Object.extend({x:_75f,y:_75e},arguments[3]||{}));};Effect.Scale=Class.create();Object.extend(Object.extend(Effect.Scale.prototype,Effect.Base.prototype),{initialize:function(_760,_761){this.element=$(_760);if(!this.element){throw (Effect._elementDoesNotExistError);}var _762=Object.extend({scaleX:true,scaleY:true,scaleContent:true,scaleFromCenter:false,scaleMode:"box",scaleFrom:100,scaleTo:_761},arguments[2]||{});this.start(_762);},setup:function(){this.restoreAfterFinish=this.options.restoreAfterFinish||false;this.elementPositioning=this.element.getStyle("position");this.originalStyle={};["top","left","width","height","fontSize"].each(function(k){this.originalStyle[k]=this.element.style[k];}.bind(this));this.originalTop=this.element.offsetTop;this.originalLeft=this.element.offsetLeft;var _764=this.element.getStyle("font-size")||"100%";["em","px","%","pt"].each(function(_765){if(_764.indexOf(_765)>0){this.fontSize=parseFloat(_764);this.fontSizeType=_765;}}.bind(this));this.factor=(this.options.scaleTo-this.options.scaleFrom)/100;this.dims=null;if(this.options.scaleMode=="box"){this.dims=[this.element.offsetHeight,this.element.offsetWidth];}if(/^content/.test(this.options.scaleMode)){this.dims=[this.element.scrollHeight,this.element.scrollWidth];}if(!this.dims){this.dims=[this.options.scaleMode.originalHeight,this.options.scaleMode.originalWidth];}},update:function(_766){var _767=(this.options.scaleFrom/100)+(this.factor*_766);if(this.options.scaleContent&&this.fontSize){this.element.setStyle({fontSize:this.fontSize*_767+this.fontSizeType});}this.setDimensions(this.dims[0]*_767,this.dims[1]*_767);},finish:function(_768){if(this.restoreAfterFinish){this.element.setStyle(this.originalStyle);}},setDimensions:function(_769,_76a){var d={};if(this.options.scaleX){d.width=Math.round(_76a)+"px";}if(this.options.scaleY){d.height=Math.round(_769)+"px";}if(this.options.scaleFromCenter){var topd=(_769-this.dims[0])/2;var _76d=(_76a-this.dims[1])/2;if(this.elementPositioning=="absolute"){if(this.options.scaleY){d.top=this.originalTop-topd+"px";}if(this.options.scaleX){d.left=this.originalLeft-_76d+"px";}}else{if(this.options.scaleY){d.top=-topd+"px";}if(this.options.scaleX){d.left=-_76d+"px";}}}this.element.setStyle(d);}});Effect.Highlight=Class.create();Object.extend(Object.extend(Effect.Highlight.prototype,Effect.Base.prototype),{initialize:function(_76e){this.element=$(_76e);if(!this.element){throw (Effect._elementDoesNotExistError);}var _76f=Object.extend({startcolor:"#ffff99"},arguments[1]||{});this.start(_76f);},setup:function(){if(this.element.getStyle("display")=="none"){this.cancel();return;}this.oldStyle={};if(!this.options.keepBackgroundImage){this.oldStyle.backgroundImage=this.element.getStyle("background-image");this.element.setStyle({backgroundImage:"none"});}if(!this.options.endcolor){this.options.endcolor=this.element.getStyle("background-color").parseColor("#ffffff");}if(!this.options.restorecolor){this.options.restorecolor=this.element.getStyle("background-color");}this._base=$R(0,2).map(function(i){return parseInt(this.options.startcolor.slice(i*2+1,i*2+3),16);}.bind(this));this._delta=$R(0,2).map(function(i){return parseInt(this.options.endcolor.slice(i*2+1,i*2+3),16)-this._base[i];}.bind(this));},update:function(_772){this.element.setStyle({backgroundColor:$R(0,2).inject("#",function(m,v,i){return m+(Math.round(this._base[i]+(this._delta[i]*_772)).toColorPart());}.bind(this))});},finish:function(){this.element.setStyle(Object.extend(this.oldStyle,{backgroundColor:this.options.restorecolor}));}});Effect.ScrollTo=Class.create();Object.extend(Object.extend(Effect.ScrollTo.prototype,Effect.Base.prototype),{initialize:function(_776){this.element=$(_776);this.start(arguments[1]||{});},setup:function(){Position.prepare();var _777=Position.cumulativeOffset(this.element);if(this.options.offset){_777[1]+=this.options.offset;}var max=window.innerHeight?window.height-window.innerHeight:document.body.scrollHeight-(document.documentElement.clientHeight?document.documentElement.clientHeight:document.body.clientHeight);this.scrollStart=Position.deltaY;this.delta=(_777[1]>max?max:_777[1])-this.scrollStart;},update:function(_779){Position.prepare();window.scrollTo(Position.deltaX,this.scrollStart+(_779*this.delta));}});Effect.Fade=function(_77a){_77a=$(_77a);var _77b=_77a.getInlineOpacity();var _77c=Object.extend({from:_77a.getOpacity()||1,to:0,afterFinishInternal:function(_77d){if(_77d.options.to!=0){return;}_77d.element.hide().setStyle({opacity:_77b});}},arguments[1]||{});return new Effect.Opacity(_77a,_77c);};Effect.Appear=function(_77e){_77e=$(_77e);var _77f=Object.extend({from:(_77e.getStyle("display")=="none"?0:_77e.getOpacity()||0),to:1,afterFinishInternal:function(_780){_780.element.forceRerendering();},beforeSetup:function(_781){_781.element.setOpacity(_781.options.from).show();}},arguments[1]||{});return new Effect.Opacity(_77e,_77f);};Effect.Puff=function(_782){_782=$(_782);var _783={opacity:_782.getInlineOpacity(),position:_782.getStyle("position"),top:_782.style.top,left:_782.style.left,width:_782.style.width,height:_782.style.height};return new Effect.Parallel([new Effect.Scale(_782,200,{sync:true,scaleFromCenter:true,scaleContent:true,restoreAfterFinish:true}),new Effect.Opacity(_782,{sync:true,to:0})],Object.extend({duration:1,beforeSetupInternal:function(_784){Position.absolutize(_784.effects[0].element);},afterFinishInternal:function(_785){_785.effects[0].element.hide().setStyle(_783);}},arguments[1]||{}));};Effect.BlindUp=function(_786){_786=$(_786);_786.makeClipping();return new Effect.Scale(_786,0,Object.extend({scaleContent:false,scaleX:false,restoreAfterFinish:true,afterFinishInternal:function(_787){_787.element.hide().undoClipping();}},arguments[1]||{}));};Effect.BlindDown=function(_788){_788=$(_788);var _789=_788.getDimensions();return new Effect.Scale(_788,100,Object.extend({scaleContent:false,scaleX:false,scaleFrom:0,scaleMode:{originalHeight:_789.height,originalWidth:_789.width},restoreAfterFinish:true,afterSetup:function(_78a){_78a.element.makeClipping().setStyle({height:"0px"}).show();},afterFinishInternal:function(_78b){_78b.element.undoClipping();}},arguments[1]||{}));};Effect.SwitchOff=function(_78c){_78c=$(_78c);var _78d=_78c.getInlineOpacity();return new Effect.Appear(_78c,Object.extend({duration:0.4,from:0,transition:Effect.Transitions.flicker,afterFinishInternal:function(_78e){new Effect.Scale(_78e.element,1,{duration:0.3,scaleFromCenter:true,scaleX:false,scaleContent:false,restoreAfterFinish:true,beforeSetup:function(_78f){_78f.element.makePositioned().makeClipping();},afterFinishInternal:function(_790){_790.element.hide().undoClipping().undoPositioned().setStyle({opacity:_78d});}});}},arguments[1]||{}));};Effect.DropOut=function(_791){_791=$(_791);var _792={top:_791.getStyle("top"),left:_791.getStyle("left"),opacity:_791.getInlineOpacity()};return new Effect.Parallel([new Effect.Move(_791,{x:0,y:100,sync:true}),new Effect.Opacity(_791,{sync:true,to:0})],Object.extend({duration:0.5,beforeSetup:function(_793){_793.effects[0].element.makePositioned();},afterFinishInternal:function(_794){_794.effects[0].element.hide().undoPositioned().setStyle(_792);}},arguments[1]||{}));};Effect.Shake=function(_795){_795=$(_795);var _796={top:_795.getStyle("top"),left:_795.getStyle("left")};return new Effect.Move(_795,{x:20,y:0,duration:0.05,afterFinishInternal:function(_797){new Effect.Move(_797.element,{x:-40,y:0,duration:0.1,afterFinishInternal:function(_798){new Effect.Move(_798.element,{x:40,y:0,duration:0.1,afterFinishInternal:function(_799){new Effect.Move(_799.element,{x:-40,y:0,duration:0.1,afterFinishInternal:function(_79a){new Effect.Move(_79a.element,{x:40,y:0,duration:0.1,afterFinishInternal:function(_79b){new Effect.Move(_79b.element,{x:-20,y:0,duration:0.05,afterFinishInternal:function(_79c){_79c.element.undoPositioned().setStyle(_796);}});}});}});}});}});}});};Effect.SlideDown=function(_79d){_79d=$(_79d).cleanWhitespace();var _79e=_79d.down().getStyle("bottom");var _79f=_79d.getDimensions();return new Effect.Scale(_79d,100,Object.extend({scaleContent:false,scaleX:false,scaleFrom:window.opera?0:1,scaleMode:{originalHeight:_79f.height,originalWidth:_79f.width},restoreAfterFinish:true,afterSetup:function(_7a0){_7a0.element.makePositioned();_7a0.element.down().makePositioned();if(window.opera){_7a0.element.setStyle({top:""});}_7a0.element.makeClipping().setStyle({height:"0px"}).show();},afterUpdateInternal:function(_7a1){_7a1.element.down().setStyle({bottom:(_7a1.dims[0]-_7a1.element.clientHeight)+"px"});},afterFinishInternal:function(_7a2){_7a2.element.undoClipping().undoPositioned();_7a2.element.down().undoPositioned().setStyle({bottom:_79e});}},arguments[1]||{}));};Effect.SlideUp=function(_7a3){_7a3=$(_7a3).cleanWhitespace();var _7a4=_7a3.down().getStyle("bottom");return new Effect.Scale(_7a3,window.opera?0:1,Object.extend({scaleContent:false,scaleX:false,scaleMode:"box",scaleFrom:100,restoreAfterFinish:true,beforeStartInternal:function(_7a5){_7a5.element.makePositioned();_7a5.element.down().makePositioned();if(window.opera){_7a5.element.setStyle({top:""});}_7a5.element.makeClipping().show();},afterUpdateInternal:function(_7a6){_7a6.element.down().setStyle({bottom:(_7a6.dims[0]-_7a6.element.clientHeight)+"px"});},afterFinishInternal:function(_7a7){_7a7.element.hide().undoClipping().undoPositioned().setStyle({bottom:_7a4});_7a7.element.down().undoPositioned();}},arguments[1]||{}));};Effect.Squish=function(_7a8){return new Effect.Scale(_7a8,window.opera?1:0,{restoreAfterFinish:true,beforeSetup:function(_7a9){_7a9.element.makeClipping();},afterFinishInternal:function(_7aa){_7aa.element.hide().undoClipping();}});};Effect.Grow=function(_7ab){_7ab=$(_7ab);var _7ac=Object.extend({direction:"center",moveTransition:Effect.Transitions.sinoidal,scaleTransition:Effect.Transitions.sinoidal,opacityTransition:Effect.Transitions.full},arguments[1]||{});var _7ad={top:_7ab.style.top,left:_7ab.style.left,height:_7ab.style.height,width:_7ab.style.width,opacity:_7ab.getInlineOpacity()};var dims=_7ab.getDimensions();var _7af,initialMoveY;var _7b0,moveY;switch(_7ac.direction){case "top-left":_7af=initialMoveY=_7b0=moveY=0;break;case "top-right":_7af=dims.width;initialMoveY=moveY=0;_7b0=-dims.width;break;case "bottom-left":_7af=_7b0=0;initialMoveY=dims.height;moveY=-dims.height;break;case "bottom-right":_7af=dims.width;initialMoveY=dims.height;_7b0=-dims.width;moveY=-dims.height;break;case "center":_7af=dims.width/2;initialMoveY=dims.height/2;_7b0=-dims.width/2;moveY=-dims.height/2;break;}return new Effect.Move(_7ab,{x:_7af,y:initialMoveY,duration:0.01,beforeSetup:function(_7b1){_7b1.element.hide().makeClipping().makePositioned();},afterFinishInternal:function(_7b2){new Effect.Parallel([new Effect.Opacity(_7b2.element,{sync:true,to:1,from:0,transition:_7ac.opacityTransition}),new Effect.Move(_7b2.element,{x:_7b0,y:moveY,sync:true,transition:_7ac.moveTransition}),new Effect.Scale(_7b2.element,100,{scaleMode:{originalHeight:dims.height,originalWidth:dims.width},sync:true,scaleFrom:window.opera?1:0,transition:_7ac.scaleTransition,restoreAfterFinish:true})],Object.extend({beforeSetup:function(_7b3){_7b3.effects[0].element.setStyle({height:"0px"}).show();},afterFinishInternal:function(_7b4){_7b4.effects[0].element.undoClipping().undoPositioned().setStyle(_7ad);}},_7ac));}});};Effect.Shrink=function(_7b5){_7b5=$(_7b5);var _7b6=Object.extend({direction:"center",moveTransition:Effect.Transitions.sinoidal,scaleTransition:Effect.Transitions.sinoidal,opacityTransition:Effect.Transitions.none},arguments[1]||{});var _7b7={top:_7b5.style.top,left:_7b5.style.left,height:_7b5.style.height,width:_7b5.style.width,opacity:_7b5.getInlineOpacity()};var dims=_7b5.getDimensions();var _7b9,moveY;switch(_7b6.direction){case "top-left":_7b9=moveY=0;break;case "top-right":_7b9=dims.width;moveY=0;break;case "bottom-left":_7b9=0;moveY=dims.height;break;case "bottom-right":_7b9=dims.width;moveY=dims.height;break;case "center":_7b9=dims.width/2;moveY=dims.height/2;break;}return new Effect.Parallel([new Effect.Opacity(_7b5,{sync:true,to:0,from:1,transition:_7b6.opacityTransition}),new Effect.Scale(_7b5,window.opera?1:0,{sync:true,transition:_7b6.scaleTransition,restoreAfterFinish:true}),new Effect.Move(_7b5,{x:_7b9,y:moveY,sync:true,transition:_7b6.moveTransition})],Object.extend({beforeStartInternal:function(_7ba){_7ba.effects[0].element.makePositioned().makeClipping();},afterFinishInternal:function(_7bb){_7bb.effects[0].element.hide().undoClipping().undoPositioned().setStyle(_7b7);}},_7b6));};Effect.Pulsate=function(_7bc){_7bc=$(_7bc);var _7bd=arguments[1]||{};var _7be=_7bc.getInlineOpacity();var _7bf=_7bd.transition||Effect.Transitions.sinoidal;var _7c0=function(pos){return _7bf(1-Effect.Transitions.pulse(pos,_7bd.pulses));};_7c0.bind(_7bf);return new Effect.Opacity(_7bc,Object.extend(Object.extend({duration:2,from:0,afterFinishInternal:function(_7c2){_7c2.element.setStyle({opacity:_7be});}},_7bd),{transition:_7c0}));};Effect.Fold=function(_7c3){_7c3=$(_7c3);var _7c4={top:_7c3.style.top,left:_7c3.style.left,width:_7c3.style.width,height:_7c3.style.height};_7c3.makeClipping();return new Effect.Scale(_7c3,5,Object.extend({scaleContent:false,scaleX:false,afterFinishInternal:function(_7c5){new Effect.Scale(_7c3,1,{scaleContent:false,scaleY:false,afterFinishInternal:function(_7c6){_7c6.element.hide().undoClipping().setStyle(_7c4);}});}},arguments[1]||{}));};Effect.Morph=Class.create();Object.extend(Object.extend(Effect.Morph.prototype,Effect.Base.prototype),{initialize:function(_7c7){this.element=$(_7c7);if(!this.element){throw (Effect._elementDoesNotExistError);}var _7c8=Object.extend({style:{}},arguments[1]||{});if(typeof _7c8.style=="string"){if(_7c8.style.indexOf(":")==-1){var _7c9="",selector="."+_7c8.style;$A(document.styleSheets).reverse().each(function(_7ca){if(_7ca.cssRules){cssRules=_7ca.cssRules;}else{if(_7ca.rules){cssRules=_7ca.rules;}}$A(cssRules).reverse().each(function(rule){if(selector==rule.selectorText){_7c9=rule.style.cssText;throw $break;}});if(_7c9){throw $break;}});this.style=_7c9.parseStyle();_7c8.afterFinishInternal=function(_7cc){_7cc.element.addClassName(_7cc.options.style);_7cc.transforms.each(function(_7cd){if(_7cd.style!="opacity"){_7cc.element.style[_7cd.style.camelize()]="";}});};}else{this.style=_7c8.style.parseStyle();}}else{this.style=$H(_7c8.style);}this.start(_7c8);},setup:function(){function parseColor(_7ce){if(!_7ce||["rgba(0, 0, 0, 0)","transparent"].include(_7ce)){_7ce="#ffffff";}_7ce=_7ce.parseColor();return $R(0,2).map(function(i){return parseInt(_7ce.slice(i*2+1,i*2+3),16);});}this.transforms=this.style.map(function(pair){var _7d1=pair[0].underscore().dasherize(),value=pair[1],unit=null;if(value.parseColor("#zzzzzz")!="#zzzzzz"){value=value.parseColor();unit="color";}else{if(_7d1=="opacity"){value=parseFloat(value);if(/MSIE/.test(navigator.userAgent)&&!window.opera&&(!this.element.currentStyle.hasLayout)){this.element.setStyle({zoom:1});}}else{if(Element.CSS_LENGTH.test(value)){var _7d2=value.match(/^([\+\-]?[0-9\.]+)(.*)$/),value=parseFloat(_7d2[1]),unit=(_7d2.length==3)?_7d2[2]:null;}}}var _7d3=this.element.getStyle(_7d1);return $H({style:_7d1,originalValue:unit=="color"?parseColor(_7d3):parseFloat(_7d3||0),targetValue:unit=="color"?parseColor(value):value,unit:unit});}.bind(this)).reject(function(_7d4){return ((_7d4.originalValue==_7d4.targetValue)||(_7d4.unit!="color"&&(isNaN(_7d4.originalValue)||isNaN(_7d4.targetValue))));});},update:function(_7d5){var _7d6=$H(),value=null;this.transforms.each(function(_7d7){value=_7d7.unit=="color"?$R(0,2).inject("#",function(m,v,i){return m+(Math.round(_7d7.originalValue[i]+(_7d7.targetValue[i]-_7d7.originalValue[i])*_7d5)).toColorPart();}):_7d7.originalValue+Math.round(((_7d7.targetValue-_7d7.originalValue)*_7d5)*1000)/1000+_7d7.unit;_7d6[_7d7.style]=value;});this.element.setStyle(_7d6);}});Effect.Transform=Class.create();Object.extend(Effect.Transform.prototype,{initialize:function(_7db){this.tracks=[];this.options=arguments[1]||{};this.addTracks(_7db);},addTracks:function(_7dc){_7dc.each(function(_7dd){var data=$H(_7dd).values().first();this.tracks.push($H({ids:$H(_7dd).keys().first(),effect:Effect.Morph,options:{style:data}}));}.bind(this));return this;},play:function(){return new Effect.Parallel(this.tracks.map(function(_7df){var _7e0=[$(_7df.ids)||$$(_7df.ids)].flatten();return _7e0.map(function(e){return new _7df.effect(e,Object.extend({sync:true},_7df.options));});}).flatten(),this.options);}});Element.CSS_PROPERTIES=$w("backgroundColor backgroundPosition borderBottomColor borderBottomStyle "+"borderBottomWidth borderLeftColor borderLeftStyle borderLeftWidth "+"borderRightColor borderRightStyle borderRightWidth borderSpacing "+"borderTopColor borderTopStyle borderTopWidth bottom clip color "+"fontSize fontWeight height left letterSpacing lineHeight "+"marginBottom marginLeft marginRight marginTop markerOffset maxHeight "+"maxWidth minHeight minWidth opacity outlineColor outlineOffset "+"outlineWidth paddingBottom paddingLeft paddingRight paddingTop "+"right textIndent top width wordSpacing zIndex");Element.CSS_LENGTH=/^(([\+\-]?[0-9\.]+)(em|ex|px|in|cm|mm|pt|pc|\%))|0$/;String.prototype.parseStyle=function(){var _7e2=Element.extend(document.createElement("div"));_7e2.innerHTML="<div style=\""+this+"\"></div>";var _7e3=_7e2.down().style,styleRules=$H();Element.CSS_PROPERTIES.each(function(_7e4){if(_7e3[_7e4]){styleRules[_7e4]=_7e3[_7e4];}});if(/MSIE/.test(navigator.userAgent)&&!window.opera&&this.indexOf("opacity")>-1){styleRules.opacity=this.match(/opacity:\s*((?:0|1)?(?:\.\d*)?)/)[1];}return styleRules;};Element.morph=function(_7e5,_7e6){new Effect.Morph(_7e5,Object.extend({style:_7e6},arguments[2]||{}));return _7e5;};["setOpacity","getOpacity","getInlineOpacity","forceRerendering","setContentZoom","collectTextNodes","collectTextNodesIgnoreClass","morph"].each(function(f){Element.Methods[f]=Element[f];});Element.Methods.visualEffect=function(_7e8,_7e9,_7ea){s=_7e9.gsub(/_/,"-").camelize();effect_class=s.charAt(0).toUpperCase()+s.substring(1);new Effect[effect_class](_7e8,_7ea);return $(_7e8);};Element.addMethods();