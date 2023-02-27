$(function(){
	$(‘#busqueda’).keyup(function() {
		$.ajax({
			type: “POST”,
			url: “searchAjax/”,
			data: {
				‘busqueda’: $(‘#busqueda’).val(),
				‘csrfmiddlewaretoken’: $(“input[name=csrfmiddlewaretoken]”).val()
			},
			success: searchSuccess,
			dataType: ‘html’
		});
	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$(‘#resultado_busqueda’).html(data);
}