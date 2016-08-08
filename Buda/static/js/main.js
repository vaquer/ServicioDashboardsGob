$(document).ready(function() {

    //var urlDescargasDatos = 'partials/example.json';
    var urlDescargasDatos = '/tablero-instituciones/apicomparativa/recursos-mas-descargados/';
    var newDataSet, descargasDatos;
    //Datos mas descargados
    $.ajax({
      url: urlDescargasDatos,
      async: false,
      type: 'GET',
      success: function(data) {
        $.each(data.recursos, function(key, value){
          var htmlDatos = '';
          htmlDatos += '<tr><td class="datosTitle" title="'+value[0]+'">' + value[0] + '</td><td class="text-center">' + value[1].toLocaleString('en') + '</td></tr>';
          $('#table-datos tr').first().after(htmlDatos);
        });
      }
    });

    $('[data-toggle="tooltip"]').tooltip();

    //var urlDataSet = 'partials/last_json.json';
    var urlDataSet = '/tablero-instituciones/apicomparativa/';
    var downTotal = 0;
    var resourTotal = 0;
    
    $('#apf_table').dataTable({
      "language": {
          "paginate": {
            "previous": "Anterior",
            "next": "Siguiente"
          }
        },
      "info": false,
      "bLengthChange": false,
      "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
        $('td:eq(0)', nRow).addClass("depenTitle").attr("title",aData.institucion).attr("tag", aData.slug);
        $('td:eq(3)', nRow).attr( "data-score",aData.apertura ).addClass("rating text-center").html("");
        $('td:eq(1), td:eq(2), td:eq(4)', nRow).addClass("text-center");
        $('td:eq(5)', nRow).addClass("starsTd text-center");
      },
      drawCallback: function(settings){
            var api = this.api();
            // Initialize custom control
            initRating(api.table().container());
        },
      "ajax": {
        "url": urlDataSet,
        "async": false,
        "dataSrc": function ( json ) {
          //console.log(json.dependencias);
          //META.fn: sortJSON
          function sortJSON(data, key) {
            return data.sort(function (a, b) {
                var x = a[key];
                var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
          }

          var top5Down = sortJSON(json.dependencias, 'descargas');
          
          $.each(top5Down,function(key, value){
            var totalItems = top5Down.length;
            top1 = top5Down[totalItems-1];
            top2 = top5Down[totalItems-2];
            top3 = top5Down[totalItems-3];
            top4 = top5Down[totalItems-4];
            top5 = top5Down[totalItems-5];
          });

          var htmlDown = '';
          htmlDown += '<tr><td class="datosTitle" title="'+top1.institucion+'">' + top1.institucion + '</td><td class="text-center">' + top1.descargas.toLocaleString('en') + '</td></tr>';
          htmlDown += '<tr><td class="datosTitle" title="'+top2.institucion+'">' + top2.institucion + '</td><td class="text-center">' + top2.descargas.toLocaleString('en') + '</td></tr>';
          htmlDown += '<tr><td class="datosTitle" title="'+top3.institucion+'">' + top3.institucion + '</td><td class="text-center">' + top3.descargas.toLocaleString('en') + '</td></tr>';
          htmlDown += '<tr><td class="datosTitle" title="'+top4.institucion+'">' + top4.institucion + '</td><td class="text-center">' + top4.descargas.toLocaleString('en') + '</td></tr>';
          htmlDown += '<tr><td class="datosTitle" title="'+top5.institucion+'">' + top5.institucion + '</td><td class="text-center">' + top5.descargas.toLocaleString('en') + '</td></tr>';
          $('#table-downloads tr').last().after(htmlDown);

          $.each(json.dependencias,function(key, value){
            downTotal = downTotal + value.descargas;
            resourTotal = resourTotal + value.total;
            $("#downloadsTotal").html(downTotal.toLocaleString('en'));
            $("#resourcesTotal").html(resourTotal.toLocaleString('en'));
            $("#dependencesTotal").html(json.dependencias.length);
          });
          return json.dependencias;
        }
      },
      "columns": [
          { "data": "institucion" },
          { "data": "ranking" },
          { "data": "total", render: $.fn.dataTable.render.number( ',', '.', 0 ) },
          { "data": "apertura" },
          { "data": "descargas", render: $.fn.dataTable.render.number( ',', '.', 0 )  },
          { "data": "calidad" }
      ]
    });

    $("#searchbox").keyup(function() {
        $('#apf_table').dataTable().fnFilter(this.value);
        //table.draw();
    });

    // Initializes jQuery Raty control
    function initRating(container){
      $('.rating', container).raty({
        starType: 'i',
        hints       : ['1', '2', '3', '4', '5'],
        half: true,
        starHalf: 'glyphicon glyphicon-star gly-2x',
        starOff: 'glyphicon glyphicon-star-empty gly-2x',
        starOn: 'glyphicon glyphicon-star gly-2x',
        readOnly: true,
        score: function() {
            return $(this).attr('data-score');
        }
      })
    };

    $('#apf_table tbody').on('click', 'tr', function () {
        var titleVar = $(this).find(".depenTitle").attr('tag');
        window.location.href = "/tablero-instituciones/detalle/" + titleVar + "/";
    });

});
