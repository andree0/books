$(function(){
    $("input#btn_delete").click(function(event){
        return confirm("Are you sure you want to remove a book from the list ?")
      });

    $("button.clear").click(function(){
        $("form").find("input").not("input[type=submit]").val('');
        $("select[name='term']").find("option[value='0']").prop("selected", true);
    });

    $("td").addClass("align-middle");
    $("th").addClass("align-middle");
    $(".error").addClass("text-danger");
    $(".success").addClass("text-success");
    $(".errorlist").addClass("alert-danger");
    $("label").addClass("m-2");
    $("form#book_form > p:first").next().next().append( $("form#book_form > div:first")).addClass("d-inline-block");
  });

