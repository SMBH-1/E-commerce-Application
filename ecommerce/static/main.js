axios.defaults.xsrfCookieName='csrftoken';
axios.defaults.xsrfHeaderName='X-CSRFTOKEN';

function addToCart(productID){
  console.log('OnClick' + productID)
  axios.post(`/add-product/${productID}/`)
  .then( (response) =>{
      console.log(response.request.responseURL)
      newURL = response.request.responseURL
      window.location.href = newURL
    } )
  .catch((err) => console.log(err))
}

function openLink(){
  location.href = document.getElementById("link_id").value;
}