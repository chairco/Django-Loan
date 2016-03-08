$('#pegaModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget)
  var recipient = button.data('whatever')
  var modal = $(this)
  modal.find('.modal-title').text('New to ' + recipient)
  $('#pegasave').click(function() {
    var name = modal.find("input[name='name']").val();
    var email = modal.find("input[name='email']").val();
    $.ajax({
      type: "post",
      url: '/adddri_pega',
      cache: false,
      data: {
        name: name, 
        email: email,
        //csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      dataType: "html",
      success: function(data, result, statues, xml){
        if (data == "False"){
          $("#statusModal").modal({show: true}).find('.modal-body').text("EMAIL格式存在錯誤 或是 使用者名稱已經存在PEGA's GROUP, 請確認.");
        } else {
          $("#statusModal").modal({show: true}).find('.modal-body').text("更新成功");
          $('#id_pegadri').append('<option value="'+data+'">'+name+','+email+'</option>');
          $('#id_pega_dri_mail_group').append('<option value="'+data+'">'+name+','+email+'</option>');
          $('#id_pega_dri_mail_group').multiSelect('refresh');
        }
      }
    });// Ajax End
    return false;
  });
})
