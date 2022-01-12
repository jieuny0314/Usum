$(document).ready(function(){
			var imgs;
			var imgs2;
			var img_count;
			var img_count2;
			var img_position = 1;	//지금 보여지는 이미지 번호
			var img_position2 = 1;

			imgs = $(".slider .imgSlide");
			imgs2 = $(".slider2 .imgSlide2");
	//imgSlide가져오기
			img_count = imgs.children().length;	
			img_count2 = imgs2.children().length;
	//.slider .imgSlide의 자식, 즉 li의 갯수 = 이미지의 갯수
		
		$('#prev').on('click', function(){
			console.log("W");
			prev();
		});

		$('#next').on('click', function(){
			next();
		});

		function prev(){
			if(1 < img_position){	//1번 이미지보다 뒤의 이미지에 있을 때
				imgs.animate({left:'+=333px'}, 500);	//이미지의 width값이 780이므로 왼쪽으로 780만큼 움직여서 슬라이드되는 것처럼 보이게 함.
				
				img_position--;
				imgs2.animate({left:'+=333px'}, 500);
				
				img_position2--;	//하나 뒤로 갔으니 이미지 번호도 줄여줌
				
			}	
		}

		function next(){
			if(img_count > img_position){
				imgs.animate({left: '-=333px'}, 500);
				img_position++;
			}	//이미지 갯수가 1개보다 많으면
			if(img_count2 > img_position2){
				imgs2.animate({left: '-=333px'}, 500);
				img_position2++;
			}	
		}
	});