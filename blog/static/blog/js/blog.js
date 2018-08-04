
function show_reply_box(comment_id) {
    $("#id_superior_id").val(comment_id);
    $("#comment-post").appendTo($("#div-comment-" + comment_id));
    $("#comment-title").hide();
    $("#comment-cancel").show();
}

function cancel_reply() {
    $("#comment-title").show();
    $("#comment-cancel").hide();
    $("#id_superior_id").val('')
    $("#comment-post").prependTo($("#comment-area"));
}

$("#add-category").click(function(){
    $.post(
        "/category/add/", 
        {category:$("#new-category-name").val()},
        function(result) {
            if(result['success'] === 0) {
                alert("无效分类");
            }
            else {
                $("#id_category").find("option:selected").attr("selected",false);
                $("#id_category").append('<option value="'+result['id']+'" selected>'+result['name']+'</option>')   
            }
        }
    )
});

$("#add-tag").click(function(){
    $.post(
        "/tag/add/", 
        {tag:$("#new-tag-name").val()},
        function(result) {
            if(result['success'] === 0) {
                alert("无效标签");
            }
            else {
                $("#id_tags").append('<option value="'+result['id']+'" selected>'+result['name']+'</option>')
            }
        }
    )
});