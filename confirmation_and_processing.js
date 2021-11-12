function askConfirmation() {
        var selected_words = checkCheckboxes()
        var fc_nb = selected_words.length

        const confirm_message = "Do you want to generate " + fc_nb + " flashcards?"
        document.getElementById("confirmation").innerHTML = confirm_message;

      }

    function checkCheckboxes(){
    var selected_words = [];
    var checkboxes = document.getElementsByName("word");
    for(var i=0,cbLen=checkboxes.length;i<cbLen;i++){
        if(checkboxes[i].checked){
        selected_words.push(checkboxes[i].id);}
    }
    return selected_words
    }