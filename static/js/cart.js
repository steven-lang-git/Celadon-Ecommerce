var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var quantityInput = this.closest('form').querySelector('.quantity-2, .qty'); // Get the quantity input field

        var quantity = 1; // Default quantity
        if (quantityInput) {
            quantity = parseInt(quantityInput.value, 10); // Get the quantity from the input field
        }

        // console.log('productId:', productId, 'Action:', action, 'Quantity:', quantity);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('Not logged in');
        } else {
            updateUserOrder(productId, action, quantity);
        }
    });
}


function updateUserOrder(productId, action, quantity) {
    console.log('User is logged in, sending data..');
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action, 'quantity': quantity }), // Include quantity in the request
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('data:', data);
            window.location.reload();
        });
}