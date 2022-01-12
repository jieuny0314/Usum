$(document).ready(function(){
	$('.make-couplecode').click(function(){
		Swal.fire({
                    title: '"장재훈" 님의 커플코드는' ,
                    text: "'0#928&#50' 입니다.",
                    icon: 'info',
					showCancelButton: false,
					customClass : 'sweet-size',
                    confirmButtonColor: '#6eb5ff',
					confirmButtonText: '확인',
                    
                })
	});
});