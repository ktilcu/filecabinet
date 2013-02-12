var saveButton = document.getElementById('saveContent');
var pageID = window.location.href.split("/").pop();
if (saveButton){
    saveButton.addEventListener("click", function(){
        markdown = $('textarea').get(0).value;
        console.log(markdown)
        var request = $.ajax({
            type:"POST",
            url: "/edit/" + pageID,
            data: {'content': markdown},
            datatype: 'json'
        });

        request.done(function(msg){
            console.log(msg);
        });
        request.fail(function(msg){
            alert(msg);
        });
    }, false);
}