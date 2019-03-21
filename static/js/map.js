<script>
  window.onload=function(){//原生js选项卡写法
  var oDiv = document.getElementById('div1');
  var aInput = document.getElementsByTagName('input');
  var aCon = oDiv.getElementsByTagName('div');
  for(var i=0;i<aInput.length;i++){
   aInput[i].index = i;
   aInput[i].onclick = function(){
   for(var i=0;i<aInput.length;i++){
    aInput[i].className = '';
    aCon[i].style.display = 'none';
   }
   this.className= 'active';
   aCon[this.index].style.display = 'block';
   }
  }
  }
 </script>