function fun(){
	// alert("hello");
	// document.getElementById("save_detail").submit();
	// document.save_detail.submit();
	$(document).ready(function(){
	$.ajaxSetup({
		data:{csrfmiddlewaretoken:'{{ csrf_token }}'},
	});
	$(window).unload(function(){
		var text = document.getElementById("is_interested").value;
		alert(text);
		$.ajax({
			url:"{% url 'interest' article.id %}",
			type:"post",
			data:{
				is_interested:text
			},
			success:function(data){
			},
			error:function(){
				alert("false");
			}
		})
		return false; //阻止表单再次提交引起跳转到奇怪页面。
	});
});
	alert("hello");
}

// 	$(document).ready(function(){
// 	$.ajaxSetup({
// 		data:{csrfmiddlewaretoken:'{{ csrf_token }}'},
// 	});
// 	$(window).unload(function(){
// 		var text = document.getElementById("is_interested").value;
// 		alert(text);
// 		$.ajax({
// 			url:"{% url 'interest' article.id %}",
// 			type:"post",
// 			data:{
// 				is_interested:text
// 			},
// 			success:function(data){
// 			},
// 			error:function(){
// 				alert("false");
// 			}
// 		})
// 		return false; //阻止表单再次提交引起跳转到奇怪页面。
// 	});
// });

//// 用于出版商访问时记录是否感兴趣
// function interest(){
// 	interest_nums++;
// 	var text;
// 	alert(interest_nums)
// 	console.log(interest_nums);
// 	if(interest_nums%2==1){
// 		interested_it=1;		//1表示感兴趣
// 		var the_str="";
// 		document.getElementById("is_interested").value=1;
// 		text=1;
// 		if(interested_it==0){
// 			the_str="/static/images/heart_off.png";
// 		}
// 		if(interested_it==1){
// 			the_str="/static/images/heart.png";
// 		}
// 	}else{
// 		interested_it=0;		//0表示不感兴趣
// 		var the_str="";
// 		document.getElementById("is_interested").value=0;
// 		text = 0;
// 		if(interested_it==0){
// 			the_str="/static/images/heart_off.png";
// 		}
// 		if(interested_it==1){
// 			the_str="/static/images/heart.png";
// 		}
// 	}
// 	$(document).ready(function(){
// 		$.ajaxSetup({
// 			data:{csrfmiddlewaretoken:'{{ csrf_token }}'},
// 		});
// 		$.ajax({
// 			url:"{% url 'interest' article.id %}",
// 			type:"post",
// 			data:{
// 				is_interested:text
// 			},
// 			success:function(data){
// 				alert(data)
// 			},
// 			error:function(){
// 				alert("false");
// 			}
// 		});
// 	});
// 	document.getElementById("ok_no").innerHTML="<div id=12_1 style='width:50px;border-bottom:2px solid red;display:flex;flex-direction:column;' onclick='interest()'></div>";
// 	document.getElementById("12_1").innerHTML="<img src="+the_str+"  style='margin-top:auto;width:30px;height:30px;margin-left:auto;margin-right:auto;'></img><div>感兴趣</div>";
// }