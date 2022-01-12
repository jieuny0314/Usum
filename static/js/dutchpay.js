  
$().ready(function () {
            $(".send-yes").click(function () {
				Swal.fire({
                    title: '장재훈\n(334-3263-2352-23)',
                    text: "님에게 이체하시겠습니까?",
                    icon: 'question',
					showCancelButton: true,
					customClass : 'sweet-size',
                    confirmButtonColor: '#6eb5ff',
					cancelButtonColor: '#ffabab',
                    confirmButtonText: '예',
                    cancelButtonText: '아니오'
                }).then((result) => {
                    if (result.isConfirmed) {
                        Swal.fire(
                            '이체가\n 완료되었습니다.'
                            
                        )
                    }
                })
            });
	
        });

