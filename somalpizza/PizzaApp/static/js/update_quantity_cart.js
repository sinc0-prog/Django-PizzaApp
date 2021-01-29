
document.addEventListener('DOMContentLoaded', function() {
   
    console.log("elements Are loaded");

    const btn = document.getElementsByClassName('update-cart');

    for (i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', function(){
            const product_id = this.dataset.product
            const action_id = this.dataset.action
            const pizzaName = this.dataset.name
            const size = this.dataset.size

            console.log('productId:', product_id, 'action:', action_id, 'pizza_name', pizzaName, 'size:', size);
        
            console.log("USER", user);
            if (user === 'AnonymousUser'){
                console.log("Not logged in");
            }else{
                updateUserOrder(product_id, action_id, pizzaName, size)
            }
        });
    }
     

    function updateUserOrder(product_id, action_id, pizzaName, size){
        console.log("User is logged in, sending data...");
        console.log(pizzaName);

        var url = '/update_item/'
        fetch(url, {
            method:'POST',
            headers:{
                'Conten-Type':'application/json',
                'X-CSRFToken': csrftoken,
                },
            body: JSON.stringify({'productId': product_id, 'action': action_id, 'pizza_name': pizzaName, 'size': size})
        })
        .then((response) =>{
            return response.json();
        })
    
        .then(data => {
            console.log('data', data);
            location.reload();
        })
        
    }
});   