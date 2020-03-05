$(document).ready(function(){

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    $('.carousel').carousel()

    $('#register').on('click', function(){
        $('#modalRegisterForm').slideToggle();
    });
    $('#login').on('click', function(){
        $('#modalLoginForm').slideToggle();
    });
    $('#cuenta').on('click', function(){
        $('#modalcuenta').slideToggle();
    });
    $('#cuenta_aut').on('click', function(){
        $('#modalcuenta_aut').slideToggle();
    });

    $('#submit_reg').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('#registerform').serialize();
        $.ajax({
            url: $('#submit_reg').attr('href'),
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                var response = jQuery.parseJSON(respuesta);
                if(response.error){
                    $('.errores').css({display:'block'});
                    $('.errores').css('color','white');
                    $('.errores').css('background-color','red');
                    $('.errores').css('border-radius','6px');
                    $('.errores').css('padding','10px');
                    $('.errores').html(response.msj);
                }else if(response.exito){
                    var redir = $('.user_page').attr('href');
                    $(location).attr('href', redir);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    $('#submit_login').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('#loginform').serialize();
        $.ajax({
            url: $('#submit_login').attr("href"),
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                var response = jQuery.parseJSON(respuesta);
                if(response.error){
                    $('.errores2').css({display:'block'});
                    $('.errores2').css('color','white');
                    $('.errores2').css('background-color','red');
                    $('.errores2').css('border-radius','6px');
                    $('.errores2').css('padding','10px');
                    $('.errores2').html(response.msj);
                }else if(response.success){
                    var redir = $('.user_page').attr('href');
                    $(location).attr('href', redir);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    /*---guardar/eliminar de favoritos---------------------------------------*/
    $('.buttonfav').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('.buttonfav').attr('value');
        $.ajax({
            url: '/' + datos + '/guardar/',
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                var response = jQuery.parseJSON(respuesta);
				if (response.agregar){
					console.log('agregar');
					$('.icon1').removeClass("far fa-heart").addClass('fas fa-heart');
				}else if(response.quitar){
					console.log('quitar');
					$('.icon1').removeClass("fas fa-heart").addClass('far fa-heart');
				}
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    /*---añadir del carro------------------------------*/
    $('.buttoncart').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var id = $('.buttoncart').attr('value');
        var datos = $('#añadir_carro_form').serialize();
        $.ajax({
            url: '/' + id + '/agregar/',
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                var response = jQuery.parseJSON(respuesta);
				if (response.success){
                    $('#añadir_carro_form').hide();
                    $('.button_añadido').css({display: 'block'});
				}else if(response.error){
                    $('.buttoncart').html(response.msj)
				}
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    /*---remover del carro------------------------------*/
    $('.buttonremove').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('.buttonremove').attr('value');
        $.ajax({
            url: '/' + datos + '/quitar/',
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                var response = jQuery.parseJSON(respuesta);
				if (response.exito){
                    $('.buttonremove').hide();
                    $('.button_removido').css({display: 'block'});
				}else if(response.error){
					$('.buttonremove').html(response.msj)
				}
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    $('#submit_search').attr('disabled',true);
    $('#input_search').on('keyup',function(){
        if($(this).val().length !=0)
            $('#submit_search').attr('disabled', false);            
        else
            $('#submit_search').attr('disabled',true);
    });

    $('.buttoncart').attr('disabled',true);
    $('#cant').on('keyup',function(){
        if($(this).val().length !=0)
            $('.buttoncart').attr('disabled', false);            
        else
            $('.buttoncart').attr('disabled',true);
    });

    $('#submit_comment').attr('disabled',true);
    $('#comment').on('keyup',function(){
        if($(this).val().length !=0)
            $('#submit_comment').attr('disabled', false);            
        else
            $('#submit_comment').attr('disabled',true);
    });

    $('.dropdown-toggle').dropdown();
    /*--realizar busquedas----------------------------*/
    $('#input_search').keyup(function(){
        var datos = $('#input_search').serialize();
        $.ajax({
            url: '/resultadosajax/',
            type: 'GET',
            data: datos,
            dataType: 'json',
            success:function(respuesta){
                if(respuesta.exito){
                    console.log(respuesta.objetos);
                    $('.re_busquedas').css({display: 'block'});
                    var html_code = '<ul class="ul_busqueda">';
                    for(const item in respuesta.objetos){
                        html_code += '<li class="li_busqueda"><a class="a_busqueda" href="/' + respuesta.objetos[item].id + '/items/detalles/">' + respuesta.objetos[item].nombre + '</a></li>';
                    }
                    html_code += '</ul>';
                    $('.re_busquedas').html(html_code);
                }else if(respuesta.vacio){
                    console.log(respuesta.objetos);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    $('#input_search').on('blur', function(){
        $('.re_busquedas').css({display: 'none'});
        $('.a_busqueda').css({display: 'none'});
        $('.ul_busqueda').css({display: 'none'});
        $('.li_busqueda').css({display: 'none'});
    });
    /*subir comentario---------------------------------------*/
    $('#submit_comment').on('click', function(e){
        e.preventDefault();
        var radioValue = $("input[name='rating']:checked").val();
        if(radioValue){
            $('#radio_value').val(radioValue);
        }
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('#comment_form').serialize();
        var id = $('#submit_comment').attr('value');
        $.ajax({
            url: '/' + id + '/comentar/',
            type: 'POST',
            dataType: 'json',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            success: function(respuesta){
                if(respuesta.exito){
                    console.log(respuesta.objetos);
                    $('#comment_form').css({display:'none'});
                    $('.user_comment1').html(respuesta.objetos[0]["user"]);
                    $('.user_fecha_comment1').html(respuesta.objetos[0]["fecha"]);
                    $('.comment_text1').html(respuesta.objetos[0]["comentario"]);
                    $('.comment_cal1').html(respuesta.objetos[0]["calificacion"]);
                }else if(respuesta.error){
                    console.log(response.msj)
                    $('.errores3').css({display:'block'});
                    $('.errores3').css('color','white');
                    $('.errores3').css('background-color','red');
                    $('.errores3').css('border-radius','6px');
                    $('.errores3').css('padding','10px');
                    $('.errores3').html(response.msj);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });

    $('#bars').on('click', function(){
        $('.nav_responsive').slideToggle();
    });

    /*---------vaciar carro----------------------------*/
    $('#vaciar').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $('#vaciar').attr('value');
        $.ajax({
            url: '/vaciar/',
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: datos,
            dataType:'json',
            success: function(respuesta){
				if(respuesta.success){
                    $('#vaciar').hide();
                    $('#vacio').css({display: 'none'});
                    $('.vaciar_carro').html(respuesta.msj)
				}
            },
            error: function(e){
                console.log(e);
            }
        });
    });
});
