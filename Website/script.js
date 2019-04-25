$( "input" ).focusout(function() {
                               
    var r = document.getElementById('red').value;
    var g = document.getElementById('green').value;
    var b = document.getElementById('blue').value;
    document.getElementById('box').style.background = "rgb("+r+","+g+","+b+")";
    
});








