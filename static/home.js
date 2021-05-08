const BASE_URL = "http://127.0.0.1:5000"
const DEFAULT_EMPTY_CUPCAKE_IMAGE_URL = 
    "https://c8.alamy.com/comp/DDGC68/empty-muffin-paper-cases-on-a-timber-board-DDGC68.jpg"

$("#cupcake-image").html(`<img src="${ DEFAULT_EMPTY_CUPCAKE_IMAGE_URL }" 
width="200" 
height="200"/>`)
$("form-button").click( addCupcake )

async function addCupcake(){
    const flavor = $("#form-flavor").val()
    const size = $("#form-size").val()
    const image = $("#form-image").val()
    const rate = $("#form-rate").val()
    const cupcakeJSON = await axios.post(`${BASE_URL}/api/cupcakes`,
        {flavor, size, image, rate})
    listCupcake( cupcakeJSON )
}

async function getCupcakes() {
    const cupcakes = await axios.get(`${BASE_URL}/api/cupcakes`)
    for( cupcake of cupcakes["data"]["cupcakes"]){
        listCupcake( cupcake )                
    }
}

function listCupcake( cupcake ) {
    $("#cupcake-list")
        .append(`<li id ="cupcake-${ cupcake["id"]}"></li>`)
    updateCupcakeListing( cupcake )    
}

function updateCupcakeListing( cupcake ) {

    $(`#cupcake-${ cupcake["id"] }`)
        .off()
        .text(`
        Flavor: ${ cupcake["flavor"] },
        Size: ${ cupcake["size"] },
        Rating: ${ cupcake["rating"] } `)
        .hover( () =>{
            $("#cupcake-image")
                .html(`
                <img src="${ cupcake["image"] }" 
                width="200" 
                height="200"/>`)
            },() =>{
                $("#cupcake-image")
                    .html(`
                    <img src="${ DEFAULT_EMPTY_CUPCAKE_IMAGE_URL }" 
                    width="200" 
                    height="200"/>`)
        })
        .click( () => {

            $("#form-flavor").val( cupcake["flavor"] )
            $("#form-size").val( cupcake["size"] )
            $("#form-rating").val( cupcake["rating"] )
            $("#form-image").val( cupcake["image"] )

            $("#form-button").off()
                .text("Update Cupcake")
                .click( () => {
                    updateCupcakeDB( cupcake["id"] )
                })
        })
        .append(`<button id="del-cupcake-${ cupcake["id"] }">x</button>`)
    
    $(`#del-cupcake-${ cupcake["id"] }`)
        .click( async () => {
            await axios
                .delete(`${ BASE_URL }/api/cupcakes/${ cupcake[ "id" ] }`)
            $(`#cupcake-${ cupcake[ "id" ] }`).remove()
        })
}

async function updateCupcakeDB( cupcake_id ) {

    const flavor = $("#form-flavor").val()
    const size = $("#form-size").val()
    const image = $("#form-image").val()
    const rating = $("#form-rating").val()
    const cupcakeJSON = await axios.patch(
        `${BASE_URL}/api/cupcakes/${ cupcake_id }`,
        {flavor, size, image, rating}
    )
    console.log( cupcakeJSON )
    UpdateCupcakeListing( cupcakeJSON )

    $("#form-button").off().click( addCupcake ).text( "Add new cupcake!" )
}

getCupcakes()
