const callback = arguments[arguments.length -1];
var pre=-1;
var s=setInterval(function()
{var scrollTop=$(this).scrollTop();
if(scrollTop==pre&pre>1000)
{clearInterval(s);
var div=document.getElementsByClassName("search_table_header");
var data="";
for(var i=0;i<div.length;i++){
data=data+div[i].innerHTML.replace(/<\/?.+?>/g,"#")+"|";
}
var ans=document.getElementsByClassName("search_transfer_header")
for(var i=0;i<ans.length;i++){
data=data+ans[i].innerHTML.replace(/<\/?.+?>/g,"#")+"|";
}
callback(data);}
else{pre=scrollTop;var delta=100;window.scrollBy(0,delta);}
},500);