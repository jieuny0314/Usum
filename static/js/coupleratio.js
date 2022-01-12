$(document).ready(function(){
//$('.category').each(function(){
//	var category = $(this);
//	var percentage = category.find('.category-percentage').text();
//	category.find('.category-bar').animate({width : percentage}, 1000);
//});
//	$('.skills').animate({opacity : 1}, 1200);
	
	var ctxP = document.getElementById("pieChart").getContext('2d');
    var myPieChart = new Chart(ctxP, {
      type: 'pie',
      data: {
		  labels: ["장재훈", "김지은"],
          datasets: [{
		  data: [62, 48],
          backgroundColor: ["#d3afd5", "#f7b4be"],
          
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
				 	fontSize: 20
                }
         }
      }
    });
});
