CrossConnectionDecorator=function(){
};
CrossConnectionDecorator.prototype=new ConnectionDecorator();
CrossConnectionDecorator.prototype.paint=function(g){
g.drawLine(15,8,15,-8);
};
