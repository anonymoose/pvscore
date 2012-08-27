if(typeof window.jQuery=="undefined"){
window.undefined=window.undefined;
var jQuery=function(a,c){
if(window==this){
return new jQuery(a,c);
}
a=a||document;
if(jQuery.isFunction(a)){
return new jQuery(document)[jQuery.fn.ready?"ready":"load"](a);
}
if(typeof a=="string"){
var m=/^[^<]*(<(.|\n)+>)[^>]*$/.exec(a);
if(m){
a=jQuery.clean([m[1]]);
}else{
return new jQuery(c).find(a);
}
}
return this.setArray(a.constructor==Array&&a||(a.jquery||a.length&&a!=window&&!a.nodeType&&a[0]!=undefined&&a[0].nodeType)&&jQuery.makeArray(a)||[a]);
};
if(typeof $!="undefined"){
jQuery._$=$;
}
var $=jQuery;
jQuery.fn=jQuery.prototype={jquery:"1.1.1",size:function(){
return this.length;
},length:0,get:function(num){
return num==undefined?jQuery.makeArray(this):this[num];
},pushStack:function(a){
var ret=jQuery(this);
ret.prevObject=this;
return ret.setArray(a);
},setArray:function(a){
this.length=0;
[].push.apply(this,a);
return this;
},each:function(fn,args){
return jQuery.each(this,fn,args);
},index:function(obj){
var pos=-1;
this.each(function(i){
if(this==obj){
pos=i;
}
});
return pos;
},attr:function(key,value,type){
var obj=key;
if(key.constructor==String){
if(value==undefined){
return this.length&&jQuery[type||"attr"](this[0],key)||undefined;
}else{
obj={};
obj[key]=value;
}
}
return this.each(function(index){
for(var prop in obj){
jQuery.attr(type?this.style:this,prop,jQuery.prop(this,obj[prop],type,index,prop));
}
});
},css:function(key,value){
return this.attr(key,value,"curCSS");
},text:function(e){
if(typeof e=="string"){
return this.empty().append(document.createTextNode(e));
}
var t="";
jQuery.each(e||this,function(){
jQuery.each(this.childNodes,function(){
if(this.nodeType!=8){
t+=this.nodeType!=1?this.nodeValue:jQuery.fn.text([this]);
}
});
});
return t;
},wrap:function(){
var a=jQuery.clean(arguments);
return this.each(function(){
var b=a[0].cloneNode(true);
this.parentNode.insertBefore(b,this);
while(b.firstChild){
b=b.firstChild;
}
b.appendChild(this);
});
},append:function(){
return this.domManip(arguments,true,1,function(a){
this.appendChild(a);
});
},prepend:function(){
return this.domManip(arguments,true,-1,function(a){
this.insertBefore(a,this.firstChild);
});
},before:function(){
return this.domManip(arguments,false,1,function(a){
this.parentNode.insertBefore(a,this);
});
},after:function(){
return this.domManip(arguments,false,-1,function(a){
this.parentNode.insertBefore(a,this.nextSibling);
});
},end:function(){
return this.prevObject||jQuery([]);
},find:function(t){
return this.pushStack(jQuery.map(this,function(a){
return jQuery.find(t,a);
}));
},clone:function(deep){
return this.pushStack(jQuery.map(this,function(a){
return a.cloneNode(deep!=undefined?deep:true);
}));
},filter:function(t){
return this.pushStack(jQuery.isFunction(t)&&jQuery.grep(this,function(el,index){
return t.apply(el,[index]);
})||jQuery.multiFilter(t,this));
},not:function(t){
return this.pushStack(t.constructor==String&&jQuery.multiFilter(t,this,true)||jQuery.grep(this,function(a){
if(t.constructor==Array||t.jquery){
return jQuery.inArray(t,a)<0;
}else{
return a!=t;
}
}));
},add:function(t){
return this.pushStack(jQuery.merge(this.get(),t.constructor==String?jQuery(t).get():t.length!=undefined&&!t.nodeName?t:[t]));
},is:function(expr){
return expr?jQuery.filter(expr,this).r.length>0:false;
},val:function(val){
return val==undefined?(this.length?this[0].value:null):this.attr("value",val);
},html:function(val){
return val==undefined?(this.length?this[0].innerHTML:null):this.empty().append(val);
},domManip:function(args,table,dir,fn){
var clone=this.length>1;
var a=jQuery.clean(args);
if(dir<0){
a.reverse();
}
return this.each(function(){
var obj=this;
if(table&&jQuery.nodeName(this,"table")&&jQuery.nodeName(a[0],"tr")){
obj=this.getElementsByTagName("tbody")[0]||this.appendChild(document.createElement("tbody"));
}
jQuery.each(a,function(){
fn.apply(obj,[clone?this.cloneNode(true):this]);
});
});
}};
jQuery.extend=jQuery.fn.extend=function(){
var _44c9=arguments[0],a=1;
if(arguments.length==1){
_44c9=this;
a=0;
}
var prop;
while(prop=arguments[a++]){
for(var i in prop){
_44c9[i]=prop[i];
}
}
return _44c9;
};
jQuery.extend({noConflict:function(){
if(jQuery._$){
$=jQuery._$;
}
return jQuery;
},isFunction:function(fn){
return !!fn&&typeof fn!="string"&&typeof fn[0]=="undefined"&&/function/i.test(fn+"");
},nodeName:function(elem,name){
return elem.nodeName&&elem.nodeName.toUpperCase()==name.toUpperCase();
},each:function(obj,fn,args){
if(obj.length==undefined){
for(var i in obj){
fn.apply(obj[i],args||[i,obj[i]]);
}
}else{
for(var i=0,ol=obj.length;i<ol;i++){
if(fn.apply(obj[i],args||[i,obj[i]])===false){
break;
}
}
}
return obj;
},prop:function(elem,value,type,index,prop){
if(jQuery.isFunction(value)){
return value.call(elem,[index]);
}
var _44d8=/z-?index|font-?weight|opacity|zoom|line-?height/i;
if(value.constructor==Number&&type=="curCSS"&&!_44d8.test(prop)){
return value+"px";
}
return value;
},className:{add:function(elem,c){
jQuery.each(c.split(/\s+/),function(i,cur){
if(!jQuery.className.has(elem.className,cur)){
elem.className+=(elem.className?" ":"")+cur;
}
});
},remove:function(elem,c){
elem.className=c?jQuery.grep(elem.className.split(/\s+/),function(cur){
return !jQuery.className.has(c,cur);
}).join(" "):"";
},has:function(t,c){
t=t.className||t;
return t&&new RegExp("(^|\\s)"+c+"(\\s|$)").test(t);
}},swap:function(e,o,f){
for(var i in o){
e.style["old"+i]=e.style[i];
e.style[i]=o[i];
}
f.apply(e,[]);
for(var i in o){
e.style[i]=e.style["old"+i];
}
},css:function(e,p){
if(p=="height"||p=="width"){
var old={},oHeight,oWidth,d=["Top","Bottom","Right","Left"];
jQuery.each(d,function(){
old["padding"+this]=0;
old["border"+this+"Width"]=0;
});
jQuery.swap(e,old,function(){
if(jQuery.css(e,"display")!="none"){
oHeight=e.offsetHeight;
oWidth=e.offsetWidth;
}else{
e=jQuery(e.cloneNode(true)).find(":radio").removeAttr("checked").end().css({visibility:"hidden",position:"absolute",display:"block",right:"0",left:"0"}).appendTo(e.parentNode)[0];
var _44e9=jQuery.css(e.parentNode,"position");
if(_44e9==""||_44e9=="static"){
e.parentNode.style.position="relative";
}
oHeight=e.clientHeight;
oWidth=e.clientWidth;
if(_44e9==""||_44e9=="static"){
e.parentNode.style.position="static";
}
e.parentNode.removeChild(e);
}
});
return p=="height"?oHeight:oWidth;
}
return jQuery.curCSS(e,p);
},curCSS:function(elem,prop,force){
var ret;
if(prop=="opacity"&&jQuery.browser.msie){
return jQuery.attr(elem.style,"opacity");
}
if(prop=="float"||prop=="cssFloat"){
prop=jQuery.browser.msie?"styleFloat":"cssFloat";
}
if(!force&&elem.style[prop]){
ret=elem.style[prop];
}else{
if(document.defaultView&&document.defaultView.getComputedStyle){
if(prop=="cssFloat"||prop=="styleFloat"){
prop="float";
}
prop=prop.replace(/([A-Z])/g,"-$1").toLowerCase();
var cur=document.defaultView.getComputedStyle(elem,null);
if(cur){
ret=cur.getPropertyValue(prop);
}else{
if(prop=="display"){
ret="none";
}else{
jQuery.swap(elem,{display:"block"},function(){
var c=document.defaultView.getComputedStyle(this,"");
ret=c&&c.getPropertyValue(prop)||"";
});
}
}
}else{
if(elem.currentStyle){
var _44f0=prop.replace(/\-(\w)/g,function(m,c){
return c.toUpperCase();
});
ret=elem.currentStyle[prop]||elem.currentStyle[_44f0];
}
}
}
return ret;
},clean:function(a){
var r=[];
jQuery.each(a,function(i,arg){
if(!arg){
return;
}
if(arg.constructor==Number){
arg=arg.toString();
}
if(typeof arg=="string"){
var s=jQuery.trim(arg),div=document.createElement("div"),tb=[];
var wrap=!s.indexOf("<opt")&&[1,"<select>","</select>"]||(!s.indexOf("<thead")||!s.indexOf("<tbody")||!s.indexOf("<tfoot"))&&[1,"<table>","</table>"]||!s.indexOf("<tr")&&[2,"<table><tbody>","</tbody></table>"]||(!s.indexOf("<td")||!s.indexOf("<th"))&&[3,"<table><tbody><tr>","</tr></tbody></table>"]||[0,"",""];
div.innerHTML=wrap[1]+s+wrap[2];
while(wrap[0]--){
div=div.firstChild;
}
if(jQuery.browser.msie){
if(!s.indexOf("<table")&&s.indexOf("<tbody")<0){
tb=div.firstChild&&div.firstChild.childNodes;
}else{
if(wrap[1]=="<table>"&&s.indexOf("<tbody")<0){
tb=div.childNodes;
}
}
for(var n=tb.length-1;n>=0;--n){
if(jQuery.nodeName(tb[n],"tbody")&&!tb[n].childNodes.length){
tb[n].parentNode.removeChild(tb[n]);
}
}
}
arg=div.childNodes;
}
if(arg.length===0){
return;
}
if(arg[0]==undefined){
r.push(arg);
}else{
r=jQuery.merge(r,arg);
}
});
return r;
},attr:function(elem,name,value){
var fix={"for":"htmlFor","class":"className","float":jQuery.browser.msie?"styleFloat":"cssFloat",cssFloat:jQuery.browser.msie?"styleFloat":"cssFloat",innerHTML:"innerHTML",className:"className",value:"value",disabled:"disabled",checked:"checked",readonly:"readOnly",selected:"selected"};
if(name=="opacity"&&jQuery.browser.msie&&value!=undefined){
elem.zoom=1;
return elem.filter=elem.filter.replace(/alpha\([^\)]*\)/gi,"")+(value==1?"":"alpha(opacity="+value*100+")");
}else{
if(name=="opacity"&&jQuery.browser.msie){
return elem.filter?parseFloat(elem.filter.match(/alpha\(opacity=(.*)\)/)[1])/100:1;
}
}
if(name=="opacity"&&jQuery.browser.mozilla&&value==1){
value=0.9999;
}
if(fix[name]){
if(value!=undefined){
elem[fix[name]]=value;
}
return elem[fix[name]];
}else{
if(value==undefined&&jQuery.browser.msie&&jQuery.nodeName(elem,"form")&&(name=="action"||name=="method")){
return elem.getAttributeNode(name).nodeValue;
}else{
if(elem.tagName){
if(value!=undefined){
elem.setAttribute(name,value);
}
return elem.getAttribute(name);
}else{
name=name.replace(/-([a-z])/ig,function(z,b){
return b.toUpperCase();
});
if(value!=undefined){
elem[name]=value;
}
return elem[name];
}
}
}
},trim:function(t){
return t.replace(/^\s+|\s+$/g,"");
},makeArray:function(a){
var r=[];
if(a.constructor!=Array){
for(var i=0,al=a.length;i<al;i++){
r.push(a[i]);
}
}else{
r=a.slice(0);
}
return r;
},inArray:function(b,a){
for(var i=0,al=a.length;i<al;i++){
if(a[i]==b){
return i;
}
}
return -1;
},merge:function(first,_4508){
var r=[].slice.call(first,0);
for(var i=0,sl=_4508.length;i<sl;i++){
if(jQuery.inArray(_4508[i],r)==-1){
first.push(_4508[i]);
}
}
return first;
},grep:function(elems,fn,inv){
if(typeof fn=="string"){
fn=new Function("a","i","return "+fn);
}
var _450e=[];
for(var i=0,el=elems.length;i<el;i++){
if(!inv&&fn(elems[i],i)||inv&&!fn(elems[i],i)){
_450e.push(elems[i]);
}
}
return _450e;
},map:function(elems,fn){
if(typeof fn=="string"){
fn=new Function("a","return "+fn);
}
var _4512=[],r=[];
for(var i=0,el=elems.length;i<el;i++){
var val=fn(elems[i],i);
if(val!==null&&val!=undefined){
if(val.constructor!=Array){
val=[val];
}
_4512=_4512.concat(val);
}
}
var r=_4512.length?[_4512[0]]:[];
check:
for(var i=1,rl=_4512.length;i<rl;i++){
for(var j=0;j<i;j++){
if(_4512[i]==r[j]){
continue check;
}
}
r.push(_4512[i]);
}
return r;
}});
new function(){
var b=navigator.userAgent.toLowerCase();
jQuery.browser={safari:/webkit/.test(b),opera:/opera/.test(b),msie:/msie/.test(b)&&!/opera/.test(b),mozilla:/mozilla/.test(b)&&!/(compatible|webkit)/.test(b)};
jQuery.boxModel=!jQuery.browser.msie||document.compatMode=="CSS1Compat";
};
jQuery.each({parent:"a.parentNode",parents:"jQuery.parents(a)",next:"jQuery.nth(a,2,'nextSibling')",prev:"jQuery.nth(a,2,'previousSibling')",siblings:"jQuery.sibling(a.parentNode.firstChild,a)",children:"jQuery.sibling(a.firstChild)"},function(i,n){
jQuery.fn[i]=function(a){
var ret=jQuery.map(this,n);
if(a&&typeof a=="string"){
ret=jQuery.multiFilter(a,ret);
}
return this.pushStack(ret);
};
});
jQuery.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after"},function(i,n){
jQuery.fn[i]=function(){
var a=arguments;
return this.each(function(){
for(var j=0,al=a.length;j<al;j++){
jQuery(a[j])[n](this);
}
});
};
});
jQuery.each({removeAttr:function(key){
jQuery.attr(this,key,"");
this.removeAttribute(key);
},addClass:function(c){
jQuery.className.add(this,c);
},removeClass:function(c){
jQuery.className.remove(this,c);
},toggleClass:function(c){
jQuery.className[jQuery.className.has(this,c)?"remove":"add"](this,c);
},remove:function(a){
if(!a||jQuery.filter(a,[this]).r.length){
this.parentNode.removeChild(this);
}
},empty:function(){
while(this.firstChild){
this.removeChild(this.firstChild);
}
}},function(i,n){
jQuery.fn[i]=function(){
return this.each(n,arguments);
};
});
jQuery.each(["eq","lt","gt","contains"],function(i,n){
jQuery.fn[n]=function(num,fn){
return this.filter(":"+n+"("+num+")",fn);
};
});
jQuery.each(["height","width"],function(i,n){
jQuery.fn[n]=function(h){
return h==undefined?(this.length?jQuery.css(this[0],n):null):this.css(n,h.constructor==String?h:h+"px");
};
});
jQuery.extend({expr:{"":"m[2]=='*'||jQuery.nodeName(a,m[2])","#":"a.getAttribute('id')==m[2]",":":{lt:"i<m[3]-0",gt:"i>m[3]-0",nth:"m[3]-0==i",eq:"m[3]-0==i",first:"i==0",last:"i==r.length-1",even:"i%2==0",odd:"i%2","nth-child":"jQuery.nth(a.parentNode.firstChild,m[3],'nextSibling',a)==a","first-child":"jQuery.nth(a.parentNode.firstChild,1,'nextSibling')==a","last-child":"jQuery.nth(a.parentNode.lastChild,1,'previousSibling')==a","only-child":"jQuery.sibling(a.parentNode.firstChild).length==1",parent:"a.firstChild",empty:"!a.firstChild",contains:"jQuery.fn.text.apply([a]).indexOf(m[3])>=0",visible:"a.type!=\"hidden\"&&jQuery.css(a,\"display\")!=\"none\"&&jQuery.css(a,\"visibility\")!=\"hidden\"",hidden:"a.type==\"hidden\"||jQuery.css(a,\"display\")==\"none\"||jQuery.css(a,\"visibility\")==\"hidden\"",enabled:"!a.disabled",disabled:"a.disabled",checked:"a.checked",selected:"a.selected||jQuery.attr(a,'selected')",text:"a.type=='text'",radio:"a.type=='radio'",checkbox:"a.type=='checkbox'",file:"a.type=='file'",password:"a.type=='password'",submit:"a.type=='submit'",image:"a.type=='image'",reset:"a.type=='reset'",button:"a.type==\"button\"||jQuery.nodeName(a,\"button\")",input:"/input|select|textarea|button/i.test(a.nodeName)"},".":"jQuery.className.has(a,m[2])","@":{"=":"z==m[4]","!=":"z!=m[4]","^=":"z&&!z.indexOf(m[4])","$=":"z&&z.substr(z.length - m[4].length,m[4].length)==m[4]","*=":"z&&z.indexOf(m[4])>=0","":"z",_resort:function(m){
return ["",m[1],m[3],m[2],m[5]];
},_prefix:"z=a[m[3]]||jQuery.attr(a,m[3]);"},"[":"jQuery.find(m[2],a).length"},parse:[/^\[ *(@)([a-z0-9_-]*) *([!*$^=]*) *('?"?)(.*?)\4 *\]/i,/^(\[)\s*(.*?(\[.*?\])?[^[]*?)\s*\]/,/^(:)([a-z0-9_-]*)\("?'?(.*?(\(.*?\))?[^(]*?)"?'?\)/i,/^([:.#]*)([a-z0-9_*-]*)/i],token:[/^(\/?\.\.)/,"a.parentNode",/^(>|\/)/,"jQuery.sibling(a.firstChild)",/^(\+)/,"jQuery.nth(a,2,'nextSibling')",/^(~)/,function(a){
var s=jQuery.sibling(a.parentNode.firstChild);
return s.slice(0,jQuery.inArray(a,s));
}],multiFilter:function(expr,elems,not){
var old,cur=[];
while(expr&&expr!=old){
old=expr;
var f=jQuery.filter(expr,elems,not);
expr=f.t.replace(/^\s*,\s*/,"");
cur=not?elems=f.r:jQuery.merge(cur,f.r);
}
return cur;
},find:function(t,_4537){
if(typeof t!="string"){
return [t];
}
if(_4537&&!_4537.nodeType){
_4537=null;
}
_4537=_4537||document;
if(!t.indexOf("//")){
_4537=_4537.documentElement;
t=t.substr(2,t.length);
}else{
if(!t.indexOf("/")){
_4537=_4537.documentElement;
t=t.substr(1,t.length);
if(t.indexOf("/")>=1){
t=t.substr(t.indexOf("/"),t.length);
}
}
}
var ret=[_4537],done=[],last=null;
while(t&&last!=t){
var r=[];
last=t;
t=jQuery.trim(t).replace(/^\/\//i,"");
var _453a=false;
var re=/^[\/>]\s*([a-z0-9*-]+)/i;
var m=re.exec(t);
if(m){
jQuery.each(ret,function(){
for(var c=this.firstChild;c;c=c.nextSibling){
if(c.nodeType==1&&(jQuery.nodeName(c,m[1])||m[1]=="*")){
r.push(c);
}
}
});
ret=r;
t=t.replace(re,"");
if(t.indexOf(" ")===0){
continue;
}
_453a=true;
}else{
for(var i=0;i<jQuery.token.length;i+=2){
var re=jQuery.token[i];
var m=re.exec(t);
if(m){
r=ret=jQuery.map(ret,jQuery.isFunction(jQuery.token[i+1])?jQuery.token[i+1]:function(a){
return eval(jQuery.token[i+1]);
});
t=jQuery.trim(t.replace(re,""));
_453a=true;
break;
}
}
}
if(t&&!_453a){
if(!t.indexOf(",")){
if(ret[0]==_4537){
ret.shift();
}
jQuery.merge(done,ret);
r=ret=[_4537];
t=" "+t.substr(1,t.length);
}else{
var re2=/^([a-z0-9_-]+)(#)([a-z0-9\\*_-]*)/i;
var m=re2.exec(t);
if(m){
m=[0,m[2],m[3],m[1]];
}else{
re2=/^([#.]?)([a-z0-9\\*_-]*)/i;
m=re2.exec(t);
}
if(m[1]=="#"&&ret[ret.length-1].getElementById){
var oid=ret[ret.length-1].getElementById(m[2]);
ret=r=oid&&(!m[3]||jQuery.nodeName(oid,m[3]))?[oid]:[];
}else{
if(m[1]=="."){
var rec=new RegExp("(^|\\s)"+m[2]+"(\\s|$)");
}
jQuery.each(ret,function(){
var tag=m[1]!=""||m[0]==""?"*":m[2];
if(jQuery.nodeName(this,"object")&&tag=="*"){
tag="param";
}
jQuery.merge(r,m[1]!=""&&ret.length!=1?jQuery.getAll(this,[],m[1],m[2],rec):this.getElementsByTagName(tag));
});
if(m[1]=="."&&ret.length==1){
r=jQuery.grep(r,function(e){
return rec.test(e.className);
});
}
if(m[1]=="#"&&ret.length==1){
var tmp=r;
r=[];
jQuery.each(tmp,function(){
if(this.getAttribute("id")==m[2]){
r=[this];
return false;
}
});
}
ret=r;
}
t=t.replace(re2,"");
}
}
if(t){
var val=jQuery.filter(t,r);
ret=r=val.r;
t=jQuery.trim(val.t);
}
}
if(ret&&ret[0]==_4537){
ret.shift();
}
jQuery.merge(done,ret);
return done;
},filter:function(t,r,not){
while(t&&/^[a-z[({<*:.#]/i.test(t)){
var p=jQuery.parse,m;
jQuery.each(p,function(i,re){
m=re.exec(t);
if(m){
t=t.substring(m[0].length);
if(jQuery.expr[m[1]]._resort){
m=jQuery.expr[m[1]]._resort(m);
}
return false;
}
});
if(m[1]==":"&&m[2]=="not"){
r=jQuery.filter(m[3],r,true).r;
}else{
if(m[1]=="."){
var re=new RegExp("(^|\\s)"+m[2]+"(\\s|$)");
r=jQuery.grep(r,function(e){
return re.test(e.className||"");
},not);
}else{
var f=jQuery.expr[m[1]];
if(typeof f!="string"){
f=jQuery.expr[m[1]][m[2]];
}
eval("f = function(a,i){"+(jQuery.expr[m[1]]._prefix||"")+"return "+f+"}");
r=jQuery.grep(r,f,not);
}
}
}
return {r:r,t:t};
},getAll:function(o,r,token,name,re){
for(var s=o.firstChild;s;s=s.nextSibling){
if(s.nodeType==1){
var add=true;
if(token=="."){
add=s.className&&re.test(s.className);
}else{
if(token=="#"){
add=s.getAttribute("id")==name;
}
}
if(add){
r.push(s);
}
if(token=="#"&&r.length){
break;
}
if(s.firstChild){
jQuery.getAll(s,r,token,name,re);
}
}
}
return r;
},parents:function(elem){
var _4558=[];
var cur=elem.parentNode;
while(cur&&cur!=document){
_4558.push(cur);
cur=cur.parentNode;
}
return _4558;
},nth:function(cur,_455b,dir,elem){
_455b=_455b||1;
var num=0;
for(;cur;cur=cur[dir]){
if(cur.nodeType==1){
num++;
}
if(num==_455b||_455b=="even"&&num%2===0&&num>1&&cur==elem||_455b=="odd"&&num%2==1&&cur==elem){
return cur;
}
}
},sibling:function(n,elem){
var r=[];
for(;n;n=n.nextSibling){
if(n.nodeType==1&&(!elem||n!=elem)){
r.push(n);
}
}
return r;
}});
jQuery.event={add:function(_4562,type,_4564,data){
if(jQuery.browser.msie&&_4562.setInterval!=undefined){
_4562=window;
}
if(data){
_4564.data=data;
}
if(!_4564.guid){
_4564.guid=this.guid++;
}
if(!_4562.events){
_4562.events={};
}
var _4566=_4562.events[type];
if(!_4566){
_4566=_4562.events[type]={};
if(_4562["on"+type]){
_4566[0]=_4562["on"+type];
}
}
_4566[_4564.guid]=_4564;
_4562["on"+type]=this.handle;
if(!this.global[type]){
this.global[type]=[];
}
this.global[type].push(_4562);
},guid:1,global:{},remove:function(_4567,type,_4569){
if(_4567.events){
if(type&&type.type){
delete _4567.events[type.type][type.handler.guid];
}else{
if(type&&_4567.events[type]){
if(_4569){
delete _4567.events[type][_4569.guid];
}else{
for(var i in _4567.events[type]){
delete _4567.events[type][i];
}
}
}else{
for(var j in _4567.events){
this.remove(_4567,j);
}
}
}
}
},trigger:function(type,data,_456e){
data=jQuery.makeArray(data||[]);
if(!_456e){
jQuery.each(this.global[type]||[],function(){
jQuery.event.trigger(type,data,this);
});
}else{
var _456f=_456e["on"+type],val,fn=jQuery.isFunction(_456e[type]);
if(_456f){
data.unshift(this.fix({type:type,target:_456e}));
if((val=_456f.apply(_456e,data))!==false){
this.triggered=true;
}
}
if(fn&&val!==false){
_456e[type]();
}
this.triggered=false;
}
},handle:function(event){
if(typeof jQuery=="undefined"||jQuery.event.triggered){
return;
}
event=jQuery.event.fix(event||window.event||{});
var _4571;
var c=this.events[event.type];
var args=[].slice.call(arguments,1);
args.unshift(event);
for(var j in c){
args[0].handler=c[j];
args[0].data=c[j].data;
if(c[j].apply(this,args)===false){
event.preventDefault();
event.stopPropagation();
_4571=false;
}
}
if(jQuery.browser.msie){
event.target=event.preventDefault=event.stopPropagation=event.handler=event.data=null;
}
return _4571;
},fix:function(event){
if(!event.target&&event.srcElement){
event.target=event.srcElement;
}
if(event.pageX==undefined&&event.clientX!=undefined){
var e=document.documentElement,b=document.body;
event.pageX=event.clientX+(e.scrollLeft||b.scrollLeft);
event.pageY=event.clientY+(e.scrollTop||b.scrollTop);
}
if(jQuery.browser.safari&&event.target.nodeType==3){
var _4577=event;
event=jQuery.extend({},_4577);
event.target=_4577.target.parentNode;
event.preventDefault=function(){
return _4577.preventDefault();
};
event.stopPropagation=function(){
return _4577.stopPropagation();
};
}
if(!event.preventDefault){
event.preventDefault=function(){
this.returnValue=false;
};
}
if(!event.stopPropagation){
event.stopPropagation=function(){
this.cancelBubble=true;
};
}
return event;
}};
jQuery.fn.extend({bind:function(type,data,fn){
return this.each(function(){
jQuery.event.add(this,type,fn||data,data);
});
},one:function(type,data,fn){
return this.each(function(){
jQuery.event.add(this,type,function(event){
jQuery(this).unbind(event);
return (fn||data).apply(this,arguments);
},data);
});
},unbind:function(type,fn){
return this.each(function(){
jQuery.event.remove(this,type,fn);
});
},trigger:function(type,data){
return this.each(function(){
jQuery.event.trigger(type,data,this);
});
},toggle:function(){
var a=arguments;
return this.click(function(e){
this.lastToggle=this.lastToggle===0?1:0;
e.preventDefault();
return a[this.lastToggle].apply(this,[e])||false;
});
},hover:function(f,g){
function handleHover(e){
var p=(e.type=="mouseover"?e.fromElement:e.toElement)||e.relatedTarget;
while(p&&p!=this){
try{
p=p.parentNode;
}
catch(e){
p=this;
}
}
if(p==this){
return false;
}
return (e.type=="mouseover"?f:g).apply(this,[e]);
}
return this.mouseover(handleHover).mouseout(handleHover);
},ready:function(f){
if(jQuery.isReady){
f.apply(document,[jQuery]);
}else{
jQuery.readyList.push(function(){
return f.apply(this,[jQuery]);
});
}
return this;
}});
jQuery.extend({isReady:false,readyList:[],ready:function(){
if(!jQuery.isReady){
jQuery.isReady=true;
if(jQuery.readyList){
jQuery.each(jQuery.readyList,function(){
this.apply(document);
});
jQuery.readyList=null;
}
if(jQuery.browser.mozilla||jQuery.browser.opera){
document.removeEventListener("DOMContentLoaded",jQuery.ready,false);
}
}
}});
new function(){
jQuery.each(("blur,focus,load,resize,scroll,unload,click,dblclick,"+"mousedown,mouseup,mousemove,mouseover,mouseout,change,select,"+"submit,keydown,keypress,keyup,error").split(","),function(i,o){
jQuery.fn[o]=function(f){
return f?this.bind(o,f):this.trigger(o);
};
});
if(jQuery.browser.mozilla||jQuery.browser.opera){
document.addEventListener("DOMContentLoaded",jQuery.ready,false);
}else{
if(jQuery.browser.msie){
document.write("<scr"+"ipt id=__ie_init defer=true "+"src=//:></script>");
var _458d=document.getElementById("__ie_init");
if(_458d){
_458d.onreadystatechange=function(){
if(this.readyState!="complete"){
return;
}
this.parentNode.removeChild(this);
jQuery.ready();
};
}
_458d=null;
}else{
if(jQuery.browser.safari){
jQuery.safariTimer=setInterval(function(){
if(document.readyState=="loaded"||document.readyState=="complete"){
clearInterval(jQuery.safariTimer);
jQuery.safariTimer=null;
jQuery.ready();
}
},10);
}
}
}
jQuery.event.add(window,"load",jQuery.ready);
};
if(jQuery.browser.msie){
jQuery(window).one("unload",function(){
var _458e=jQuery.event.global;
for(var type in _458e){
var els=_458e[type],i=els.length;
if(i&&type!="unload"){
do{
jQuery.event.remove(els[i-1],type);
}while(--i);
}
}
});
}
jQuery.fn.extend({show:function(speed,_4592){
var _4593=this.filter(":hidden");
speed?_4593.animate({height:"show",width:"show",opacity:"show"},speed,_4592):_4593.each(function(){
this.style.display=this.oldblock?this.oldblock:"";
if(jQuery.css(this,"display")=="none"){
this.style.display="block";
}
});
return this;
},hide:function(speed,_4595){
var _4596=this.filter(":visible");
speed?_4596.animate({height:"hide",width:"hide",opacity:"hide"},speed,_4595):_4596.each(function(){
this.oldblock=this.oldblock||jQuery.css(this,"display");
if(this.oldblock=="none"){
this.oldblock="block";
}
this.style.display="none";
});
return this;
},_toggle:jQuery.fn.toggle,toggle:function(fn,fn2){
var args=arguments;
return jQuery.isFunction(fn)&&jQuery.isFunction(fn2)?this._toggle(fn,fn2):this.each(function(){
jQuery(this)[jQuery(this).is(":hidden")?"show":"hide"].apply(jQuery(this),args);
});
},slideDown:function(speed,_459b){
return this.animate({height:"show"},speed,_459b);
},slideUp:function(speed,_459d){
return this.animate({height:"hide"},speed,_459d);
},slideToggle:function(speed,_459f){
return this.each(function(){
var state=jQuery(this).is(":hidden")?"show":"hide";
jQuery(this).animate({height:state},speed,_459f);
});
},fadeIn:function(speed,_45a2){
return this.animate({opacity:"show"},speed,_45a2);
},fadeOut:function(speed,_45a4){
return this.animate({opacity:"hide"},speed,_45a4);
},fadeTo:function(speed,to,_45a7){
return this.animate({opacity:to},speed,_45a7);
},animate:function(prop,speed,_45aa,_45ab){
return this.queue(function(){
this.curAnim=jQuery.extend({},prop);
var opt=jQuery.speed(speed,_45aa,_45ab);
for(var p in prop){
var e=new jQuery.fx(this,opt,p);
if(prop[p].constructor==Number){
e.custom(e.cur(),prop[p]);
}else{
e[prop[p]](prop);
}
}
});
},queue:function(type,fn){
if(!fn){
fn=type;
type="fx";
}
return this.each(function(){
if(!this.queue){
this.queue={};
}
if(!this.queue[type]){
this.queue[type]=[];
}
this.queue[type].push(fn);
if(this.queue[type].length==1){
fn.apply(this);
}
});
}});
jQuery.extend({speed:function(speed,_45b2,fn){
var opt=speed&&speed.constructor==Object?speed:{complete:fn||!fn&&_45b2||jQuery.isFunction(speed)&&speed,duration:speed,easing:fn&&_45b2||_45b2&&_45b2.constructor!=Function&&_45b2};
opt.duration=(opt.duration&&opt.duration.constructor==Number?opt.duration:{slow:600,fast:200}[opt.duration])||400;
opt.old=opt.complete;
opt.complete=function(){
jQuery.dequeue(this,"fx");
if(jQuery.isFunction(opt.old)){
opt.old.apply(this);
}
};
return opt;
},easing:{},queue:{},dequeue:function(elem,type){
type=type||"fx";
if(elem.queue&&elem.queue[type]){
elem.queue[type].shift();
var f=elem.queue[type][0];
if(f){
f.apply(elem);
}
}
},fx:function(elem,_45b9,prop){
var z=this;
var y=elem.style;
var _45bd=jQuery.css(elem,"display");
y.display="block";
y.overflow="hidden";
z.a=function(){
if(_45b9.step){
_45b9.step.apply(elem,[z.now]);
}
if(prop=="opacity"){
jQuery.attr(y,"opacity",z.now);
}else{
if(parseInt(z.now)){
y[prop]=parseInt(z.now)+"px";
}
}
};
z.max=function(){
return parseFloat(jQuery.css(elem,prop));
};
z.cur=function(){
var r=parseFloat(jQuery.curCSS(elem,prop));
return r&&r>-10000?r:z.max();
};
z.custom=function(from,to){
z.startTime=(new Date()).getTime();
z.now=from;
z.a();
z.timer=setInterval(function(){
z.step(from,to);
},13);
};
z.show=function(){
if(!elem.orig){
elem.orig={};
}
elem.orig[prop]=this.cur();
_45b9.show=true;
z.custom(0,elem.orig[prop]);
if(prop!="opacity"){
y[prop]="1px";
}
};
z.hide=function(){
if(!elem.orig){
elem.orig={};
}
elem.orig[prop]=this.cur();
_45b9.hide=true;
z.custom(elem.orig[prop],0);
};
z.toggle=function(){
if(!elem.orig){
elem.orig={};
}
elem.orig[prop]=this.cur();
if(_45bd=="none"){
_45b9.show=true;
if(prop!="opacity"){
y[prop]="1px";
}
z.custom(0,elem.orig[prop]);
}else{
_45b9.hide=true;
z.custom(elem.orig[prop],0);
}
};
z.step=function(_45c1,_45c2){
var t=(new Date()).getTime();
if(t>_45b9.duration+z.startTime){
clearInterval(z.timer);
z.timer=null;
z.now=_45c2;
z.a();
if(elem.curAnim){
elem.curAnim[prop]=true;
}
var done=true;
for(var i in elem.curAnim){
if(elem.curAnim[i]!==true){
done=false;
}
}
if(done){
y.overflow="";
y.display=_45bd;
if(jQuery.css(elem,"display")=="none"){
y.display="block";
}
if(_45b9.hide){
y.display="none";
}
if(_45b9.hide||_45b9.show){
for(var p in elem.curAnim){
if(p=="opacity"){
jQuery.attr(y,p,elem.orig[p]);
}else{
y[p]="";
}
}
}
}
if(done&&jQuery.isFunction(_45b9.complete)){
_45b9.complete.apply(elem);
}
}else{
var n=t-this.startTime;
var p=n/_45b9.duration;
z.now=_45b9.easing&&jQuery.easing[_45b9.easing]?jQuery.easing[_45b9.easing](p,n,_45c1,(_45c2-_45c1),_45b9.duration):((-Math.cos(p*Math.PI)/2)+0.5)*(_45c2-_45c1)+_45c1;
z.a();
}
};
}});
jQuery.fn.extend({loadIfModified:function(url,_45c9,_45ca){
this.load(url,_45c9,_45ca,1);
},load:function(url,_45cc,_45cd,_45ce){
if(jQuery.isFunction(url)){
return this.bind("load",url);
}
_45cd=_45cd||function(){
};
var type="GET";
if(_45cc){
if(jQuery.isFunction(_45cc)){
_45cd=_45cc;
_45cc=null;
}else{
_45cc=jQuery.param(_45cc);
type="POST";
}
}
var self=this;
jQuery.ajax({url:url,type:type,data:_45cc,ifModified:_45ce,complete:function(res,_45d2){
if(_45d2=="success"||!_45ce&&_45d2=="notmodified"){
self.attr("innerHTML",res.responseText).evalScripts().each(_45cd,[res.responseText,_45d2,res]);
}else{
_45cd.apply(self,[res.responseText,_45d2,res]);
}
}});
return this;
},serialize:function(){
return jQuery.param(this);
},evalScripts:function(){
return this.find("script").each(function(){
if(this.src){
jQuery.getScript(this.src);
}else{
jQuery.globalEval(this.text||this.textContent||this.innerHTML||"");
}
}).end();
}});
if(!window.XMLHttpRequest){
XMLHttpRequest=function(){
return new ActiveXObject("Microsoft.XMLHTTP");
};
}
jQuery.each("ajaxStart,ajaxStop,ajaxComplete,ajaxError,ajaxSuccess,ajaxSend".split(","),function(i,o){
jQuery.fn[o]=function(f){
return this.bind(o,f);
};
});
jQuery.extend({get:function(url,data,_45d8,type,_45da){
if(jQuery.isFunction(data)){
_45d8=data;
data=null;
}
return jQuery.ajax({url:url,data:data,success:_45d8,dataType:type,ifModified:_45da});
},getIfModified:function(url,data,_45dd,type){
return jQuery.get(url,data,_45dd,type,1);
},getScript:function(url,_45e0){
return jQuery.get(url,null,_45e0,"script");
},getJSON:function(url,data,_45e3){
return jQuery.get(url,data,_45e3,"json");
},post:function(url,data,_45e6,type){
if(jQuery.isFunction(data)){
_45e6=data;
data={};
}
return jQuery.ajax({type:"POST",url:url,data:data,success:_45e6,dataType:type});
},ajaxTimeout:function(_45e8){
jQuery.ajaxSettings.timeout=_45e8;
},ajaxSetup:function(_45e9){
jQuery.extend(jQuery.ajaxSettings,_45e9);
},ajaxSettings:{global:true,type:"GET",timeout:0,contentType:"application/x-www-form-urlencoded",processData:true,async:true,data:null},lastModified:{},ajax:function(s){
s=jQuery.extend({},jQuery.ajaxSettings,s);
if(s.data){
if(s.processData&&typeof s.data!="string"){
s.data=jQuery.param(s.data);
}
if(s.type.toLowerCase()=="get"){
s.url+=((s.url.indexOf("?")>-1)?"&":"?")+s.data;
}
}
if(s.global&&!jQuery.active++){
jQuery.event.trigger("ajaxStart");
}
var _45eb=false;
var xml=new XMLHttpRequest();
xml.open(s.type,s.url,s.async);
if(s.data){
xml.setRequestHeader("Content-Type",s.contentType);
}
if(s.ifModified){
xml.setRequestHeader("If-Modified-Since",jQuery.lastModified[s.url]||"Thu, 01 Jan 1970 00:00:00 GMT");
}
xml.setRequestHeader("X-Requested-With","XMLHttpRequest");
if(xml.overrideMimeType){
xml.setRequestHeader("Connection","close");
}
if(s.beforeSend){
s.beforeSend(xml);
}
if(s.global){
jQuery.event.trigger("ajaxSend",[xml,s]);
}
var _45ed=function(_45ee){
if(xml&&(xml.readyState==4||_45ee=="timeout")){
_45eb=true;
var _45ef;
try{
_45ef=jQuery.httpSuccess(xml)&&_45ee!="timeout"?s.ifModified&&jQuery.httpNotModified(xml,s.url)?"notmodified":"success":"error";
if(_45ef!="error"){
var _45f0;
try{
_45f0=xml.getResponseHeader("Last-Modified");
}
catch(e){
}
if(s.ifModified&&_45f0){
jQuery.lastModified[s.url]=_45f0;
}
var data=jQuery.httpData(xml,s.dataType);
if(s.success){
s.success(data,_45ef);
}
if(s.global){
jQuery.event.trigger("ajaxSuccess",[xml,s]);
}
}else{
jQuery.handleError(s,xml,_45ef);
}
}
catch(e){
_45ef="error";
jQuery.handleError(s,xml,_45ef,e);
}
if(s.global){
jQuery.event.trigger("ajaxComplete",[xml,s]);
}
if(s.global&&!--jQuery.active){
jQuery.event.trigger("ajaxStop");
}
if(s.complete){
s.complete(xml,_45ef);
}
xml.onreadystatechange=function(){
};
xml=null;
}
};
xml.onreadystatechange=_45ed;
if(s.timeout>0){
setTimeout(function(){
if(xml){
xml.abort();
if(!_45eb){
_45ed("timeout");
}
}
},s.timeout);
}
var xml2=xml;
try{
xml2.send(s.data);
}
catch(e){
jQuery.handleError(s,xml,null,e);
}
if(!s.async){
_45ed();
}
return xml2;
},handleError:function(s,xml,_45f5,e){
if(s.error){
s.error(xml,_45f5,e);
}
if(s.global){
jQuery.event.trigger("ajaxError",[xml,s,e]);
}
},active:0,httpSuccess:function(r){
try{
return !r.status&&location.protocol=="file:"||(r.status>=200&&r.status<300)||r.status==304||jQuery.browser.safari&&r.status==undefined;
}
catch(e){
}
return false;
},httpNotModified:function(xml,url){
try{
var _45fa=xml.getResponseHeader("Last-Modified");
return xml.status==304||_45fa==jQuery.lastModified[url]||jQuery.browser.safari&&xml.status==undefined;
}
catch(e){
}
return false;
},httpData:function(r,type){
var ct=r.getResponseHeader("content-type");
var data=!type&&ct&&ct.indexOf("xml")>=0;
data=type=="xml"||data?r.responseXML:r.responseText;
if(type=="script"){
jQuery.globalEval(data);
}
if(type=="json"){
eval("data = "+data);
}
if(type=="html"){
jQuery("<div>").html(data).evalScripts();
}
return data;
},param:function(a){
var s=[];
if(a.constructor==Array||a.jquery){
jQuery.each(a,function(){
s.push(encodeURIComponent(this.name)+"="+encodeURIComponent(this.value));
});
}else{
for(var j in a){
if(a[j]&&a[j].constructor==Array){
jQuery.each(a[j],function(){
s.push(encodeURIComponent(j)+"="+encodeURIComponent(this));
});
}else{
s.push(encodeURIComponent(j)+"="+encodeURIComponent(a[j]));
}
}
}
return s.join("&");
},globalEval:function(data){
if(window.execScript){
window.execScript(data);
}else{
if(jQuery.browser.safari){
window.setTimeout(data,0);
}else{
eval.call(window,data);
}
}
}});
}
