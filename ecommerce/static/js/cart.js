let updateBtns = document.getElementsByClassName('update-cart')

for(let i=0 ; i<updateBtns.length ; i++){
    updateBtns[i].addEventListener('click',function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        if(user === 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action){
    console.log('anonymous user')
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('removed item')
            delete cart[productId]
        }
    }
    console.log('cart',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
} 

function updateUserOrder(productId,action){
    // let url = "{% url 'updateItem' %}"
    let url = '/updateItem/'
    fetch(url,{
        method:'POST',
        headers:{
            'Accept': 'application/json, text/plain, */*',
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({productId:productId,action:action})
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        location.reload();
    })

}
