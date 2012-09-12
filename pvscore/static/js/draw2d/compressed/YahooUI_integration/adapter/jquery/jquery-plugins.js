/**
This notice must be untouched at all times.
This is the COMPRESSED version of Draw2D
WebSite: http://www.draw2d.org
Copyright: 2006 Andreas Herz. All rights reserved.
Created: 5.11.2006 by Andreas Herz (Web: http://www.freegroup.de )
LICENSE: LGPL
**/

jQuery.fn._height=jQuery.fn.height;jQuery.fn._width=jQuery.fn.width;jQuery.fn.height=function(){if(this[0]==window){return self.innerHeight||jQuery.boxModel&&document.documentElement.clientHeight||document.body.clientHeight;}if(this[0]==document){return Math.max(document.body.scrollHeight,document.body.offsetHeight);}return this._height(arguments[0]);};jQuery.fn.width=function(){if(this[0]==window){return self.innerWidth||jQuery.boxModel&&document.documentElement.clientWidth||document.body.clientWidth;}if(this[0]==document){return Math.max(document.body.scrollWidth,document.body.offsetWidth);}return this._width(arguments[0]);};jQuery.fn.innerHeight=function(){return this[0]==window||this[0]==document?this.height():this.css("display")!="none"?this[0].offsetHeight-(parseInt(this.css("borderTopWidth"))||0)-(parseInt(this.css("borderBottomWidth"))||0):this.height()+(parseInt(this.css("paddingTop"))||0)+(parseInt(this.css("paddingBottom"))||0);};jQuery.fn.innerWidth=function(){return this[0]==window||this[0]==document?this.width():this.css("display")!="none"?this[0].offsetWidth-(parseInt(this.css("borderLeftWidth"))||0)-(parseInt(this.css("borderRightWidth"))||0):this.height()+(parseInt(this.css("paddingLeft"))||0)+(parseInt(this.css("paddingRight"))||0);};jQuery.fn.outerHeight=function(){return this[0]==window||this[0]==document?this.height():this.css("display")!="none"?this[0].offsetHeight:this.height()+(parseInt(this.css("borderTopWidth"))||0)+(parseInt(this.css("borderBottomWidth"))||0)+(parseInt(this.css("paddingTop"))||0)+(parseInt(this.css("paddingBottom"))||0);};jQuery.fn.outerWidth=function(){return this[0]==window||this[0]==document?this.width():this.css("display")!="none"?this[0].offsetWidth:this.height()+(parseInt(this.css("borderLeftWidth"))||0)+(parseInt(this.css("borderRightWidth"))||0)+(parseInt(this.css("paddingLeft"))||0)+(parseInt(this.css("paddingRight"))||0);};jQuery.fn.scrollLeft=function(){if(this[0]==window||this[0]==document){return self.pageXOffset||jQuery.boxModel&&document.documentElement.scrollLeft||document.body.scrollLeft;}return this[0].scrollLeft;};jQuery.fn.scrollTop=function(){if(this[0]==window||this[0]==document){return self.pageYOffset||jQuery.boxModel&&document.documentElement.scrollTop||document.body.scrollTop;}return this[0].scrollTop;};jQuery.fn.offset=function(_12fc,_12fd){var x=0,y=0,elem=this[0],parent=this[0],sl=0,st=0,_12fc=jQuery.extend({margin:true,border:true,padding:false,scroll:true},_12fc||{});do{x+=parent.offsetLeft||0;y+=parent.offsetTop||0;if(jQuery.browser.mozilla||jQuery.browser.msie){var bt=parseInt(jQuery.css(parent,"borderTopWidth"))||0;var bl=parseInt(jQuery.css(parent,"borderLeftWidth"))||0;x+=bl;y+=bt;if(jQuery.browser.mozilla&&parent!=elem&&jQuery.css(parent,"overflow")!="visible"){x+=bl;y+=bt;}}var op=parent.offsetParent;if(op&&(op.tagName=="BODY"||op.tagName=="HTML")){if(jQuery.browser.safari&&jQuery.css(parent,"position")!="absolute"){x+=parseInt(jQuery.css(op,"marginLeft"))||0;y+=parseInt(jQuery.css(op,"marginTop"))||0;}break;}if(_12fc.scroll){do{sl+=parent.scrollLeft||0;st+=parent.scrollTop||0;parent=parent.parentNode;if(jQuery.browser.mozilla&&parent!=elem&&parent!=op&&parent.style&&jQuery.css(parent,"overflow")!="visible"){y+=parseInt(jQuery.css(parent,"borderTopWidth"))||0;x+=parseInt(jQuery.css(parent,"borderLeftWidth"))||0;}}while(parent!=op);}else{parent=parent.offsetParent;}}while(parent);if(!_12fc.margin){x-=parseInt(jQuery.css(elem,"marginLeft"))||0;y-=parseInt(jQuery.css(elem,"marginTop"))||0;}if(_12fc.border&&(jQuery.browser.safari||jQuery.browser.opera)){x+=parseInt(jQuery.css(elem,"borderLeftWidth"))||0;y+=parseInt(jQuery.css(elem,"borderTopWidth"))||0;}else{if(!_12fc.border&&!(jQuery.browser.safari||jQuery.browser.opera)){x-=parseInt(jQuery.css(elem,"borderLeftWidth"))||0;y-=parseInt(jQuery.css(elem,"borderTopWidth"))||0;}}if(_12fc.padding){x+=parseInt(jQuery.css(elem,"paddingLeft"))||0;y+=parseInt(jQuery.css(elem,"paddingTop"))||0;}if(_12fc.scroll&&jQuery.browser.opera&&jQuery.css(elem,"display")=="inline"){sl-=elem.scrollLeft||0;st-=elem.scrollTop||0;}var _1302=_12fc.scroll?{top:y-st,left:x-sl,scrollTop:st,scrollLeft:sl}:{top:y,left:x};if(_12fd){jQuery.extend(_12fd,_1302);return this;}else{return _1302;}};jQuery.fn.ajaxSubmit=function(_1303){if(typeof _1303=="function"){_1303={success:_1303};}_1303=jQuery.extend({url:this.attr("action")||"",method:this.attr("method")||"GET"},_1303||{});_1303.success=_1303.success||_1303.after;_1303.beforeSubmit=_1303.beforeSubmit||_1303.before;_1303.type=_1303.type||_1303.method;var a=this.formToArray(_1303.semantic);if(_1303.beforeSubmit&&_1303.beforeSubmit(a,this,_1303)===false){return this;}var q=jQuery.param(a);if(_1303.type.toUpperCase()=="GET"){_1303.url+=(_1303.url.indexOf("?")>=0?"&":"?")+q;_1303.data=null;}else{_1303.data=q;}var $form=this,callbacks=[];if(_1303.resetForm){callbacks.push(function(){$form.resetForm();});}if(_1303.clearForm){callbacks.push(function(){$form.clearForm();});}if(!_1303.dataType&&_1303.target){var _1307=_1303.success||function(){};callbacks.push(function(data,_1309){jQuery(_1303.target).attr("innerHTML",data).evalScripts().each(_1307,[data,_1309]);});}else{if(_1303.success){callbacks.push(_1303.success);}}_1303.success=function(data,_130b){for(var i=0,max=callbacks.length;i<max;i++){callbacks[i](data,_130b);}};jQuery.ajax(_1303);return this;};jQuery.fn.ajaxForm=function(_130d){return this.each(function(){jQuery("input:submit,input:image,button:submit",this).click(function(ev){var $form=this.form;$form.clk=this;if(this.type=="image"){if(ev.offsetX!=undefined){$form.clk_x=ev.offsetX;$form.clk_y=ev.offsetY;}else{if(typeof jQuery.fn.offset=="function"){var _1310=jQuery(this).offset();$form.clk_x=ev.pageX-_1310.left;$form.clk_y=ev.pageY-_1310.top;}else{$form.clk_x=ev.pageX-this.offsetLeft;$form.clk_y=ev.pageY-this.offsetTop;}}}setTimeout(function(){$form.clk=$form.clk_x=$form.clk_y=null;},10);});}).submit(function(e){jQuery(this).ajaxSubmit(_130d);return false;});};jQuery.fn.formToArray=function(_1312){var a=[];if(this.length===0){return a;}var form=this[0];var els=_1312?form.getElementsByTagName("*"):form.elements;if(!els){return a;}for(var i=0,max=els.length;i<max;i++){var el=els[i];var n=el.name;if(!n){continue;}if(_1312&&form.clk&&el.type=="image"){if(!el.disabled&&form.clk==el){a.push({name:n+".x",value:form.clk_x},{name:n+".y",value:form.clk_y});}continue;}var v=jQuery.fieldValue(el,true);if(v===null){continue;}if(v.constructor==Array){for(var j=0,jmax=v.length;j<jmax;j++){a.push({name:n,value:v[j]});}}else{a.push({name:n,value:v});}}if(!_1312&&form.clk){var _131b=form.getElementsByTagName("input");for(var i=0,max=_131b.length;i<max;i++){var input=_131b[i];var n=input.name;if(n&&!input.disabled&&input.type=="image"&&form.clk==input){a.push({name:n+".x",value:form.clk_x},{name:n+".y",value:form.clk_y});}}}return a;};jQuery.fn.formSerialize=function(_131d){return jQuery.param(this.formToArray(_131d));};jQuery.fn.fieldSerialize=function(_131e){var a=[];this.each(function(){var n=this.name;if(!n){return;}var v=jQuery.fieldValue(this,_131e);if(v&&v.constructor==Array){for(var i=0,max=v.length;i<max;i++){a.push({name:n,value:v[i]});}}else{if(v!==null&&typeof v!="undefined"){a.push({name:this.name,value:v});}}});return jQuery.param(a);};jQuery.fn.fieldValue=function(_1323){var cbVal,cbName;for(var i=0,max=this.length;i<max;i++){var el=this[i];var v=jQuery.fieldValue(el,_1323);if(v===null||typeof v=="undefined"||(v.constructor==Array&&!v.length)){continue;}if(el.type!="checkbox"){return v;}cbName=cbName||el.name;if(cbName!=el.name){return cbVal;}cbVal=cbVal||[];cbVal.push(v);}return cbVal;};jQuery.fieldValue=function(el,_1329){var n=el.name,t=el.type,tag=el.tagName.toLowerCase();if(typeof _1329=="undefined"){_1329=true;}if(_1329&&(!n||el.disabled||t=="reset"||(t=="checkbox"||t=="radio")&&!el.checked||(t=="submit"||t=="image")&&el.form&&el.form.clk!=el||tag=="select"&&el.selectedIndex==-1)){return null;}if(tag=="select"){var index=el.selectedIndex;if(index<0){return null;}var a=[],ops=el.options;var one=(t=="select-one");var max=(one?index+1:ops.length);for(var i=(one?index:0);i<max;i++){var op=ops[i];if(op.selected){var v=jQuery.browser.msie&&!(op.attributes["value"].specified)?op.text:op.value;if(one){return v;}a.push(v);}}return a;}return el.value;};jQuery.fn.clearForm=function(){return this.each(function(){jQuery("input,select,textarea",this).clearFields();});};jQuery.fn.clearFields=jQuery.fn.clearInputs=function(){return this.each(function(){var t=this.type,tag=this.tagName.toLowerCase();if(t=="text"||t=="password"||tag=="textarea"){this.value="";}else{if(t=="checkbox"||t=="radio"){this.checked=false;}else{if(tag=="select"){this.selectedIndex=-1;}}}});};jQuery.fn.resetForm=function(){return this.each(function(){if(typeof this.reset=="function"||(typeof this.reset=="object"&&!this.reset.nodeType)){this.reset();}});};