function getTags(){
	var content = document.getElementById("tags").childNodes;   //获取选取标签栏的子节点
	var submit_tags = document.getElementById("choose_tags");
	var submit_mine = document.getElementById("my_tags");
	var mytags = document.getElementById("my_sign").childNodes;
	var tags = "";
	var mine = "";
	for(i=0;i<content.length;i++){		//从子节点中提取出标签值
		tags += content[i].value+" ";
	}
	for(i=0;i<mytags.length;i++){
		mine += mytags[i].innerHTML+" ";
	}
	// alert(mine);
	submit_tags.value = tags;
	return true;
}