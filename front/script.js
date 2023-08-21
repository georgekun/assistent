eel.expose(js_view_info)

function js_view_info(text) {
    document.querySelector(".vosk").innerHTML = text;
    // const keywords = document.querySelector(".keywords")

}


const exit = document.querySelector(".exit")
exit.addEventListener("click", () => {
    eel.py_exit_program()
})