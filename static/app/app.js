$(function(){
    $("input#btn_delete").click(function(event){
        return confirm("Are you sure you want to remove a book from the list ?")
      });

    $("button#clear_form").click(function(){
        $('form').find("input").not("input[type=submit]").val('');
    });

    $("td").addClass("align-middle");

    $(".errorlist").addClass("alert-danger");
  });

