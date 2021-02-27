var updatecart = document.getElementsByClassName('add-cart')

for (i = 0; i< updatecart.length; i++) {
    updatecart[i].addEventListener('click', function(){
         var productId = this.dataset.product
         var action = this.dataset.action
         console.Log('productId:', productId, 'Action:', action)
         })
}