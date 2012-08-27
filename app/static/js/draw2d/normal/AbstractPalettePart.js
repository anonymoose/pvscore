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
 * Base class for elements which can be inserted into an external
 * tool palette.<br>
 * Objects of this class can be drag&drop around the hole web page. An event will
 * be fired if the element has been dropped into the canvas.<br>
 * Inherited classes should override the drop event method to implement
 * special behaviour.
 *
 * @version 0.9.23
 * @author Andreas Herz
 * @constructor
 * @since 0.9.18
 */
AbstractPalettePart=function()
{
  /** @private*/
  this.x = 0;
  /** @private*/
  this.y = 0;
  /** @private*/
  this.html=null;
};

/** @private **/
AbstractPalettePart.prototype.type="AbstractPalettePart";
AbstractPalettePart.prototype = new Draggable();


/**
 * @private
 **/
AbstractPalettePart.prototype.createHTMLElement=function()
{
    var item = document.createElement('div');
    item.id = this.id;
    item.style.position="absolute";
    item.style.height = "24px";
    item.style.width  = "24px";
    return item;
};

/**
 * Called by the frame to set the parent of the palette part.
 *
 * @private
 * @final
 **/
AbstractPalettePart.prototype.setEnviroment=function(/*:Workflow*/ workflow, /*:ExternalPalette*/ palette)
{
  this.palette = palette;
  this.workflow = workflow;
};

/**
 * @private
 * @final
 **/
AbstractPalettePart.prototype.getHTMLElement=function()
{
  if(this.html===null)
  {
    this.html = this.createHTMLElement();
    Draggable.call(this, this.html);
  }
  return this.html;
};


/**
 * @private
 **/
AbstractPalettePart.prototype.onDrop=function(/*:int*/ eventX, /*:int*/ eventY)
{
   var scrollLeft = this.workflow.getScrollLeft();
   var scrollTop  = this.workflow.getScrollTop();
   var xOffset = this.workflow.getAbsoluteX();
   var yOffset = this.workflow.getAbsoluteY();

   // set object to original position 
   this.setPosition(this.x, this.y);

   this.execute(eventX+scrollLeft-xOffset, eventY+scrollTop-yOffset);
};

/**
 *
 **/
AbstractPalettePart.prototype.execute=function(/*:int*/ x, /*:int*/ y)
{
  alert("inerited class should override the method 'AbstractPalettePart.prototype.execute'");
};

AbstractPalettePart.prototype.setTooltip=function(/*:String*/ tooltipText)
{
  this.tooltip = tooltipText;
  if(this.tooltip!==null)
     this.html.title=this.tooltip;
  else
     this.html.title="";
};


/**
 *
 **/
AbstractPalettePart.prototype.setDimension=function(/*:int*/ w,/*:int*/ h)
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
AbstractPalettePart.prototype.setPosition=function(xPos /*int*/, yPos /*int*/)
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
  this.html.style.cursor = "move";
};

/**
 *
 **/
AbstractPalettePart.prototype.getWidth=function()
{
  return this.width;
};

/**
 *
 **/
AbstractPalettePart.prototype.getHeight=function()
{
  return this.height;
};

/**
 *
 **/
AbstractPalettePart.prototype.getY=function()
{
    return this.y;
};

/**
 *
 **/
AbstractPalettePart.prototype.getX=function()
{
    return this.x;
};

/**
 * @type Point
 **/
AbstractPalettePart.prototype.getPosition=function()
{
  return new Point(this.x, this.y);
};


/**
 * Utility function to disable text selection on the handsover element
 *
 * @private
 **/
AbstractPalettePart.prototype.disableTextSelection=function(/*:HTMLElement*/ e)
{
   // disable text selection
   //
   if (typeof e.onselectstart!="undefined") //IE route
      e.onselectstart=function(){return false;};
   else if (typeof e.style.MozUserSelect != "undefined") //Firefox route
      e.style.MozUserSelect="none";
};
