$(document).ready(function(){window.requestAnimFrame=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimaitonFrame||function(e){window.setTimeout(e,1e3/60)};var e=document.getElementById("sig-canvas"),t=e.getContext("2d");t.strokeStyle="#222222",t.lineWidth=4;var n=!1,i={x:0,y:0},o=i;function u(e,t){var n=e.getBoundingClientRect();return{x:t.clientX-n.left,y:t.clientY-n.top}}e.addEventListener("mousedown",function(t){n=!0,o=u(e,t)},!1),e.addEventListener("mouseup",function(e){n=!1},!1),e.addEventListener("mousemove",function(t){i=u(e,t)},!1),e.addEventListener("touchstart",function(e){},!1),e.addEventListener("touchmove",function(t){var n=t.touches[0],i=new MouseEvent("mousemove",{clientX:n.clientX,clientY:n.clientY});e.dispatchEvent(i)},!1),e.addEventListener("touchstart",function(t){var n,o;n=t,o=e.getBoundingClientRect(),i={x:n.touches[0].clientX-o.left,y:n.touches[0].clientY-o.top};var u=t.touches[0],d=new MouseEvent("mousedown",{clientX:u.clientX,clientY:u.clientY});e.dispatchEvent(d)},!1),e.addEventListener("touchend",function(t){var n=new MouseEvent("mouseup",{});e.dispatchEvent(n)},!1),document.body.addEventListener("touchstart",function(t){t.target==e&&t.preventDefault()},!1),document.body.addEventListener("touchend",function(t){t.target==e&&t.preventDefault()},!1),document.body.addEventListener("touchmove",function(t){t.target==e&&t.preventDefault()},!1),function e(){requestAnimFrame(e),n&&(t.moveTo(o.x,o.y),t.lineTo(i.x,i.y),t.stroke(),o=i)}();var d=document.getElementById("sig-dataUrl"),c=document.getElementById("sig-image"),a=document.getElementById("id_image"),r=document.getElementById("sig-clearBtn"),s=document.getElementById("sig-submitBtn");r.addEventListener("click",function(t){e.width=e.width,d.innerHTML="Data URL for your signature will go here!",c.setAttribute("src",""),a.setAttribute("value","")},!1),s.addEventListener("click",function(t){var n=e.toDataURL();d.innerHTML=n,c.setAttribute("src",n),a.setAttribute("value",n)},!1)});