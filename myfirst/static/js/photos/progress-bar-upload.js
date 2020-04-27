$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({//это в настройках подключаемых FILE UPLOAD SCRIPTS
    dataType: 'json',
    sequentialUploads: true,/* 1. SEND THE FILES ONE BY ONE */    
    //singleFileUploads: true means each file of a selection is uploaded using an individual request for XHR type uploads. 
    //Then you can get information of an individual file and call the store procedure with the information you have just got.

    /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
    start: function (e) {//Устанавливает обработчик запуска ajax-запроса, при условии, что в этот момент не выполняются другие ajax-запросы.
      $("#modal-progress").modal("show");
    },
    /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
    stop: function (e) {
      $("#modal-progress").modal("hide");
    },
    /* 4. UPDATE THE PROGRESS BAR */
    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);//анализирует строку и возвращает целое число.
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});/*Возвращает/устанвливает значения css-свойств у выбранных элементов страницы*/
      $(".progress-bar").text(strProgress);/*метод устанавливает или возвращает текстовое содержимое выбранных элементов*/
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(/*Метод вставляет указанное содержимое в начале выбранных элементов.*/
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"/*встовляет новую картинку*/
        )
      }
    }

  });

});