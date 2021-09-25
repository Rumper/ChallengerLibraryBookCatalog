
function books_events_delete(pk, isbn){
	var form = $('#books_delete')
	var crsf_token = form.find('input[name="csrfmiddlewaretoken"]')
	form.find('input').remove();
	for(value of [[isbn, 'isbn'], [pk, 'pk']]) form.append($('<input>', {type: 'hidden', 'value': value[0], 'name': value[1]}))
	form.append(crsf_token)
	$('#delete_modal_book').find('span.isbn').html(isbn);
}

function books_submit_delete(){
	var form = $('#books_delete')
	var isbn = form.find('input[name="isbn"]').val();
	var ajax = $.ajax({
		url: form.attr('action').replace('1111', form.find('input[name="pk"]').val()),
		type : 'DELETE',
		headers: { 'X-CSRFToken': form.find('input[name="csrfmiddlewaretoken"]').val()}})
	ajax.done(function(){
		$('#delete_modal_book .close').click()
		$(`#book-${isbn}`).remove();
		var number = parseInt($('#total-books .number').text()) - 1;
		if (!number){
			$('#total-books-empty').removeClass('hidden')
			$('#total-books').addClass('hidden')
		}
	})
	ajax.fail(function(response){
		// TODO: Hacer mostrar mensajes de errores de formulario
	});
}

function get_form(url, action, modal){
	if (!modal){
		$('#EditModalBook .title').html($('.books .title-book').html())
		modal = '#edit_books'
	}
	$(modal).attr('action', action)
	var ajax = $.ajax({
		url: url,
	})
	ajax.done(function(response){
		$(`${modal} #fields`).html(response)
	})
	ajax.fail(function(response){
		alert('form not found')
	});
}

function form_books(id_form){
	var form = $(id_form)
	var ajax = $.ajax({
		url: form.attr('action'),
		type: form.attr('method'),
		headers: { 'X-CSRFToken': form.find('input[name="csrfmiddlewaretoken"]').val()},
		data: form.serialize()
	})
	ajax.done(function(response){
		location.href = `http://${location.host}${response.success_url}`
	})
	ajax.fail(function(response){
		form.find('.errors').remove()
		show_errors(form, (response.responseJSON || {}).errors || {})
	});

}

function show_errors(form, errors, prefix){
	if (prefix) prefix += '-'
	var error = $('<div>', {class: 'errors'})
	for(var field in errors){
		if(field == 'formset'){
			for(var idx in (errors.formset || {})){
				show_errors(form, errors.formset[idx] || {}, 'form-'+ idx)
			}
			continue
		}
		form.find(`#id_${prefix || ''}${field}`).parent().append(
			error.clone().html(errors[field])
		)
	}
}