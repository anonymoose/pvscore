/* This notice must be untouched at all times.

Open-jACOB Draw2D
The latest version is available at
http://www.openjacob.org

Copyright (c) 2006 Andreas Herz. All rights reserved.
Created 5. 11. 2006 by Andreas Herz (Web: http://www.freegroup.de )

LICENSE: LGPL

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License (LGPL) as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA,
or see http://www.gnu.org/copyleft/lesser.html
*/

/**
 * 
 * @version 0.9.23
 * @author Andreas Herz
 * @constructor
 */
Button=function(/*:PaletteWindow*/ palette, /*:int*/ width, /*:int*/ height)
{
  /** @private **/
  this.x   = 0;
  /** @private **/
  this.y   = 0;
  /** @private **/
  this.width= 24;
  /** @private **/
  this.height= 24;
  /** @private **/
  this.id  = UUID.create();
  /** @private **/
  this.enabled=true;
  /** @private **/
  this.active=false;
  /** @private **/
  this.palette = palette;

  /** @private **/
  this.html = this.createHTMLElement();

  if(width!==undefined && height!==undefined)
    this.setDimension(width,height);
  else
    this.setDimension(24,24);

};

Button.prototype.type="Button";

/**
 * @private
 **/
Button.prototype.dispose=function()
{
  //this.id   = null; don't dispose the id! This is important for deregistration
  //this.html = null; don't dispose the id! This is important for deregistration
};


Button.prototype.getImageUrl=function()
{
   return this.type+".png";
};


/**
 * @private
 **/
Button.prototype.createHTMLElement=function()
{
    var item = document.createElement('div');
    item.id        = this.id;
    item.style.position="absolute";
    item.style.left   = this.x+"px";
    item.style.top    = this.y+"px";
    item.style.height = this.width+"px";
    item.style.width  = this.height+"px";
    item.style.margin = "0px";
    item.style.padding= "0px";
    item.style.outline= "none";

    if(this.getImageUrl()!==null)
      item.style.backgroundImage="url("+this.getImageUrl()+")";
    else
      item.style.backgroundImage="";

    var oThis = this;
    this.omousedown=function(event)
    {
       if(oThis.enabled)
       {
          oThis.setActive(true);
       }
       event.cancelBubble = true;
       event.returnValue = false;
    }
    this.omouseup=function(event)
    {
       if(oThis.enabled)
       {
          oThis.setActive(false);
          oThis.execute();
          oThis.palette.setActiveTool(null);
       }
       event.cancelBubble = true;
       event.returnValue = false;
    }

    if (item.addEventListener) 
    {
      item.addEventListener("mousedown", this.omousedown, false);
      item.addEventListener("mouseup", this.omouseup, false);
    }
    else if (item.attachEvent) 
    {
      item.attachEvent("onmousedown", this.omousedown);
      item.attachEvent("onmouseup", this.omouseup);
    }

    return item;
};

/**
 * @private
 **/
Button.prototype.getHTMLElement=function()
{
  if(this.html===null)
    this.html = this.createHTMLElement();
  return this.html;
};


/**
 *
 **/
Button.prototype.execute=function()
{
};

Button.prototype.setTooltip=function(/*:String*/ tooltipText)
{
  this.tooltip = tooltipText;
  if(this.tooltip!==null)
     this.html.title=this.tooltip;
  else
     this.html.title="";

};

/**
 * Return the associated workflow canvas.
 *
 * @since 0.9.19
 * @type Workflow
 **/
Button.prototype.getWorkflow=function()
{
   return this.getToolPalette().getWorkflow();
}

/**
 * Return the associated tool palette.
 *
 * @since 0.9.19
 * @type ToolPalette
 **/
Button.prototype.getToolPalette=function()
{
   return this.palette;
}

/**
 **/
Button.prototype.setActive=function(flag /*:boolean*/)
{
  if(!this.enabled)
    return;
  this.active = flag;
  if(flag===true)
    this.html.style.border="1px inset";
  else
    this.html.style.border="0px";
};

Button.prototype.isActive=function()
{
  return this.active;
};

/**
 * @private
 **/
Button.prototype.setEnabled=function(flag /*:boolean*/)
{
  this.enabled=flag;
  if(flag)
  {
    this.html.style.filter="alpha(opacity=100)";
    this.html.style.opacity="1.0";
  }
  else
  {
    this.html.style.filter="alpha(opacity=30)";
    this.html.style.opacity="0.3";
  }
};

/**
 *
 **/
Button.prototype.setDimension=function( w /*:int*/, h /*:int*/)
{
  this.width = w;
  this.height= h;

  // Falls das Element noch nie gezeichnet wurde, dann braucht aus das HTML nicht 
  // aktualisiert werden
  //
  if(this.html===null)
    return;

  this.html.style.width  = this.width+"px";
  this.html.style.height = this.height+"px";
};

/**
 *
 **/
Button.prototype.setPosition=function(/*:int*/ xPos ,/*:int*/ yPos)
{
  this.x = Math.max(0,xPos);
  this.y = Math.max(0,yPos);
  // Falls das Element noch nie gezeichnet wurde, dann braucht aus das HTML nicht 
  // aktualisiert werden
  //
  if(this.html===null)
    return;

  this.html.style.left = this.x+"px";
  this.html.style.top  = this.y+"px";
};

/**
 *
 **/
Button.prototype.getWidth=function()
{
  return this.width;
};

/**
 *
 **/
Button.prototype.getHeight=function()
{
  return this.height;
};

/**
 *
 **/
Button.prototype.getY=function()
{
    return this.y;
};

/**
 *
 **/
Button.prototype.getX=function()
{
    return this.x;
};

/**
 *
 **/
Button.prototype.getPosition=function()
{
  return new Point(this.x, this.y);
};

