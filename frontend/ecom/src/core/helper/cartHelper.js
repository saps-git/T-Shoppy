export const addItemToCart = (item, next) => { // to add an item to the cart in the browser
    let cart = []; // taking an empty cart array to add items
    if (typeof window !== undefined) { // typeof window is for browser, so if it exists
      if (localStorage.getItem("cart")) { // check if any item exist in local storage already
        cart = JSON.parse(localStorage.getItem("cart")); // if is there, then add them to the array in normal format
      }
  
      cart.push({ //else
        ...item, //push all the item recievd as paramter to the array
      }); 
      localStorage.setItem("cart", JSON.stringify(cart)); // add those item in the local storage in JSON format
      next();
    }
  };

export const loadCart = () => { // loading all elements in the cart
  if(typeof window !== undefined){
    if(localStorage.getItem("cart")){
      return JSON.parse(localStorage.getItem("cart"))
    }
  }
}

export const removeItemFromCart = (productId) => {
  let cart = [];
  if (typeof window !== undefined) {
    if (localStorage.getItem("cart")) {
      cart = JSON.parse(localStorage.getItem("cart"));
    }
    cart.map((product, i) => {
      if (product.id === productId) {
        cart.splice(i, 1);
      }
    });
    localStorage.setItem("cart", JSON.stringify(cart));
  }
  return cart;
};

export const cartEmpty = (next) => {
  if(typeof window !== undefined){
    localStorage.removeItem("cart")
    let cart = []
    localStorage.setItem("cart", JSON.stringify(cart))
    next()
  }
}