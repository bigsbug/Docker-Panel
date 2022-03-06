function hide_messages(time) {
    setTimeout(function () {
        container_message = document.getElementById("message-container").style.display = "none";

    }, time)
}
// function set_message(text, type) {
//     span_message = document.getElementById('message-text')
//     span_message.innerText = text
//     span_message.className = 'message-list-item ' + type
// }
// set_message('My Message', 'info')
hide_messages(5000)



// modal actions
const modal_close = document.getElementsByClassName('modal-close')[0];
const modal = document.getElementById('modal-newContainer');
const btn_modal = document.getElementById('modal-btn-newContainer');

function hide_modal(target_modal) {
    target_modal.style.display = 'none'
}
// hide modal
modal_close.onclick = () => {
    hide_modal(modal)
}

window.addEventListener('click', event => {
    if (event.target == modal) {
        hide_modal(modal)
    }
}
)
//show modal
btn_modal.onclick = () => {
    modal.style.display = 'block'
}


// btn_form = document.querySelector('#btn-submit')
window.addEventListener('submit', event => {
    form = event.target
    event.preventDefault()
    const my_form = new FormData(form)
    const plan_form = Object.fromEntries(my_form.entries())
    const data = JSON.stringify(plan_form)
    console.log(data)

    const response = fetch(form.action, {
        method: "POST",
        headers: {
            "Content-type": 'application/json; charset=utf-8',
        },
        body: data,

    })
    response.then(resp => {
        console.log(Object(resp.json()))
    })
    response.catch(() => {
        alert('Error')
    })
})