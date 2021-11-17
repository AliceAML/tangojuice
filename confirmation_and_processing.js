document.querySelector("#inputForm").onsubmit

function askConfirmation() {
    var selected_words = checkCheckboxes();
    var fc_nb = selected_words.length;

    const confirm_message = "Do you want to generate " + fc_nb + " flashcards?";
    document.getElementById("confirmation").innerHTML = confirm_message;

}

function checkCheckboxes() {
    var selected_words = [];
    var checkboxes = document.getElementsByName("word");
    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            selected_words.push(checkbox.id);
        }
    }
    return selected_words;
}