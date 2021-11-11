function checkCheckbox(){
    var selected_words = [];
    var checkboxes = document.getElementsByName("word");
    for(var i=0,cbLen=checkboxes.length;i<cbLen;i++){
        if(checkboxes[i].checked){
        selected_words.push(checkboxes[i].id);}
    }
    console.log(selected_words)
    return selected_words
    }