def html():
    return """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta name="viewport" content="width=device-width, minimum-scale=1.0, user-scalable=no">
<meta name="copyright" content="Copyright (C) 2019-2023 Akkiesoft, MIT License">
<meta charset="utf-8">
<title>マスコン</title>
<style type="text/css">
* { margin: 0; padding: 0; }
body { background: #777777; width: 100%; font-family: sans-serif; }
.mascon { margin: 0 auto; display: table; }
.mascon > div {
  display: table-cell;
  vertical-align: middle;
  border: 1px solid #000;
}
.mascon .label {
  font-family: sans-serif;
  font-size: 16px;
  line-height: 20px;
  background-color: #333333;
}
.eb { color: red; }
.br { color: yellow; }
.pp { color: white; }
.controller input[type=range] {
  -webkit-appearance: none;
  transform: rotate(90deg); 
  width: 200px;
}
.controller input[type=range]::-webkit-slider-runnable-track {
	height: 5px;
	background: gray;
}
.controller input[type=range]::-webkit-slider-thumb {
	-webkit-appearance: none;
	width: 40px;
	height: 160px;
	background: #000000;
    margin-top: -78px;
}
#dir { width:80px; }
.center { text-align: center; }
</style>
</head>
<body>
<div class="mascon">
  <div class="controller"><input id="cont" type="range" orient="vertical" value="5" min="0" max="9" step="1" onchange="updatespeed()" /><br></div>
  <div class="label">
    <span class="eb">- EB</span><br>
    <span class="br">- B4</span><br>
    <span class="br">- B3</span><br>
    <span class="br">- B2</span><br>
    <span class="br">- B1</span><br>
    <span class="pp">- &nbsp;&nbsp;-</span><br>
    <span class="pp">- P1</span><br>
    <span class="pp">- P2</span><br>
    <span class="pp">- P3</span><br>
    <span class="pp">- P4</span>
  </div>
<span id="contvalue">-</span>
</div>
<div class="center" id="result">-</div>
<div class="center">
前 <input id="dir" type="range" value="0" min="0" max="1" step="1" onchange="updatedir()" /> 後
</div>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
</body>

<script>
  var com = ['EB', 'B4', 'B3', 'B2', 'B1', '-', 'P1', 'P2', 'P3', 'P4'];
  var elem = document.getElementById('cont');
  var target = document.getElementById('contvalue');
  var rangeValue = function (elem, target) {
    return function(evt){
      target.innerHTML = com[elem.value];
    }
  }
  elem.addEventListener('input', rangeValue(elem, target));

function updatespeed() {
  var elem = document.getElementById('cont');
  fetch('/'+com[elem.value], { method: 'GET' }).then(function(r){ return r.text(); }).then(function(t){ 
    document.getElementById('result').innerText = t;
  });
}
function updatedir() {
  var elem = document.getElementById('dir');
  var dir = elem.value;
  fetch('/DIR/' + dir, { method: 'GET' }).then(function(r){ return r.text() }).then(function(t){
    if (t == "X") { elem.value = 1 - dir; }
  });
}
</script>
</html>
"""#.replace("\n", "")