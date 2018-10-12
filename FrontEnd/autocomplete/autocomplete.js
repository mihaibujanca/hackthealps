var places;
function retriveLocations(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			places = JSON.parse(this.responseText);
			console.log(places);
		}
	};
	xmlhttp.open("GET", "https://2af4ab4b.ngrok.io/locations?lat=46.739125&lon=11.95784", false);
	xmlhttp.send();
	
}

// Array of names
var names = [];
function getNames(array){
	for (var i=0; i < array.length; i++){
		var name = {
			"name":"",
			"distance":0
		};
		name.name = array[i].Name;
		name.distance = array[i].Distance;
		names[i] = name;
	}
}
// CALL RETRIVE INFORMATION
retriveLocations();
// EXTRACT NAMES
getNames(places);

// SET ROUTE WHEN CLICK
var route;
function goToLocation(name){
	 for (var i = 0; i < places.length; i++) {
        if (places[i].Name === name) {
			// If route already exist just change the last waypoint
			if (route == null){
			route = L.Routing.control({ waypoints: [
				L.latLng(46.739125, 11.95784),
				L.latLng(places[i].Latitude, places[i].Longitude)
		],
				routeWhileDragging: true,
				router: L.Routing.graphHopper('28cffa38-92cf-4404-8fa1-5a19717bac74')
				
				//serviceUrl: 'http://192.168.170.131:5000/route/v1'
			})
			route.addTo(mymap);
			}
			else{
				route.spliceWaypoints(route.getWaypoints().length - 1, 1,L.latLng(places[i].Latitude, places[i].Longitude)	);
			}
			// Update UI
			document.getElementById("destination").innerHTML = "Destination: <strong> "+places[i].Name+"</strong>";
			document.getElementById("tempdest").innerHTML = "Dest. altitude: <strong> "+places[i].Altitude+"m</strong>";
			//document.getElementsByClassName("rightInfo")[0].display = ""; 
			return true;
        }
    }
    return null;
}


function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].name.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].name.substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].name.substr(val.length);
		  // ADD DISTANCE
		  b.innerHTML += "<strong> - " + arr[i].distance.toFixed(1) + "m</strong>";
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i].name + "'>";
		  
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
			  // Navigate to that location
			  goToLocation(inp.value);
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}

autocomplete(document.getElementById("myInput"), names);
