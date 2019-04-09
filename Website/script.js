$( "input" ).focusout(function() {
                               
    var r = document.getElementById('red').value;
    var g = document.getElementById('green').value;
    var b = document.getElementById('blue').value;
    document.getElementById('box').style.background = "rgb("+r+","+g+","+b+")";
    
  });


  var slideCol = document.getElementById("myRange");
  var y = document.getElementById("f");
  y.innerHTML = slideCol.value;
  
  slideCol.oninput = function() {
      y.innerHTML = this.value;
  }
