
document.addEventListener('DOMContentLoaded', function() {
   
    console.log("elements Are loaded");

    const btn = document.getElementsByClassName('update-cart');
    const size_select = document.getElementsByName('size');
    
    
    
    
    for (i = 0; i < size_select.length; i++) {
        size_select[i].addEventListener('change', function(){
            size = this.value
            return console.log('size:', size);
            });
        }    

    

    for (i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', function(){
            
            const pizzaName = this.dataset.name
            const product_id = this.dataset.product
            const action_id = this.dataset.action
            console.log('productId:', product_id, 'action:', action_id, 'pizza_name', pizzaName);
        
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