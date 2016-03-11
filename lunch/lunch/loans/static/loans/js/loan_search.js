$(".name_submit").click(function(){
    var nickname = $("input[name='nickname']").val();
    console.log(nickname)
    $(".name_value").text("");
    $(".name_value").append("<br>搜尋中...約30秒內 ");
    $.ajax({
      url:"/utkvalue",
      type:"post",
      data:{"nickname":nickname},
      dataType:"json",
      success:function(data){
        $(".name_value").text("");
        $(".name_value").append("<hr></hr>");

        //$(".name_value").append("<hr></hr>UTK: "+data+"<br>");
        //for (var i in data) {
        // i 為 key，把 data 的每一項顯示在網頁上
        //$('.name_value').append("<br>" + i + " : " + data[i] + "<br>");
        //}

        //var trHTML = '';
        var trHeader = '';
        var trContent = '';
        var trTable = '';
        var count = 0;
        for (var i in data) {
            //trHTML += '<tr><td>' + i + ": " + '</td><td>' + data[i] + '</td></tr>';
            trHeader += '<th>' + i + '</th>';
            trContent += '<td>' + data[i] + '</td>';
        };
        trHeader = '<thead><tr>' + trHeader + '</tr></thead>';
        trContent = '<tbody><tr>' + trContent + '</tr></tbody>';
        trTable = '<table class="table table-striped table table-hover" style="font-size:12px;">' + trHeader + trContent + '</table>'
        //$('.name_value').append(trHTML)
        $('.name_value').append(trTable)
      }
    }); //AJAXEnd
  });

