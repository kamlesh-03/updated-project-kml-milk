let cart = JSON.parse(localStorage.getItem("kmlCart") || "[]");
function addToCart(productId, name){
  const found = cart.find(x => x.product_id === productId);
  if(found) found.quantity += 1; else cart.push({product_id: productId, name, quantity: 1});
  localStorage.setItem("kmlCart", JSON.stringify(cart));
  alert(name + " added to your website order.");
}
function prepareOrder(form){
  if(cart.length === 0){
    alert("Please add at least one product.");
    return false;
  }
  document.getElementById("order-items").value = JSON.stringify(cart);
  return true;
}
