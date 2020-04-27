
document.getElementById("ahab").onmouseover = function(){mouseOver()};
document.getElementById("ahab").onmouseout = function() {mouseOut()};
function mouseOver(){
	document.getElementById("ahab").style.color = "red";
	
}
function mouseOut() {
  document.getElementById("ahab").style.color = "black";
}

function closeMenu(){
	var subm = document.querySelectorAll("li.submenu");
	for (var i=0; i<subm.length; i++){
		subm[i].style.display="none"; 
	}
}


document.getElementById("sear").onmouseover = function(event){
	var target = event.target;
	if (target.className == "men-item col-6"){
		var s = target.getElementsByClassName("submenu");
		closeMenu();
		var l = s.length;
		for (var i=0; i<l; i++){
			s[1].style.display="block";

		}

	}
}

document.onmouseover = function(event){
	var target = event.target;
	if (target.className!="men-item col-6" && target.className!="submenu"){
		closeMenu();
	}
}


//это часть у нас munu-link сплывающие меню на главной странице
$(document).ready(function(){
	var link = $('.menu-link');
	var link_active = $('.menu-link_active');

	link.click(function(){
		alert('hhh');
		link.toogleClass('.menu-link_active');
	});
	link_active.click(function(){
		link.removeClass('.menu-link_active');
	});
});