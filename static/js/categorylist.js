$(document).ready(function(){
$('.category').each(function(){
	var category = $(this);
	var percentage = category.find('.category-percentage').text();
	category.find('.category-bar').animate({width : percentage}, 1000);
});
	$('.skills').animate({opacity : 1}, 1200);
	
	var ctxP = document.getElementById("pieChart").getContext('2d');
    var myPieChart = new Chart(ctxP, {
      type: 'pie',
      data: {
		  labels: ["음식점", "카페", "교통", "놀거리", "편의점", "패션", "생필품", "기타"],
          datasets: [{
		  data: [30, 30, 15, 10, 5, 3, 2, 5],
          backgroundColor: ["#ef404a", "#f79552", "#ffd400", "#80b463", "#b0dfdb", "#81d3eb", "#9e7eb9", "black"],
          
        }]
      },
      options: {
        responsive: true,
        legend: {
            position: 'right',
			 labels: {
                    fontColor: "#848484",
                    boxWidth: 20,
                    padding: 20,
				 	fontSize: 10
                }
         }
      }
    });
});
