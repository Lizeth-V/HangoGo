function autocomplete(inp, arr) {
  var currentFocus;
  /* starts autocompleting after every word */
  inp.addEventListener("input", function(e) {
    /* inititate values to start autocomplete div */
    var a, b, i, val = this.value;
    /* reset the autocomplete lists */
    closeAllLists();
    if (!val) { return false;}
    currentFocus = -1;
    /* create a bigger div that holds all locations that have the same prefixes */
    a = document.createElement("div");
    a.setAttribute("class", "autocomplete-items");
    /*append to this div to autocomplete container:*/
    this.parentNode.appendChild(a);
    /* before the other locations, append current location div first */
    b = document.createElement("div");
    b.innerHTML = "Current Location <input type='hidden' value='Current Location'>";
    a.appendChild(b);
    /* if click on location, automatically fills in the rest of the input with the value */
    b.addEventListener("click", function(e) {
      inp.value = this.getElementsByTagName("input")[0].value;
      inp.style.fontWeight = 'bold';
      closeAllLists();
    });
    /* check every location in the cities array to see which one matches*/
    for (i = 0; i < arr.length; i++) {
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        /* create divs of the locations (with bolded words) */
        b = document.createElement("div");
        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>" + arr[i].substr(val.length) + "<input type='hidden' value='" + arr[i] + "'>"
        /* if click on location, automatically fills in the rest of the input with the value */
        b.addEventListener("click", function(e) {
          inp.value = this.getElementsByTagName("input")[0].value;
          inp.style.fontWeight = 'bold';
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
    var scroll_autocomplete = document.querySelector('.autocomplete-items');
    var x = document.getElementsByClassName("autocomplete-items")[0];
    if (x) x = x.getElementsByTagName("div");
    /* if down key pressed, highlight down */
    if (e.key == "ArrowDown") {
      removeHighlight(x);
      currentFocus++;
      highlight(x);
      /* allow scrolling as key down is pressed */
      if (currentFocus%3==0){
        var scrollby = (currentFocus/3)*123;
        scroll_autocomplete.scrollTop = scrollby;
      }
      /* if up key pressed, highlight up */
    } else if (e.key == "ArrowUp") {
      removeHighlight(x);
      currentFocus--;
      highlight(x);
      /* allow scrolling as key up is pressed */
      if ((currentFocus+1)%3==0){
        var scrollby = (((currentFocus+1)/3)*123)-123;
        scroll_autocomplete.scrollTop = scrollby;
      }
      if (currentFocus == (x.length-1)){
        scroll_autocomplete.scrollTop = scroll_autocomplete.scrollHeight;
      }
      /* if enter key pressed, don't submit form but instead replace input with the list */
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });
  /* add highlight */
  function highlight(x) {
    if (!x){
      return false;
    } 
    /* cycle highlights */
    if (currentFocus >= x.length){
      currentFocus = 0;
    }
    if (currentFocus < 0){
      currentFocus = (x.length - 1);
    }
    x[currentFocus].classList.add("autocomplete-highlight");
  }
  /* remove highlight */
  function removeHighlight(x) {
    if (currentFocus >= 0){
      x[currentFocus].classList.remove("autocomplete-highlight");
    }
  }
  /* close all autocomplete lists */
  function closeAllLists() {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists();
  });
}

  