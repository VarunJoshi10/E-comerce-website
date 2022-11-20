let HomeAndLivingArr = [
    {
      image_url:
        'https://assets.myntassets.com/f_webp,dpr_1.5,q_60,w_210,c_limit,fl_progressive/assets/images/13374272/2022/1/1/6327ebd6-7a7b-48b7-be42-d3b7d97bd58a1641030225627SaralHomeBrownBeigeColourblockedAnti-SkidBedRunner1.jpg',
      name: 'Brown & Beige Colourblocked Anti-Skid Bed Runner',
      price: '₹999',
      strikedoffprice: '₹1999',
      brand: 'Saral Home',
      discount: '50% OFF',
    },
    
  ]
  
  let cartArr = JSON.parse(localStorage.getItem('cartData')) || []
  window.addEventListener('load', function () {
    cartItems()
  })
  
  function sortByGivenOptions() {
    selected = document.querySelector('#sort').value
    if (selected == 'Ascending') {
      HomeAndLivingArr.sort(function (a, b) {
        if (Number(a.price.substring(1)) > Number(b.price.substring(1))) return 1
        if (Number(a.price.substring(1)) < Number(b.price.substring(1))) return -1
        return 0
      })
      displayPage(HomeAndLivingArr)
    }
    if (selected == 'Descending') {
      HomeAndLivingArr.sort(function (a, b) {
        return Number(b.price.substring(1)) - Number(a.price.substring(1))
      })
      displayPage(HomeAndLivingArr)
    }
    if (selected == 'Discount') {
      HomeAndLivingArr.sort(function (a, b) {
        if (a.discount > b.discount) return -1
        if (a.discount < b.discount) return 1
        return 0
      })
      displayPage(HomeAndLivingArr)
    }
  }
  function filterByGivenOptions() {
    selected = document.querySelector('#filter').value
    let filterList = HomeAndLivingArr.filter(function (el) {
      return el.brand == selected
    })
    displayPage(filterList)
  }
  function sortByNames() {
    selected = document.querySelector('#sortNames').value
    if (selected == 'Ascending') {
      HomeAndLivingArr.sort(function (a, b) {
        if (a.name > b.name) return 1
        if (a.name < b.name) return -1
        return 0
      })
      displayPage(HomeAndLivingArr)
    }
    if (selected == 'Descending') {
      HomeAndLivingArr.sort(function (a, b) {
        if (a.name > b.name) return -1
        if (a.name < b.name) return 1
        return 0
      })
      displayPage(HomeAndLivingArr)
    }
  }
  
  homeAndLivingArr = JSON.parse(localStorage.getItem('cartData')) || []
  displayPage(HomeAndLivingArr)
  
  function displayPage(HomeAndLivingArr) {
    document.querySelector('#container').innerHTML = ''
    HomeAndLivingArr.forEach(function (el) {
      let box = document.createElement('div')
  
      let img = document.createElement('img')
      img.setAttribute('src', el.image_url)
      let name = document.createElement('h4')
      name.innerText = el.name.substring(0, 27) + '...'
      name.style.fontWeight = 'bold'
      let price = document.createElement('p')
      price.innerHTML = el.price
      let strikedoffprice = document.createElement('p')
      strikedoffprice.innerHTML = el.strikedoffprice
      let discount = document.createElement('p')
      discount.innerHTML = el.discount
      let prices = document.createElement('div')
      //    prices.innerHTML=`<div id="prices" ></div>`
      prices.append(price, strikedoffprice, discount)
      let brand = document.createElement('h4')
      brand.innerText = el.brand
      brand.style.color = 'gray'
      let add2Cart = document.createElement('button')
      add2Cart.innerText = 'Add to Cart'
      add2Cart.addEventListener('click', function () {
        addToCart(el)
      })
      box.append(img, name, brand, prices, add2Cart)
      document.querySelector('#container').append(box)
      //    console.log(box);
    })
  }
  
  function addToCart(ele) {
    let flag = false
    for (let i = 0; i < cartArr.length; i++) {
      if (cartArr[i].name == ele.name) {
        cartArr[i].quantity++
        cartArr[i].cartprice = cartArr[i].price * cartArr[i].quantity
        flag = true
        alert(`Product ${ele.name} Added to Cart ${cartArr[i].quantity} Times`)
      }
    }
    if (!flag) {
      ele.quantity = 1
      ele.price = Number(ele.price.substring(1, ele.price.length))
      ele.cartprice = ele.price * ele.quantity
      cartArr.push(ele)
      alert(`Product ${ele.name} Added to Cart Succesfully`)
    }
    localStorage.setItem('cartData', JSON.stringify(cartArr))
    cartItems()
  }
  function Gotohome() {
    window.location.href = 'index.html'
  }
  function cartItems(){
    let temp = JSON.parse(localStorage.getItem('cartData')) || []
    let items=0
    temp.forEach(function(ele){
      items+=ele.quantity
    })
    document.getElementById("cart-items").innerText=items
  }
  