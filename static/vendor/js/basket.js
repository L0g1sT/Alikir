$(document).ready(function () {
    $('.quantity-input').on('change', function () {
        var basketId = $(this).data('basket-id');
        var quantity = $(this).val();
        $.ajax({
            url: '/products/baskets/update_quantity/' + basketId + '/', // Обновленный URL-адрес
            method: 'POST',
            data: {
                'basket_id': basketId,
                'quantity': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                // Обновим сумму и общее количество товаров в корзине
                $('.total-sum').text(data.total_sum.replace('.', ',') + ' руб.');
                $('.total-quantity').text(data.total_quantity);
                var basketSum = $('.basket-sum[data-basket-sum=' + basketId + ']');
                basketSum.find('.basket-sum-value').text(data.basket_sum.toString().replace('.', ',') + ' руб.');
                console.log(data.basket_sum)
                console.log(data.total_sum);

                // Обновим видимость кнопки "Оформить заказ"
                if (data.total_sum > 0) {
                    $('.order-button').show();
                } else {
                    $('.order-button').hide();
                }
            },


            error: function (xhr, textStatus, errorThrown) {
                console.log(xhr.responseText);
            }
        });
    });
    $('#continue-button').click(function(e) {
    e.preventDefault(); // Предотвращаем отправку формы

    // Отправляем форму с помощью AJAX
    $.ajax({
        url: $(this).closest('form').attr('action'),
        method: $(this).closest('form').attr('method'),
        data: $(this).closest('form').serialize(),
        success: function(response) {
            // Очищаем корзину после успешной отправки формы
            $('.total-quantity').text(0);
            $('.total-sum').text(0);
            $('.card.mb-3').remove();

            // Отображаем сообщение об успешном оформлении заказа
            $('<div class="alert alert-success">Заказ успешно оформлен</div>').insertAfter('form');
        },
        error: function(error) {
            // Отображаем сообщение об ошибке при отправке формы
            $('<div class="alert alert-danger">Произошла ошибка при оформлении заказа</div>').insertAfter('form');
        }
    });
});
});
