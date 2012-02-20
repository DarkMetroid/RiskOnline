function draw(canvas, image){
	
	var ctx = canvas.getContext('2d');
	var img = new Image();
	img.onload = function(){
		ctx.drawImage(img, 0,0, 640,480);
		ctx.stroke();
	};
	img.src = image;
};

function makeDiv(x,y, id){//, message){
	var divNode = document.createElement('div');
	divNode.setAttribute('id', id);
	divNode.setAttribute('style', 'position:absolute; left:' + x + 'px; top:' + y  + 'px; border-style:solid; border-width:5px; border-color:red; width:50px; height:50px;');
	divNode.setAttribute('onClick', "alert('asdasd');");
	document.getElementById('thebody').insertBefore(divNode, null);
	return divNode;
};

var obj;
function ajaxDivData(url, processChange) {
  // native  object

	if (window.XMLHttpRequest) {
	// obtain new object
	obj = new XMLHttpRequest();
	// set the callback function
	obj.onreadystatechange = processChange;
	// we will do a GET with the url; "true" for asynch
	obj.open("GET", url, true);
	// null for GET with native object
	obj.send(null);
	// IE/Windows ActiveX object
	} else if (window.ActiveXObject) {
	obj = new ActiveXObject("Microsoft.XMLHTTP");
		if (obj) {
		  obj.onreadystatechange = processChange;
		  obj.open("GET", url, true);
		  // don't send null for ActiveX
		  obj.send();
		}
	} else {
	alert("Your browser does not support AJAX");
	}
};

function getDivPositions() {
	// 4 means the response has been returned and ready to be processed
	if (obj.readyState == 4) {
		// 200 means "OK"
		if (obj.status == 200) {
			t_to_pos = eval('(' + obj.responseText + ')');
			canvas = document.getElementById('map');
			var div;
			for(var i in t_to_pos){
				div = makeDiv(t_to_pos[i][0] + canvas.offsetLeft, t_to_pos[i][1] + canvas.offsetTop, i)
				div.appendChild(document.createTextNode(t_to_pos[i][2]));
			}
		} else {
			//Problem	
			alert(obj.status);
		}
	}
};