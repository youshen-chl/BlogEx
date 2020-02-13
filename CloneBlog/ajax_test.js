a.ajax({
    url:_deel.url+"/ajax/comment.php",
    data:a(this).serialize(),
    type:a(this).attr("method"),
    error:function(w){
        a(".comt-loading").hide();
        a(".comt-error").show().html(w.responseText);
        setTimeout(
            function(){
            $submit.attr("disabled",false).fadeTo("slow",1);
            a(".comt-error").fadeOut()
            },3000
        )
    },
    success:function(B){
        a(".comt-loading").hide();
        r.push(a("#comment").val());
        a("textarea").each(function(){this.value=""});
        var y=addComment,A=y.I("cancel-comment-reply-link"),w=y.I("wp-temp-form-div"),C=y.I(y.respondId),x=y.I("comment_post_ID").value,z=y.I("comment_parent").value;
        if(!o&&$comments.length){
            n=parseInt($comments.text().match(/\d+/));
            $comments.text($comments.text().replace(n,n+1))
        }
        new_htm='" id="new_comm_'+k+'"></';
        new_htm=(z=="0")?('\n<ol style="clear:both;" class="commentlist commentnew'+new_htm+"ol>"):('\n<ul class="children'+new_htm+"ul>");
        ok_htm='\n<span id="success_'+k+b;ok_htm+="</span><span></span>\n";
        if(z=="0"){
            if(a("#postcomments .commentlist").length){
                a("#postcomments .commentlist").before(new_htm)
            }
            else{
                a("#respond").after(new_htm)
            }
        }else{
            a("#respond").after(new_htm)
        }
        a("#comment-author-info").slideUp();
        console.log(a("#new_comm_"+k));
        a("#new_comm_"+k).hide().append(B);
        a("#new_comm_"+k+" li").append(ok_htm);
        a("#new_comm_"+k).fadeIn(4000);
        $body.animate({scrollTop:a("#new_comm_"+k).offset().top-200},500);
        a(".comt-avatar .avatar").attr("src",a(".commentnew .avatar:last").attr("src"));
        l();
        k++;
        o="";
        a("*").remove("#edit_id");
        A.style.display="none";
        A.onclick=null;
        y.I("comment_parent").value="0";
        if(w&&C){
            w.parentNode.insertBefore(C,w);
            w.parentNode.removeChild(w)
        }
    }
});

