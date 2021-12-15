//글쓰기 폼 유효성 검사
function checkWriting(){
    var form = document.writeForm;    //폼 선택
    var title = form.title.value;     //입력받은 글제목 값
    var content = form.content.value; //입력받은 글내용 값

    if(title == ""){ //제목이 비어있으면
        alert("제목은 필수 입력 항목입니다.");
        form.title.focus();  //커서를 위치로 보냄
        return false;
    }
    else if(content == ""){  //내용이 비었으면
        alert("글 내용은 필수 입력 항목입니다.");
        form.content.focus();  //커서를 위치로 보냄
        return false;
    }
    else{
        form.submit();   //폼 전송
    }
}