var Scriptaculous={Version:"1.7.0",require:function(_3d8b){
document.write("<script type=\"text/javascript\" src=\""+_3d8b+"\"></script>");
},load:function(){
if((typeof Prototype=="undefined")||(typeof Element=="undefined")||(typeof Element.Methods=="undefined")||parseFloat(Prototype.Version.split(".")[0]+"."+Prototype.Version.split(".")[1])<1.5){
throw ("script.aculo.us requires the Prototype JavaScript framework >= 1.5.0");
}
$A(document.getElementsByTagName("script")).findAll(function(s){
return (s.src&&s.src.match(/scriptaculous\.js(\?.*)?$/));
}).each(function(s){
var path=s.src.replace(/scriptaculous\.js(\?.*)?$/,"");
var _3d8f=s.src.match(/\?.*load=([a-z,]*)/);
(_3d8f?_3d8f[1]:"builder,effects,dragdrop,controls,slider").split(",").each(function(_3d90){
Scriptaculous.require(path+_3d90+".js");
});
});
}};
Scriptaculous.load();
