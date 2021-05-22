function pay() {
   fetch('/api/pay', {
        method: 'post',
        headers: {
            'Context-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        location.href= '/payment';
    })
    .catch(err => {
        location.href = '/payment';
    });
}

function changeActive(id) {
    fetch('/api/changeActive', {
         method: 'post',
         body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Context-Type': 'application/json',
        }
    })
    .then(res => console.log(res))
    .then(data=>{
    alert("Thao tác thành công")
        location.reload()
    })
    .catch(err=>{
    alert("Thao tác thất bại")
        location.reload();
    })
}

function delCart(id) {
   fetch('/api/delCart', {
        method: 'post',
        body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Context-Type': 'application/json'
        }

    })
    .then(data => {
        location.href = '/payment';
    })
    .catch(err => {
        location.href = '/payment';
    });
}


function reg_price(id) {
    fetch('/api/reg_price', {
         method: 'post',
         body: JSON.stringify({
            'id': id
         }),
         headers: {
            'Context-Type': 'application/json',
         }
    })
    .then(data=>{
    alert("Thao tác thành công")
        location.reload()
    })
    .catch(err=>{
    alert("Thao tác thất bại")
        location.reload();
    })
}

